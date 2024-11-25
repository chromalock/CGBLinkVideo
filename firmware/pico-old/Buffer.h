#pragma once

struct Buffer {
  virtual size_t size() const = 0;
  virtual const uint8_t *get_front() const = 0;
  virtual const uint8_t *get_back() const = 0;
  virtual void clear(bool preserve_front = true) = 0;
  virtual void swap_if_ready() = 0;
  virtual void write(uint8_t *buf, size_t sz) = 0;
};