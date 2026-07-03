#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <vector>

class Fraction {
public:
  Fraction(int num, int denum) : numerator_(num), denumerator_(denum) {
  }

  bool operator<(const Fraction& other) const {
    return this->numerator_ * other.denumerator_ < this->denumerator_ * other.numerator_;
  }

private:
  int64_t numerator_ = 1;
  int64_t denumerator_ = 1;
};

class Point {
public:
  int x = 0;
  int y = 0;
  std::size_t idx = 0;

  friend Fraction operator-(const Point& lpt, const Point& rpt) {
    return {rpt.y - lpt.y, rpt.x - lpt.x};
  }
};

namespace {
Point FindLeftmostPoint(const std::vector<Point>& array) {
  if (array.empty()) {
    throw std::invalid_argument("array is empty");
  }
  Point left_point = array[0];
  for (std::size_t i = 1; i < array.size(); i++) {
    if (array[i].x < left_point.x) {
      left_point = array[i];
    }
  }
  return left_point;
}
}  // namespace

int main() {
  std::size_t n_points = 0;
  std::cin >> n_points;

  std::vector<Point> points;
  points.reserve(n_points);
  for (std::size_t i = 0; i < n_points; i++) {
    Point curr_point;
    std::cin >> curr_point.x >> curr_point.y;
    curr_point.idx = i;
    points.push_back(curr_point);
  }

  if (points.size() == 2) {
    std::cout << 1 << " " << 2;
    return 0;
  }

  Point left_point = {};
  try {
    left_point = FindLeftmostPoint(points);
  } catch (const std::invalid_argument& e) {
    std::cout << "Problem constraints are not met.";
    return 1;
  }
  points.erase(std::next(points.begin(), static_cast<std::ptrdiff_t>(left_point.idx)));

  std::sort(points.begin(), points.end(), [left_point](const Point& lpt, const Point& rpt) {
    return (left_point - lpt) < (left_point - rpt);
  });
  std::cout << left_point.idx + 1 << " " << points[points.size() / 2].idx + 1;
  return 0;
}