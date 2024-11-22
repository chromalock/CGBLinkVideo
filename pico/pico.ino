#include <pico/stdlib.h>
#include <hardware/clocks.h>
#include <hardware/pio.h>
#include <hardware/spi.h>
#include "./Buffer.h"
#include "./TripleBuffer.h"
#include "./DoubleBuffer.h"
#include "./SingleBuffer.h"
#include "./util.h"
#include "./gb_link_ext.pio.h"

#include <SerialTransfer.h>

SerialTransfer transfer;

Buffer *gb_buffer = NULL;

constexpr size_t GB_RECV_TIMEOUT = 2000;
constexpr size_t UART_RECV_TIMEOUT = 2000;

// Note: The pins have to be in ascending order. You can change SI, but SC = SI+1 and SO = SI+2
constexpr auto SI = 2;
constexpr auto SC = 3;
constexpr auto SO = 4;

PIO pio = pio0;
uint sm;
uint offset;
uint timeout;
int pio_irq;

volatile size_t front_position = 0;
uint last_gb_recv;

static inline int gb_get() {
  return pio_sm_get(pio, sm);
}

static inline int gb_get_blocking() {
  return pio_sm_get_blocking(pio, sm);
}

static inline int gb_avail() {
  return pio_sm_get_rx_fifo_level(pio, sm);
}

static inline void gb_put(uint8_t byte) {
  pio_sm_put(pio, sm, byte << 24);
}

static inline void gb_put_blocking(uint8_t byte) {
  pio_sm_put_blocking(pio, sm, byte << 24);
}

// GB Receive IRQ
static void pio_irq_func() {
  last_gb_recv = millis();
  uint8_t c = gb_get();

  if (!gb_buffer) {
    return;
  }

  // Reset position at start of frame
  if (c == 0x00) {
    gb_buffer->swap_if_ready();
    front_position = 0;
  }

  gb_put(gb_buffer->get_front()[front_position]);
  front_position = (front_position + 1) % gb_buffer->size();
}

// CORE 0 : PIO + IRQ

void setup() {
  last_gb_recv = millis();

  offset = pio_add_program(pio, &gb_link_ext_program);
  sm = pio_claim_unused_sm(pio, true);
  gb_link_ext_program_init(pio, sm, offset, SI, SC, SO);

  pio_irq = (pio == pio0) ? PIO0_IRQ_0 : PIO1_IRQ_0;

  irq_get_exclusive_handler(pio_irq);
  irq_add_shared_handler(pio_irq, pio_irq_func, PICO_SHARED_IRQ_HANDLER_DEFAULT_ORDER_PRIORITY);
  irq_set_enabled(pio_irq, true);
  const uint irq_index = pio_irq - ((pio == pio0) ? PIO0_IRQ_0 : PIO1_IRQ_0);
  pio_set_irqn_source_enabled(pio, irq_index, (pio_interrupt_source_t)(pis_sm0_rx_fifo_not_empty + sm), true);  // Set pio to tell us when the FIFO is NOT empty
}

void loop() {
  delay(GB_RECV_TIMEOUT);
  // if no data has been received in time, restart the pio
  if (millis() - last_gb_recv > GB_RECV_TIMEOUT) {
    pio_sm_restart(pio, sm);
    gb_link_ext_program_init(pio, sm, offset, SI, SC, SO);
    pio_sm_clear_fifos(pio, sm);
    last_gb_recv = millis();
  }
}

// CORE 1 : Serial Input + Output

constexpr auto MAX_BUFFER_SIZE = 5760;

enum BufferType {
  Single = 0,
  Double = 1,
  Triple = 2
};

struct Parameters {
  bool preserve_front;
  size_t size;
  BufferType buffer_type;
};

Parameters params;

void setParametersCallback() {
  transfer.rxObj(params);
  if (gb_buffer) {
    delete gb_buffer;
    gb_buffer = NULL;
  }
  switch (params.buffer_type) {
    case BufferType::Single:
      gb_buffer = new SingleBuffer(params.size);
      break;
    case BufferType::Double:
      gb_buffer = new DoubleBuffer(params.size);
      break;
    case BufferType::Triple:
      gb_buffer = new TripleBuffer(params.size);
      break;
  }
}

void recvDataCallback() {
  if (gb_buffer) {
    gb_buffer->write(transfer.packet.rxBuff, transfer.bytesRead);
  }
}

void clearCallback() {
  if (gb_buffer) {
    gb_buffer->clear(params.preserve_front);
  }
}

const functionPtr callbacks[] = { setParametersCallback, recvDataCallback, clearCallback };

void setup1() {
  Serial.begin(921600);

  configST config;
  config.timeout = UART_RECV_TIMEOUT;
  config.debug = false;
  config.callbacks = callbacks;
  config.callbacksLen = sizeof(callbacks) / sizeof(functionPtr);

  transfer.begin(Serial, config);

  gb_buffer->clear(false);
}

void loop1() {
  transfer.tick();
}
