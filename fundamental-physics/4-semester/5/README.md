To complie this, use the following command:

```bash
gfortran -std=f95 script.f90 -L/usr/local/pgplot -L/usr/X11/lib -lpgplot -lX11
```

Instruction for installation of pgplot is here: [link](https://guaix.fis.ucm.es/~ncl/howto/howto-pgplot)

### failed refactor attempt

I want to refactor my program like this: make history array to be dynamic (up to 100 steps max). Assume that history stuct has size param. Size never increases more than 100 steps. On each step forward we try to increase the size of an array till it reaches 100. Also we should keep all the used t_vals (it's history is more than just 100 steps, it grows from the beginning).

If i want to do step forward but size is already at 100, then i calculate new state from current data via verlet_step subroutine and insert it on the 100th place in array (the first element is dropped).

Speaking of step back: write verlet_back subroutine which recalculates the previous steps for the 1st index of array. And when we try to go back and the absolute time reaches 0, from now we start shrinking our array to the left till it's size reaches 1.