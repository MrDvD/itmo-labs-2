#include <cstddef>
#include <forward_list>
#include <functional>
#include <iostream>

class Sign {
public:
  std::size_t count = 0;
  std::size_t type = 0;

  // use this instead of `bool operator>(const Sign& other) const { ... }`
  // otherwise i would have to define getters (POD vs Non-POD)
  friend bool operator>(const Sign& lsn, const Sign& rsn) {
    return lsn.count > rsn.count;
  }
};

int main() {
  std::size_t k_types = 1;
  std::cin >> k_types;
  std::forward_list<Sign> signs;
  for (std::size_t i = 0; i < k_types; i++) {
    Sign sign = {0, i + 1};
    std::cin >> sign.count;
    signs.push_front(sign);
  }
  signs.sort(std::greater<>());
  // 

  while (signs.begin() != signs.end()) {
    auto prev = signs.before_begin();
    for (auto i = signs.begin(); i != signs.end(); i++) {
      if (i->count > 0) {
        std::cout << i->type << " ";
        i->count--;
      }
      if (i->count == 0) {
        signs.erase_after(prev);
        break;
      }
      prev = i;
    }
  }
  return 0;
}