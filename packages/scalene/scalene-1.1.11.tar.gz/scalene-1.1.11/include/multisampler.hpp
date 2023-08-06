#pragma once

#include <cmath>
#include <iostream>
#include <thread>
#include <unistd.h>

#include "mwc.h"

#define SAMPLER_DETERMINISTIC 0

template <int64_t SAMPLE_RATE, int Number>
class MultiSampler {
private:
  int64_t _next[Number];
#if !SAMPLER_DETERMINISTIC
  // MWC rng;
#endif

private:

  MWC& getRNG() {
    static MWC rng;
    return rng;
  }
  
public:
  MultiSampler()
  {
    for (auto i = 0; i < Number; i++) {
#if !SAMPLER_DETERMINISTIC
      _next[i] = getRNG().geometric(SAMPLE_PROBABILITY);
#else
      _next[i] = SAMPLE_RATE;
#endif
    }
  }
  
  inline ATTRIBUTE_ALWAYS_INLINE int64_t sample(int64_t sz, int index) {
    _next[index] -= sz;
    if (unlikely(_next[index] <= 0)) {
      return updateSample(sz, index);
    }
    return 0;
  }
  
private:

  int64_t updateSample(int64_t sz, int index) {
#if SAMPLER_DETERMINISTIC
    _next[index] = SAMPLE_RATE;
#else
    while (true) {
      _next[index] = getRNG().geometric(SAMPLE_PROBABILITY);
      if (_next[index] > 0) {
	break;
      }
    }
#endif
    if (sz >= SAMPLE_RATE) {
      return sz / SAMPLE_RATE + 1;
    } else {
      return 1;
    }
  }
  
  static constexpr double SAMPLE_PROBABILITY = (double) 1.0 / (double) SAMPLE_RATE;
};
