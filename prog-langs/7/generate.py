import random

COUNT = 10

with open('dots.txt', 'w') as f:
  for i in range(COUNT):
    f.write(f'{random.randint(-100, 100)} {random.randint(-100, 100)}')
    if i != COUNT - 1:
      f.write('\n')