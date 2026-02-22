// Wokwi Custom Chip - 74LS08 Quad 2-Input AND Gate
#include "wokwi-api.h"
#include <stdio.h>
#include <stdlib.h>

typedef struct {
  pin_t pin_1A; pin_t pin_1B; pin_t pin_1Y;
  pin_t pin_2A; pin_t pin_2B; pin_t pin_2Y;
  pin_t pin_3A; pin_t pin_3B; pin_t pin_3Y;
  pin_t pin_4A; pin_t pin_4B; pin_t pin_4Y;
  pin_t pin_VCC; pin_t pin_GND;
} chip_state_t;

static void update_gate(pin_t pin_a, pin_t pin_b, pin_t pin_y) {
  uint32_t val_a = pin_read(pin_a);
  uint32_t val_b = pin_read(pin_b);

  // AND Logic: Output is HIGH (1) only if both inputs are HIGH (1)
  uint32_t result = (val_a && val_b);

  pin_write(pin_y, result);
}

void chip_pin_change(void *user_data, pin_t pin, uint32_t value) {
  chip_state_t *chip = (chip_state_t *)user_data;
  update_gate(chip->pin_1A, chip->pin_1B, chip->pin_1Y);
  update_gate(chip->pin_2A, chip->pin_2B, chip->pin_2Y);
  update_gate(chip->pin_3A, chip->pin_3B, chip->pin_3Y);
  update_gate(chip->pin_4A, chip->pin_4B, chip->pin_4Y);
}

void chip_init() {
  chip_state_t *chip = malloc(sizeof(chip_state_t));

  // Initialize Inputs with Pull-ups for stability
  chip->pin_1A = pin_init("1A", INPUT_PULLUP);
  chip->pin_1B = pin_init("1B", INPUT_PULLUP);
  chip->pin_2A = pin_init("2A", INPUT_PULLUP);
  chip->pin_2B = pin_init("2B", INPUT_PULLUP);
  chip->pin_3A = pin_init("3A", INPUT_PULLUP);
  chip->pin_3B = pin_init("3B", INPUT_PULLUP);
  chip->pin_4A = pin_init("4A", INPUT_PULLUP);
  chip->pin_4B = pin_init("4B", INPUT_PULLUP);

  // Initialize Outputs
  chip->pin_1Y = pin_init("1Y", OUTPUT);
  chip->pin_2Y = pin_init("2Y", OUTPUT);
  chip->pin_3Y = pin_init("3Y", OUTPUT);
  chip->pin_4Y = pin_init("4Y", OUTPUT);
  
  chip->pin_VCC = pin_init("VCC", INPUT); 
  chip->pin_GND = pin_init("GND", INPUT);

  const pin_watch_config_t watch_config = {
    .edge = BOTH,
    .pin_change = chip_pin_change,
    .user_data = chip,
  };

  pin_watch(chip->pin_1A, &watch_config);
  pin_watch(chip->pin_1B, &watch_config);
  pin_watch(chip->pin_2A, &watch_config);
  pin_watch(chip->pin_2B, &watch_config);
  pin_watch(chip->pin_3A, &watch_config);
  pin_watch(chip->pin_3B, &watch_config);
  pin_watch(chip->pin_4A, &watch_config);
  pin_watch(chip->pin_4B, &watch_config);

  chip_pin_change(chip, 0, 0); 
  printf("74LS08 Custom Chip Initialized!\n");
}