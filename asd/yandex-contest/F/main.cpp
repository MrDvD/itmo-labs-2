#include <algorithm>
#include <cstddef>
#include <iostream>
#include <iterator>
#include <string>
#include <string_view>
#include <vector>

int main() {
  std::vector<std::string> arr;
  std::string line;
  while (std::cin >> line) {
    arr.push_back(line);
  }
  std::sort(arr.begin(), arr.end(), [](const std::string_view& lsr, const std::string_view& rsr) {
    const std::size_t a_len = lsr.length();
    const std::size_t b_len = rsr.length();
    const std::size_t left = std::min(a_len, b_len);
    const std::size_t right = std::max(a_len, b_len);
    const auto* iter1 = lsr.begin();
    const auto* iter2 = rsr.begin();
    for (std::size_t _ = 0; _ < left; _++) {
      if (*iter1 != *iter2) {
        return *iter1 > *iter2;
      }
      iter1 = std::next(iter1);
      iter2 = std::next(iter2);
    }
    if (a_len == b_len) {
      return false;
    }
    if (a_len < b_len) {
      iter1 = rsr.begin();
    } else {
      iter2 = lsr.begin();
    }
    for (std::size_t _ = left; _ < right; _++) {
      if (*iter1 != *iter2) {
        return *iter1 > *iter2;
      }
      iter1 = std::next(iter1);
      iter2 = std::next(iter2);
    }
    if (a_len < b_len) {
      iter2 = lsr.begin();
    } else {
      iter1 = rsr.begin();
    }
    for (std::size_t _ = right; _ < left + right; _++) {
      if (*iter1 != *iter2) {
        return *iter1 > *iter2;
      }
      iter1 = std::next(iter1);
      iter2 = std::next(iter2);
    }
    return false;
  });
  for (const auto& str : arr) {
    std::cout << str;
  }
  std::cout << "\n";
  return 0;
}