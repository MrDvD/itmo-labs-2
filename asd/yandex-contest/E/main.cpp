#include <iostream>
#include <vector>

int count_cows(const std::vector<long>& arr, int n, long dist) {
  int count = 1;
  long last = arr[0];
  for (int i = 1; i < n; i++) {
    if (std::abs(last - arr[i]) >= dist) {
      last = arr[i];
      count++;
    }
  }
  return count;
}

long bin_search(const std::vector<long>& arr, int n, int k) {
  if (n < 1) { // assertion
    return -1;
  }
  long l = 0, r = arr[n - 1] - arr[0];
  while (l + 1 < r) {
    long mid = l + (r - l) / 2;
    if (count_cows(arr, n, mid) < k) {
      r = mid - 1;
    } else {
      l = mid;
    }
  }
  if (count_cows(arr, n, r) >= k) {
    return r;
  }
  return l;
}

int main() {
  int N, K;
  std::cin >> N >> K;
  std::vector<long> arr;
  arr.reserve(N);
  for (int i = 0; i < N; i++) {
    long item;
    std::cin >> item;
    arr.push_back(item);
  }
  std::cout << bin_search(arr, N, K);
  return 0;
}