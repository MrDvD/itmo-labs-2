#include <algorithm>
#include <iostream>
#include <unordered_map>
#include <vector>

using letter = struct {
  char c;
  long v;
};

int main() {
  std::unordered_map<char, long> occur;
  char c;
  while (std::cin >> std::noskipws >> c && c != '\n') {
    occur[c] = occur.count(c) ? occur[c] + 1 : 1;
  }
  std::cin >> std::skipws;
  std::vector<letter> costs;
  costs.reserve(26);
  for (int i = 0; i < 26; i++) {
    letter l;
    l.c = 'a' + i;
    std::cin >> l.v;
    costs.push_back(l);
  }
  std::sort(costs.begin(), costs.end(), [](const letter& a, const letter& b) { return a.v > b.v; });
  std::string pair, rest;
  for (letter l : costs) {
    if (occur.count(l.c) == 0) {
      continue;
    }
    if (occur[l.c] > 1) {
      pair += l.c;
      for (int i = 0; i < occur[l.c] - 2; i++) {
        rest += l.c;
      }
      continue;
    }
    rest += l.c;
  }
  std::cout << pair << rest << std::string(pair.rbegin(), pair.rend());
  return 0;
}