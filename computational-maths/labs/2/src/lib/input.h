#ifndef INPUT_H
#define INPUT_H

#include <cctype>
#include <filesystem>
#include <fstream>
#include <sstream>

#include "preamble.h"
#ifdef _WIN32
#include <direct.h>
#else
#include <unistd.h>
#endif

namespace fs = std::filesystem;

class InputModule {
private:
  static bool isDouble(const string& str) {
    if (str.empty())
      return false;

    string s = str;
    size_t start = s.find_first_not_of(" \t");
    if (start == string::npos) {
      return false;
    }
    size_t end = s.find_last_not_of(" \t");
    s = s.substr(start, end - start + 1);

    if (s.empty()) {
      return false;
    }

    bool decimalPoint = false;
    bool hasDigit = false;
    bool signAllowed = true;

    for (size_t i = 0; i < s.length(); i++) {
      char c = s[i];

      if (c == '+' || c == '-') {
        if (!signAllowed)
          return false;
        if (i + 1 >= s.length())
          return false;
        signAllowed = false;
      } else if (c == '.' || c == ',') {
        if (decimalPoint) {
          return false;
        }
        decimalPoint = true;
        signAllowed = false;
      } else if (isdigit(c)) {
        hasDigit = true;
        signAllowed = false;
      } else if (c == ' ' || c == '\t') {
        if (i > 0 && (s[i - 1] == '+' || s[i - 1] == '-'))
          return false;
        bool hasOnlySpaces = true;
        for (size_t j = i; j < s.length(); j++) {
          if (s[j] != ' ' && s[j] != '\t') {
            hasOnlySpaces = false;
            break;
          }
        }
        if (hasOnlySpaces)
          break;
        return false;
      } else {
        return false;
      }
    }

    return hasDigit;
  }

  static double parseDouble(const string& str) {
    string s = str;
    size_t start = s.find_first_not_of(" \t");
    size_t end = s.find_last_not_of(" \t");
    s = s.substr(start, end - start + 1);

    size_t commaPos = s.find(',');
    if (commaPos != string::npos) {
      s[commaPos] = '.';
    }

    return stod(s);
  }

public:
  static int getDimension(const string& source = "console") {
    int n = -1;
    string input;
    bool valid = false;

    while (!valid) {
      cout << "Enter system dimension (n > 0): ";

      if (source == "console") {
        getline(cin, input);
      }

      bool isNumber = true;
      for (char c : input) {
        if (!isdigit(c) && c != '-' && c != '+') {
          isNumber = false;
          break;
        }
      }

      if (!isNumber || input.empty()) {
        cerr << "Error: Invalid input! Please enter a positive integer." << endl;
        continue;
      }

      try {
        n = stoi(input);
        if (n <= 0) {
          cerr << "Error: Dimension must be positive! Please enter n > 0." << endl;
        } else if (n > 100) {
          cerr << "Warning: Large dimension may cause performance issues. Continue? (y/n): ";
          string choice;
          getline(cin, choice);
          if (choice == "y" || choice == "Y") {
            valid = true;
          }
        } else {
          valid = true;
        }
      } catch (...) {
        cerr << "Error: Invalid dimension! Please enter a valid integer." << endl;
      }
    }

    return n;
  }

  static vector<vector<double>> readMatrixFromConsole(int n) {
    vector<vector<double>> A(n, vector<double>(n, 0.0));
    vector<double> b(n, 0.0);

    cout << "\nEnter matrix A (" << n << "x" << n << "):" << endl;
    cout << "Format: " << n << " numbers per row, space-separated" << endl;

    for (int i = 0; i < n; i++) {
      bool rowValid = false;
      while (!rowValid) {
        cout << "Row " << i + 1 << ": ";
        string line;
        getline(cin, line);

        vector<string> tokens;
        stringstream ss(line);
        string token;
        while (ss >> token) {
          tokens.push_back(token);
        }

        if (tokens.size() != n) {
          cerr << "Error: Expected " << n << " numbers, got " << tokens.size()
               << ". Please re-enter row " << i + 1 << ":" << endl;
          continue;
        }

        bool rowValidNumbers = true;
        for (int j = 0; j < n; j++) {
          if (!isDouble(tokens[j])) {
            cerr << "Error: Invalid number '" << tokens[j] << "' at position " << j + 1
                 << " in row " << i + 1 << endl;
            rowValidNumbers = false;
            break;
          }
        }

        if (!rowValidNumbers) {
          continue;
        }

        for (int j = 0; j < n; j++) {
          A[i][j] = parseDouble(tokens[j]);
        }
        rowValid = true;
      }
    }

    cout << "\nEnter RHS vector b (" << n << " elements):" << endl;
    for (int i = 0; i < n; i++) {
      bool elementValid = false;
      while (!elementValid) {
        cout << "b[" << i + 1 << "]: ";
        string input;
        getline(cin, input);

        if (!isDouble(input)) {
          cerr << "Error: Invalid number! Please enter a valid number." << endl;
          continue;
        }

        b[i] = parseDouble(input);
        elementValid = true;
      }
    }

    vector<vector<double>> augmented = A;
    for (int i = 0; i < n; i++) {
      augmented[i].push_back(b[i]);
    }

    return augmented;
  }

  static vector<vector<double>> readMatrixFromFile(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) {
      cerr << "Error: Cannot open file '" << filename << "'" << endl;
      return {};
    }

    int n;
    file >> n;

    if (file.fail() || n <= 0) {
      cerr << "Error: Invalid dimension in file!" << endl;
      return {};
    }

    vector<vector<double>> augmented(n, vector<double>(n + 1, 0.0));

    for (int i = 0; i < n; i++) {
      for (int j = 0; j <= n; j++) {
        if (!(file >> augmented[i][j])) {
          cerr << "Error: Not enough numbers in matrix at row " << i + 1 << endl;
          return {};
        }
      }
    }

    double extra;
    if (file >> extra) {
      cerr << "Warning: Extra data found in file after reading all required numbers." << endl;
    }

    file.close();
    return augmented;
  }

  static int getInputSource() {
    string choice;
    while (true) {
      cout << "### INPUT SOURCE SELECTION" << endl;
      cout << "1. Console input" << endl;
      cout << "2. File input" << endl;
      cout << "3. Generate random system" << endl;
      cout << "Choose option (1-3): ";

      if (!getline(cin, choice)) {
        cerr << "\nError: End of input detected. Exiting." << endl;
        exit(1);
      }

      if (choice.empty()) {
        cerr << "Error: No input provided!" << endl;
        continue;
      }

      if (choice == "1") {
        return 1;
      }
      if (choice == "2") {
        return 2;
      }
      if (choice == "3") {
        return 3;
      }

      cerr << "Error: Invalid choice '" << choice << "'!" << endl;
    }
  }

  static string getFilename() {
    string filename;

    while (true) {
      cout << "Enter filename: ";

      if (!getline(cin, filename)) {
        cerr << "\nError: End of input detected. Exiting." << endl;
        exit(1);
      }

      if (filename.empty()) {
        cerr << "Error: Filename cannot be empty!" << endl;
        continue;
      }

      if (fs::exists(filename) && fs::is_regular_file(filename)) {
        return filename;
      }

      fs::path testPath = fs::path("tests") / filename;
      if (fs::exists(testPath) && fs::is_regular_file(testPath)) {
        cout << "Found file in 'tests/' directory: " << testPath << endl;
        return testPath.string();
      }

      cerr << "Error: File '" << filename << "' not found in 'tests/' subdirectory!" << endl;
    }
  }
};

#endif