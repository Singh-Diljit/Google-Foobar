'''
PROBLEM STATEMENT

From the scans of the nebula, you have found that it
is very flat and distributed in distinct patches, so
you can model it as a 2D grid. You find that the current
existence of gas in a cell of the grid is determined
exactly by its 4 nearby cells, specifically, (1) that cell,
(2) the cell below it, (3) the cell to the right of it, and
(4) the cell below and to the right of it. If, in the
current state, exactly 1 of those 4 cells in the 2x2
block has gas, then it will also have gas in the next state.
Otherwise, the cell will be empty in the next state.

Note that the resulting output will have 1 fewer row
and column, since the bottom and rightmost cells do
not have a cell below and to the right of them, respectively.

Write a function solution(g) where g is an array of array
of bools saying whether there is gas in each cell
(the current scan of the nebula), and return an int with
the number of possible previous states that could have
resulted in that grid after 1 time step. For instance,
if the function were given the current state c above,
it would deduce that the possible previous states were p
(given above) as well as its horizontal and vertical
reflections, and would return 4. The width of the grid will
be between 3 and 50 inclusive, and the height of the grid
will be between 3 and 9 inclusive.
'''