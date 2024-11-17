#pragma once

struct DoubleBuffer {
  uint8_t *_back;
  uint8_t *_front;
  size_t _pos = 0;
  size_t _size;

  volatile bool _front_full;


  DoubleBuffer(uint size)
    : _front_full(true),
      _size(size) {
    this->_back = (uint8_t *)malloc(size);
    this->_front = (uint8_t *)malloc(size);
    this->clear(false);
  }

  ~DoubleBuffer() {
    free(this->_back);
    free(this->_front);
  }

  void swap() {
    auto tmp = this->_front;
    this->_front = this->_back;
    this->_back = tmp;
  }

  const uint8_t *get_front() const {
    return this->_front;
  }

  const uint8_t *get_back() const {
    return this->_back;
  }

  void swap_if_ready() {
    if (this->_front_full) {
      this->swap();
      this->_front_full = false;
    }
  }

  void writec(uint8_t c) {
    this->_back[this->_pos++] = c;
    if (this->_pos >= this->_size) {
      this->_pos = 0;
      this->_front_full = true;
      while (this->_front_full) {
        // wait for the front to be unlocked
      }
    }
  }

  void write(uint8_t *buf, size_t sz) {
    while (sz--) {
      this->writec(*(buf++));
    }
  }

  void clear(bool preserve_front = true) {
    memset(this->_back, 0, this->_size);
    this->_front_full = false;
    this->_pos = 0;
    if (!preserve_front) {
      memset(this->_front, 0, this->_size);
    }
  }
};
