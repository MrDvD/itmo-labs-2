#include <iostream>
#include <vector>

void fill_options(std::vector<int>& options) {
  for (int o : options) {
    options.push_back(o << 1 | 1);
    options.push_back(o << 1);
  }
}

int main() {
  int N;
  std::cin >> N;
  std::vector<int> arr;
  for (int i = 0; i < N; i++) {
    int item;
    std::cin >> item;
    arr.push_back(item);
  }
  std::vector<int> opts = {0, 1};
  for (int i = 0; i < N - 1; i++) {
    fill_options(opts);
  }
  long ans = 2000000;
  for (int o : opts) {
    long sum1 = 0, sum2 = 0, curr;
    for (int i = 0; i < N; i++) {
      if (o >> i & 1) {
        sum1 += arr[i];
      } else {
        sum2 += arr[i];
      }
    }
    curr = abs(sum2 - sum1);
    if (curr < ans) {
      ans = curr;
    }
  }
  std::cout << ans;
  return 0;
}