#pragma once

struct SingleBuffer {
  uint8_t *_front;
  size_t _size;
  size_t _pos = 0;

  SingleBuffer(uint size):
      _size(size) {
    this->_front = (uint8_t *)malloc(size);
    this->clear(false);
  }

  ~SingleBuffer() {
    free(this->_front);
  }


  const uint8_t *get_front() const {
    return this->_front;
  }

  const uint8_t *get_back() const {
    return this->_front;
  }

  void swap_if_ready() {}

  void writec(uint8_t c) {
    this->_front[this->_pos++] = c;
    if (this->_pos >= this->_size) {
      this->_pos = 0;
    }
  }

  void write(uint8_t *buf, size_t sz) {
    while (sz--) {
      this->writec(*(buf++));
    }
  }

  void clear(bool preserve_front = true) {
    this->_pos = 0;
    if (!preserve_front) {
      memset(this->_front, 0, this->_size);
    }
  }
};
