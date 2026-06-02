//===----------------------------------------------------------------------===//
//
//                         BusTub
//
// count_min_sketch.cpp
//
// Identification: src/primer/count_min_sketch.cpp
//
// Copyright (c) 2015-2025, Carnegie Mellon University Database Group
//
//===----------------------------------------------------------------------===//

#include "primer/count_min_sketch.h"

#include <algorithm>
#include <limits>
#include <stdexcept>
#include <string>

namespace bustub {

/**
 * Constructor for the count-min sketch.
 *
 * @param width The width of the sketch matrix.
 * @param depth The depth of the sketch matrix.
 * @throws std::invalid_argument if width or depth are zero.
 */
template <typename KeyType>
CountMinSketch<KeyType>::CountMinSketch(uint32_t width, uint32_t depth) : width_(width), depth_(depth), row_locks_(depth) {
  /** @TODO(student) Implement this function! */
  if (width == 0 || depth == 0) {
    throw std::invalid_argument("invalid width / depth");
  }

  table_ = std::vector<std::vector<uint32_t>>(depth_, std::vector<uint32_t>(width_, 0));

  /** @spring2026 PLEASE DO NOT MODIFY THE FOLLOWING */
  // Initialize seeded hash functions
  hash_functions_.reserve(depth_);
  for (size_t i = 0; i < depth_; i++) {
    hash_functions_.push_back(this->HashFunction(i));
  }
}

template <typename KeyType>
CountMinSketch<KeyType>::CountMinSketch(CountMinSketch &&other) noexcept : width_(other.width_), depth_(other.depth_), row_locks_(other.depth_) {
  /** @TODO(student) Implement this function! */
  table_ = std::move(other.table_);
  hash_functions_ = std::move(other.hash_functions_);
}

template <typename KeyType>
auto CountMinSketch<KeyType>::operator=(CountMinSketch &&other) noexcept -> CountMinSketch & {
  if (this != &other) {
    width_ = other.width_;
    depth_ = other.depth_;
    row_locks_ = std::vector<std::mutex>(depth_);
    table_ = std::move(other.table_);
    hash_functions_ = std::move(other.hash_functions_);
  }

  return *this;
}

template <typename KeyType>
void CountMinSketch<KeyType>::Insert(const KeyType &item) {
  /** @TODO(student) Implement this function! */
  

  for (uint32_t i = 0; i < depth_; i++) {
    size_t col = hash_functions_[i](item);
    std::lock_guard<std::mutex> lock(row_locks_[i]);
    table_[i][col]++;
  }
}

template <typename KeyType>
void CountMinSketch<KeyType>::Merge(const CountMinSketch<KeyType> &other) {
  if (width_ != other.width_ || depth_ != other.depth_) {
    throw std::invalid_argument("Incompatible CountMinSketch dimensions for merge.");
  }
  /** @TODO(student) Implement this function! */
  std::lock_guard<std::mutex> lock(mutex_);

  for (uint32_t i = 0; i < depth_; i++) {
    std::lock_guard<std::mutex> lock(row_locks_[i]);
    for (uint32_t j = 0; j < width_; j++) {
      table_[i][j] += other.table_[i][j];
    }
  }
}

template <typename KeyType>
auto CountMinSketch<KeyType>::Count(const KeyType &item) const -> uint32_t {
  

  uint32_t count = std::numeric_limits<uint32_t>::max();

  for (uint32_t i = 0; i < depth_; i++) {
    size_t col = hash_functions_[i](item);
    std::lock_guard<std::mutex> lock(row_locks_[i]);
    uint32_t value = table_[i][col];
    if (value < count) {
      count = value;
    }
  }

  return count;
}

template <typename KeyType>
void CountMinSketch<KeyType>::Clear() {
  /** @TODO(student) Implement this function! */
  std::lock_guard<std::mutex> lock(mutex_);

  for (uint32_t i = 0; i < depth_; i++) {
    std::lock_guard<std::mutex> lock(row_locks_[i]);
    for (uint32_t j = 0; j < width_; j++) {
      table_[i][j] = 0;
    }
  }
}

template <typename KeyType>
auto CountMinSketch<KeyType>::TopK(uint16_t k, const std::vector<KeyType> &candidates)
    -> std::vector<std::pair<KeyType, uint32_t>> {
  std::vector<std::pair<KeyType, uint32_t>> result;

  for (const auto &item : candidates) {
    result.emplace_back(item, Count(item));
  }

  std::sort(result.begin(), result.end(), [](const auto &a, const auto &b) {
    return a.second > b.second;
  });

  if (result.size() > k) {
    result.resize(k);
  }

  return result;
}

// Explicit instantiations for all types used in tests
template class CountMinSketch<std::string>;
template class CountMinSketch<int64_t>;  // For int64_t tests
template class CountMinSketch<int>;      // This covers both int and int32_t
}  // namespace bustub
