"""The following code is a modified version of search.py by aima and is being used for the purpose of 
assignment 2 issued by Oliver Schulte"""

"""imports can be found in the zip folder and references can be found at https://github.com/aimacode/aima-python"""

import sys
from collections import deque

from utils import *

import pytest

from search import *

import time


class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0


#THE FOLLOWING CODE IS WHERE THE CHANGE BEGINS!#

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def manhattan(self, node):

        ##A map of some kind needs to be setup otherwise it will not traverse and can mistake it for a member of a separate function attribute
        
        mhd = 0
        state = node.state
        board = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        stategoal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        #maximum = mhd.maxsize
        
        for i in range(len(state)):
            index_state[state[i]] = board[i]

    #(index_state[i][j] // 3  - index_goal[i][j] // 3)  + abs(index_state[i][j] % 3 - index_goal[i][j] % 3)
        for i in range(1, 9):
            for j in range(2):
                mhd += ( abs(stategoal[i][j] // 3 - index_state[i][j] // 3) + abs(stategoal[i][j] % 3 - index_state[i][j] % 3)) ##formula was wrong and adjusted it here
                #maximum = max(maximum, mhd)
        return mhd

    def maxfunction(self, node):

        mhd = 0
        state = node.state
        board = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        stategoal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}

        h = sum(s != g for (s, g) in zip(node.state, self.goal))
        
        for i in range(len(state)):
            index_state[state[i]] = board[i]

    #(index_state[i][j] // 3  - index_goal[i][j] // 3)  + abs(index_state[i][j] % 3 - index_goal[i][j] % 3)
        for i in range(1, 9):
            for j in range(2):
                mhd += ( abs(stategoal[i][j] // 3 - index_state[i][j] // 3) + abs(stategoal[i][j] % 3 - index_state[i][j] % 3)) ##formula was wrong and adjusted it here
                maximum = max(h, mhd)
        return maximum

       

    
# ______________________________________________________________________________

#This times the A* misplaced

def f():
   start_time = time.time()

   result = astar_search(eight_puzzle, None, True)

   print("Total length (tiles moved): ",result.path_cost)

   # ... do something ...

   elapsed_time = time.time() - start_time

   print(f'elapsed time (in seconds): {elapsed_time}s')


# ______________________________________________________________________________

#This times the A* manhattan

def f1():

   start_time = time.time()

   result1 = astar_search(eight_puzzle, eight_puzzle.manhattan, True)

   print("Total length (tiles moved): ",result1.path_cost)

   elapsed_time = time.time() - start_time

   print(f'elapsed time (in seconds): {elapsed_time}s')

#This time the A* max of manhattan and misplaced

def f2():

    start_time = time.time()

    result2 = astar_search(eight_puzzle, eight_puzzle.maxfunction, True)

    print("Total length (tiles moved): ",result2.path_cost)

    elapsed_time = time.time() - start_time

    print(f'elapsed time (in seconds): {elapsed_time}s')

   
#Make a function to define permutations

#This permutation function was inspired by stackoverflow 
#and was used to process a single line of code. Alternatively could have used
#itertools instead.

def perm(x):
    if len(x) <= 1:
         yield x  #Rather then returning, use yield as it allows the value processed to retain itself to continue from where it left off in the function
    
    else:
        for y in perm(x[1:]):
            for index in range(len(x)):
                yield y[:index] + x[0:1] + y[index:]
            

def make_rand_8puzzle():
    
    lst1 = perm([0,1,2,3,4,5,6,7,8]) #The one line it was used which essentially creates random arrays within the given set of numbers

    array = list(lst1)

    state = tuple(random.choice(array)) ##Chooses among the arrays and turns it into a tuple

    #state = tuple(state0)

    #TRACE ARRAY BY PRINTING

    print(state)

    return state

def display(state):

    for index in range(0, 9):
        if(index % 3 == 0):
            print("")       
        if(state[index] != 0):
            print(state[index]," ", end ="")


        else:
            print("*  ", end = "")

if __name__=="__main__":

    #state= make_rand_8puzzle()
    #display(state)
    #eight_puzzle = EightPuzzle(state)
    #assert eight_puzzle.check_solvability((state))

#Test to see if generated initial generated array is solvable

    print("This is the default test that was required to show for assignment")

    state0 = [0, 3, 2, 1, 8, 7, 4, 5, 6]

    eight_puzzle = EightPuzzle((0, 3, 2, 1, 8, 7, 4, 5, 6))

    assert eight_puzzle.check_solvability((0, 3, 2, 1, 8, 7, 4, 5, 6))

    #state = [8, 2, 3, 4, 1, 6, 0, 7 ,5]

    print(state0)
    
    display((0, 3, 2, 1, 8, 7, 4, 5, 6))

    assert eight_puzzle.check_solvability((0, 3, 2, 1, 8, 7, 4, 5, 6))

    assert eight_puzzle.check_solvability(state0)

    assert eight_puzzle.goal_test((1, 2, 3, 4, 5, 6, 7, 8, 0))

    #maximum = max(eight_puzzle.h, eight_puzzle.manhattan)

    #print(maximum)

    print("\n")

    f()

    print("\n")

    f1()

    print("\n")
    
    f2()

    print("\nThis is the random test")

    state= make_rand_8puzzle()
    display(state)
    eight_puzzle = EightPuzzle(state)
    assert eight_puzzle.check_solvability((state))

    print("\n")

    f()

    print("\n")

    f1()

    print("\n")
    
    f2()


    #astar_search(eight_puzzle, manhattan, True)

    #astar_search(eight_puzzle, manhattan, True)

    #eight_puzzle.result((8, 2, 3, 4, 1, 6, 0, 7 ,5), DOWN)

    #eight_puzzle.__init__(state)

    #eight_puzzle.h(state[1])
    

  





