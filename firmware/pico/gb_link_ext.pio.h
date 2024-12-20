// -------------------------------------------------- //
// This file is autogenerated by pioasm; do not edit! //
// -------------------------------------------------- //

#pragma once

#if !PICO_NO_HARDWARE
#include "hardware/pio.h"
#endif

// ----------- //
// gb_link_ext //
// ----------- //

#define gb_link_ext_wrap_target 0
#define gb_link_ext_wrap 11
#define gb_link_ext_pio_version 0

static const uint16_t gb_link_ext_program_instructions[] = {
            //     .wrap_target
    0xff40, //  0: set    y, 0                   [31]
    0xff20, //  1: set    x, 0                   [31]
    0x9f80, //  2: pull   noblock                [31]
    0xe047, //  3: set    y, 7                       
    0x3f21, //  4: wait   0 pin, 1               [31]
    0xbf42, //  5: nop                           [31]
    0x7f01, //  6: out    pins, 1                [31]
    0x3fa1, //  7: wait   1 pin, 1               [31]
    0xbf42, //  8: nop                           [31]
    0x5f01, //  9: in     pins, 1                [31]
    0x0084, // 10: jmp    y--, 4                     
    0x9f00, // 11: push   noblock                [31]
            //     .wrap
};

#if !PICO_NO_HARDWARE
static const struct pio_program gb_link_ext_program = {
    .instructions = gb_link_ext_program_instructions,
    .length = 12,
    .origin = -1,
    .pio_version = 0,
#if PICO_PIO_VERSION > 0
    .used_gpio_ranges = 0x0
#endif
};

static inline pio_sm_config gb_link_ext_program_get_default_config(uint offset) {
    pio_sm_config c = pio_get_default_sm_config();
    sm_config_set_wrap(&c, offset + gb_link_ext_wrap_target, offset + gb_link_ext_wrap);
    return c;
}

static inline void gb_link_ext_program_init(
    PIO pio, 
    uint sm,
    uint offset,
    uint si,
    uint sc,
    uint so
) {
    assert(sc == si+1);
    pio_sm_config c = gb_link_ext_program_get_default_config(offset);
    sm_config_set_in_pins(&c, si);
    pio_sm_set_consecutive_pindirs(pio, sm, si, 2, false);
    pio_gpio_init(pio, si);
    pio_gpio_init(pio, sc);
    sm_config_set_out_pins(&c, so, 1);
    pio_sm_set_consecutive_pindirs(pio, sm, so, 1, true);
    pio_gpio_init(pio, so);
    sm_config_set_in_shift(
        &c,
        false,
        false,
        8
    );
    sm_config_set_out_shift(
        &c,
        false,
        false,
        8
    );
    pio_sm_init(pio, sm, offset, &c);
    pio_sm_set_enabled(pio, sm, true);
}

#endif

