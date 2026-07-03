#include <algorithm>
#include <cstddef>
#include <iostream>
#include <set>
#include <vector>

namespace {
struct Point {
  std::size_t x;
  std::size_t y;

  bool operator<(const Point& other) const {
    if (x != other.x) {
      return x < other.x;
    }
    return y < other.y;
  }
};

void AddBounds(std::vector<Point>& arr, const std::size_t x_bound, const std::size_t y_bound) {
  for (std::size_t y_idx = 0; y_idx <= y_bound + 1; y_idx++) {
    for (const std::size_t x_idx : {static_cast<std::size_t>(0), x_bound + 1}) {
      arr.push_back({x_idx, y_idx});
    }
  }
  for (std::size_t x_idx = 1; x_idx < x_bound + 1; x_idx++) {
    for (const std::size_t y_idx : {static_cast<std::size_t>(0), y_bound + 1}) {
      arr.push_back({x_idx, y_idx});
    }
  }
}

bool SortByY(const Point& lpt, const Point& rpt) {
  if (lpt.y != rpt.y) {
    return lpt.y < rpt.y;
  }
  return lpt.x < rpt.x;
}
}  // namespace

int main() {
  std::size_t m_count = 0;
  std::size_t n_count = 0;
  std::size_t k_count = 0;
  std::cin >> m_count >> n_count >> k_count;

  std::vector<Point> black_points(k_count);
  black_points.reserve(k_count + 2 * (n_count + m_count + 2));
  for (std::size_t i = 0; i < k_count; i++) {
    std::cin >> black_points[i].x >> black_points[i].y;
  }
  AddBounds(black_points, m_count, n_count);

  std::size_t white_streaks = 0;
  std::set<Point> suspicious_points = {};
  std::sort(black_points.begin(), black_points.end());
  for (std::size_t i = 0; i < black_points.size() - 1; i++) {
    const Point& lpt = black_points[i];
    const Point& rpt = black_points[i + 1];
    if (lpt.x != rpt.x) {
      continue;
    }
    const auto diff = static_cast<std::ptrdiff_t>(rpt.y - lpt.y);
    if (diff == 1) {
      continue;
    }
    if (diff == 2) {
      suspicious_points.insert({lpt.x, lpt.y + 1});
      continue;
    }
    white_streaks++;
  }

  std::sort(black_points.begin(), black_points.end(), SortByY);
  for (std::size_t i = 0; i < black_points.size() - 1; i++) {
    const Point& lpt = black_points[i];
    const Point& rpt = black_points[i + 1];
    if (lpt.y != rpt.y) {
      continue;
    }
    const auto diff = static_cast<std::ptrdiff_t>(rpt.x - lpt.x);
    if (diff == 1) {
      continue;
    }
    if (diff == 2) {
      const Point sus_point = {lpt.x + 1, lpt.y};
      if (suspicious_points.count(sus_point) != 0U) {
        suspicious_points.erase(sus_point);
        white_streaks++;
      }
      continue;
    }
    white_streaks++;
  }
  std::cout << white_streaks;
  return 0;
}