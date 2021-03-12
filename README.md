# Heuristic-Search-Algorithms

This was an assignment during CMPT 310, which required us to compare heuristic search algorithms (more specifically A*). The comparison is validated based on time take to execute and solve an eight piece puzzle.

While some algorithms were provided via https://github.com/aimacode/aima-python , we were tasked to implement a function that could generate a random eight puzzle so that the test cases are more reliable. 

The spreadsheet keeps tab of the generated puzzle and the times for all algorithms.

In terms of speed and efficiency, it was safe to assume that A* manhattan takes the top. This is likely due to the fact that manhattan accounts for the distance needed for a tile to be placed in the correct position, rather than just simply detecting if the tile is misplaced.
