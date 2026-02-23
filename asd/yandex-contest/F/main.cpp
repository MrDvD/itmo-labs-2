#include <algorithm>
#include <iostream>
#include <vector>

int main() {
  std::vector<std::string> arr;
  std::string line;
  while (std::cin >> line) {
    arr.push_back(line);
  }
  struct {
    bool operator()(std::string a, std::string b) const {
      return a + b > b + a;
    }
  } customLess;
  std::sort(arr.begin(), arr.end(), customLess);
  for (std::string& s : arr) {
    std::cout << s;
  }
  std::cout << "\n";
  return 0;
}