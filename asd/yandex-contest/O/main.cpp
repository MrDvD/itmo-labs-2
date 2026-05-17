#include <cstddef>
#include <iostream>
#include <list>
#include <unordered_map>
#include <vector>

struct Vertex {
  std::size_t color = 0;
  bool visited = false;
  std::vector<std::size_t> neighbours;
};

class Graph {
public:
  void AddEdge(std::size_t from_id, std::size_t to_id) {
    if (this->vertices_.count(from_id) == 0U) {
      this->vertices_[from_id] = {0, false, {}};
    }
    if (this->vertices_.count(to_id) == 0U) {
      this->vertices_[to_id] = {0, false, {}};
    }
    this->vertices_[from_id].neighbours.push_back(to_id);
    this->vertices_[to_id].neighbours.push_back(from_id);
  }

  static std::size_t SwitchColor(std::size_t from_color) {
    return from_color == 0 ? 1 : 0;
  }

  bool TryColor() {
    bool is_possible = true;
    for (std::size_t i = 1; i <= this->vertices_.size(); i++) {
      if (this->vertices_[i].visited) {
        continue;
      }
      std::list<std::size_t> to_visit = {i};
      while (!to_visit.empty()) {
        Vertex& top_vertex = this->vertices_[to_visit.front()];
        to_visit.pop_front();
        top_vertex.visited = true;
        for (const auto& neightbour : top_vertex.neighbours) {
          Vertex& neightbour_vertex = this->vertices_[neightbour];
          if (neightbour_vertex.visited && neightbour_vertex.color == top_vertex.color) {
            is_possible = false;
            break;
          }
          if (neightbour_vertex.visited) {
            continue;
          }
          neightbour_vertex.color = Graph::SwitchColor(top_vertex.color);
          to_visit.push_front(neightbour);
        }
      }
    }
    return is_possible;
  }

private:
  std::unordered_map<std::size_t, Vertex> vertices_;
};

int main() {
  std::size_t n_students = 0;
  std::size_t m_pairs = 0;
  std::cin >> n_students >> m_pairs;
  Graph graph;
  for (std::size_t i = 0; i < m_pairs; i++) {
    std::size_t from_id = 0;
    std::size_t to_id = 0;
    std::cin >> from_id >> to_id;
    graph.AddEdge(from_id, to_id);
  }
  std::cout << (graph.TryColor() ? "YES" : "NO");
  return 0;
}