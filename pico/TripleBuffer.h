#pragma once

#include "./Buffer.h"

struct TripleBuffer : public Buffer {
  uint8_t *_back;
  uint8_t *_front;
  uint8_t *_ready;
  bool _dirty;
  size_t _pos = 0;
  size_t _size;

  TripleBuffer(uint size)
    : _dirty(true),
      _size(size) {
    this->_back = (uint8_t *)malloc(size);
    this->_front = (uint8_t *)malloc(size);
    this->_ready = (uint8_t *)malloc(size);
    this->clear(false);
  }

  ~TripleBuffer() {
    free(this->_back);
    free(this->_front);
    free(this->_ready);
  }

  virtual size_t size() const {
    return this->_size;
  }


  virtual const uint8_t *get_front() const {
    return this->_front;
  }

  virtual const uint8_t *get_back() const {
    return this->_back;
  }

  virtual void swap_if_ready() {
    if (!this->_dirty) {
      auto tmp = this->_front;
      this->_front = this->_ready;
      this->_ready = tmp;

      this->_dirty = true;
    }
  }

  void writec(uint8_t c) {
    this->_back[this->_pos++] = c;
    if (this->_pos >= this->_size) {
      this->_pos = 0;

      auto tmp = this->_ready;
      this->_ready = this->_back;
      this->_back = tmp;

      this->_dirty = false;
    }
  }

  virtual void write(uint8_t *buf, size_t sz) {
    while (sz--) {
      this->writec(*(buf++));
    }
  }

  virtual void clear(bool preserve_front = true) {
    memset(this->_back, 0, this->_size);
    memset(this->_ready, 0, this->_size);
    this->_dirty = true;
    this->_pos = 0;
    if (!preserve_front) {
      memset(this->_front, 0, this->_size);
    }
  }
};
