
from NPuzzleState import *
from searching import *

class NPuzzleProblem(object):
    def __init__(self, size=3, state=None):
        self.init_state = state
        if not self.init_state:
            self.init_state = RandomNPuzzleState(size)

    def successors(self, state):
        result = []
        for move in state.valid_moves():
            newstate = state.do_action(*move)
            result.append((move, newstate))
        return result

    def isgoal(self, state):
        return state.is_solved()

    def stepcost(self, prev, action, new):
        return 1

class NPuzzleAgent(Agent):
    def tiles_misplaced(self, node):
        """ Counts the tiles out of place """
        value = 0
        for index, number in enumerate(node.state.state):
            if index != number:
                value += 1
        return value

    def tiles_distance(self, node):
        value = 0
        for index, number in enumerate(node.state.state):
            x1 = index % node.state.size
            y1 = index // node.state.size
            x2 = number % node.state.size
            y2 = number // node.state.size
            value += abs(x2 - x1) + abs(y2 - y1)

        return value

    def astar_eval(self, node):
        """ Estimates the value of a given state. """
        return node.cost + self.tiles_distance(node)

    def greedy_eval(self, node):
        """ Estimates the value of a given state. """
        return  self.tiles_distance(node)