#include <iostream>
#include <vector>

int main() {
  int N;
  std::cin >> N;
  std::vector<int> arr;
  long total_sum = 0;
  for (int i = 0; i < N; i++) {
    int item;
    std::cin >> item;
    arr.push_back(item);
    total_sum += item;
  }
  std::vector<int> min_coins[2];
  int INF = N + 1;
  for (int j = 0; j < 2; j++) {
    std::vector<int> step;
    for (int i = 0; i <= total_sum; i++) {
      step.push_back(INF);
    }
    step[0] = 0;  // dp base
    min_coins[j] = step;
  }
  short curr_step_idx = 0, prev_step_idx = 1;
  for (int i = 1; i <= N; i++) {
    curr_step_idx ^= 1;
    prev_step_idx ^= 1;
    for (long cost = 0; cost <= total_sum; cost++) {
      int prev = min_coins[prev_step_idx][cost];
      long prev_cost = cost - arr[i - 1];
      int curr = prev_cost >= 0 ? min_coins[prev_step_idx][cost - arr[i - 1]] + 1 : INF;
      min_coins[curr_step_idx][cost] = prev <= curr ? prev : curr;
    }
  }
  long diff = total_sum;
  for (long cost = 0; cost < total_sum; cost++) {
    long curr_diff = abs(2 * cost - total_sum);
    if (min_coins[curr_step_idx][cost] != INF && curr_diff < diff) {
      diff = curr_diff;
    }
  }
  std::cout << diff;
  return 0;
}