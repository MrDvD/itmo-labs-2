#include <cstddef>
#include <forward_list>
#include <functional>
#include <iostream>
#include <iterator>
#include <list>
#include <stdexcept>

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

namespace {
std::list<std::list<Sign>> GenerateList(const std::forward_list<Sign>& signs) {
  if (signs.begin() == signs.end()) {
    throw std::invalid_argument("forward list is empty");
  }
  std::list<std::list<Sign>> list = {{*signs.begin()}};
  for (auto i = ++signs.begin(); i != signs.end() && i->count != 0; i++) {
    if (list.back().front().count == i->count) {
      list.back().push_front(*i);
      continue;
    }
    list.push_back({*i});
  }
  return list;
}

void StepPillar(std::list<std::list<Sign>>& list) {
  // taking item from a pillar
  auto next_list = std::next(list.begin());
  auto top = list.begin()->begin();
  std::cout << top->type << " ";
  top->count--;
  // if pillar is the only one item
  if (next_list == list.end()) {
    if (top->count == 0) {
      list.pop_front();
    }
    return;
  }
  // if pillar has transformed into plain, extend next item
  if (next_list->front().count == top->count) {
    next_list->push_front(*top);
    list.pop_front();
  }
  // take item from next plain
  std::cout << next_list->back().type << " ";
  next_list->back().count--;
  const Sign hanging_sign = next_list->back();
  next_list->pop_back();
  // if hanging sign was the pillar
  if (next_list->empty()) {
    next_list = list.erase(next_list);
  } else {
    ++next_list;
  }
  if (hanging_sign.count == 0) {
    return;
  }
  // extend next plain, if possible
  if (next_list != list.end() && hanging_sign.count == next_list->front().count) {
    next_list->push_front(hanging_sign);
    // otherwise, create a new pillar
  } else {
    list.insert(next_list, {hanging_sign});
  }
}

void ProcessPlain(std::list<std::list<Sign>>& list) {
  auto next_list = std::next(list.begin());
  auto plain = list.begin();
  while (!plain->empty()) {
    std::cout << plain->back().type << " ";
    plain->back().count--;
    // if item is not gone yet
    if (plain->back().count > 0) {
      // extend next plain, if possible
      if (next_list != list.end() && plain->back().count == next_list->front().count) {
        next_list->push_front(plain->back());
        // otherwise, create a new pillar
      } else {
        next_list = list.insert(next_list, {plain->back()});
      }
    }
    plain->pop_back();
  }
  list.pop_front();
}
}  // namespace

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

  std::list<std::list<Sign>> list = {};
  try {
    list = GenerateList(signs);
  } catch (const std::invalid_argument& e) {
    std::cout << "Problem constraints are not met.";
    return 1;
  }
  signs.clear();

  while (!list.empty() && std::next(list.front().begin()) == list.front().end()) {
    StepPillar(list);
  }
  while (!list.empty()) {
    ProcessPlain(list);
  }
  return 0;
}