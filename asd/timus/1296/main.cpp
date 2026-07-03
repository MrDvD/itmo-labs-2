#include <iostream>

int main() {
  int N;
  std::cin >> N;
  long long ans = 0, curr = 0;
  for (int i = 0; i < N; i++) {
    int item;
    std::cin >> item;
    curr += item;
    if (curr < 0) {
      curr = 0;
    }
    if (curr > ans) {
      ans = curr;
    }
  }
  std::cout << ans;
  return 0;
}