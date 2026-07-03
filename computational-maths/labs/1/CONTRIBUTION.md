# Разработка

Команда для компиляции тестов:
```bash
cd src &&
g++ main.cpp lib/lagrange.cpp lib/test.cpp -I. -Ilib -o main.out -std=c++20
```