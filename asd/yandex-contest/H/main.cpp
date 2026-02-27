#include <algorithm>
#include <iostream>
#include <vector>

int main() {
  int n, k;
  std::cin >> n >> k;
  std::vector<int> arr;
  arr.reserve(n);
  long sum = 0;
  for (int i = 0; i < n; i++) {
    int item;
    std::cin >> item;
    arr.push_back(item);
    sum += item;
  }
  std::sort(arr.begin(), arr.end());
  for (int i = n - k; i >= 0; i -= k) {
    sum -= arr[i];
  }
  std::cout << sum;
  return 0;
}