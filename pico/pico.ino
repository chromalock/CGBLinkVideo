#include <pico/stdlib.h>
#include <hardware/clocks.h>
#include <hardware/pio.h>
#include <hardware/spi.h>
#include "./TripleBuffer.h"
#include "./DoubleBuffer.h"
#include "./SingleBuffer.h"
#include "./util.h"
#include "./gb_link_ext.pio.h"

constexpr size_t GB_RECV_TIMEOUT = 2000;
constexpr size_t UART_RECV_TIMEOUT = 2000;

// whether or not the buffer should retain 
// the last frame after a timeout
constexpr bool PRESERVE_FRONT = false;

constexpr size_t BUFFER_LEN = 5760;
// Note: make sure its a fraction of the buffer len.
// Also, on my machine 192 is the max size so it can result in
// a deadlock if the RX_LEN is above 192. Change this value to be
// a lower fraction if you run into an issue. Ultimately even
// an RX_LEN of 1 should be fine, if not potentially slower.
constexpr size_t RX_LEN = 2;

// Note: The pins have to be in ascending order. You can change SI, but SC = SI+1 and SO = SI+2
constexpr auto SI = 2;
constexpr auto SC = 3;
constexpr auto SO = 4;

// Use triple buffering when the latency of the source is important (live streaming)
// Use double buffering when you want  (playing videos)
// Use single buffering when you dont care about screen tearing, and latency of the source is important

// With triple buffering, write()s will not block, they will just start overwriting the previous buffer
// With double buffering, write()s will block
// With single buffering, writes() will not block

#define Buffer TripleBuffer

Buffer video_data(BUFFER_LEN);

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
  
  // Reset position at start of frame
  if (c == 0x00) {
    video_data.swap_if_ready();
    front_position = 0;
  }
  
  gb_put(video_data.get_front()[front_position]);
  front_position = (front_position + 1) % BUFFER_LEN;
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

uint8_t rxBuf[RX_LEN] = { 0 };
uint last_uart_recv = 0;

void setup1() {
  Serial.begin(921600);
  last_uart_recv = millis();
  video_data.clear(false);
}

void loop1() {
  if (millis() - last_uart_recv > UART_RECV_TIMEOUT) {
    video_data.clear(PRESERVE_FRONT);
    Serial.flush();
    while (Serial.read() > -1)
      ;
    last_uart_recv = millis();
  }
  while (Serial.available() >= RX_LEN) {
    auto readBytes = Serial.readBytes(rxBuf, RX_LEN);
    video_data.write(rxBuf, readBytes);
    last_uart_recv = millis();
  }
}
