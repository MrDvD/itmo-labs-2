#include <iostream>

int main() {
  int N;
  std::cin >> N;
  for (int i = 0; i < N; i++) {
    std::string curr;
    std::cin >> curr;
    std::string ans;
    int currL = curr.length();
    if (currL % 2 || curr.substr(0, currL / 2) != curr.substr(currL / 2, currL)) {
      ans = "NO";
    } else {
      ans = "YES";
    }
    std::cout << ans << std::endl;
  }
  return 0;
}