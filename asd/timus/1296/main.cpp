#include <iostream>
#include <vector>

int main() {
  int N;
  std::cin >> N;
  std::vector<int> arr;
  std::vector<long long> prefix;
  prefix.push_back(0);
  for (int i = 0; i < N; i++) {
    arr.push_back(0);
    prefix.push_back(0);
  }
  for (int i = 0; i < N; i++) {
    std::cin >> arr[i];
    prefix[i + 1] = prefix[i] + arr[i];
  }
  long long ans = 0;
  for (int i = 1; i <= N; i++) {
    for (int j = i; j <= N; j++) {
      long long curr = prefix[j] - prefix[i - 1];
      if (curr > ans) {
        ans = curr;
      }
    }
  }
  std::cout << ans;
  return 0;
}