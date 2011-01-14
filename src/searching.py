from collections import deque
from heapq import heappop, heappush


__all__ = ['Agent', 'Node', 'Solution']


class Agent(object):
    def breadth_search(self):
        closed = {}
        fringe = deque()
        fringe.append(Node(None, None, self.problem.init_state, 0))
        while fringe:
            node = fringe.popleft()
            if self.problem.isgoal(node.state):
                return node.solution()
            if self.graph:
                if node.state not in closed:
                    closed[node.state] = node.cost
                else:
                    continue
            for (action, state) in self.problem.successors(node.state):
                step_cost = self.problem.stepcost(node.state, action, state)
                fringe.append(Node(node, action, state, step_cost))

    def depth_search(self, max_depth=None):
        closed = {}
        fringe = deque()
        fringe.append(Node(None, None, self.problem.init_state, 0))
        while fringe:
            node = fringe.pop()
            if self.problem.isgoal(node.state):
                return node.solution()
            if self.graph:
                if node.state not in closed or node.cost < closed[node.state]:
                    closed[node.state] = node.cost
                else:
                    continue
            if max_depth is None or node.depth <= max_depth:
                for (action, state) in self.problem.successors(node.state):
                    step_cost = \
                        self.problem.stepcost(node.state, action, state)
                    fringe.append(Node(node, action, state, step_cost))

    def iterative_search(self):
        n = 0
        while 1:
            solution = self.depth_search(n)
            if solution is None:
                n += 1
            else:
                return solution

    def greedy_search(self):
        closed = {}
        fringe = []
        root = Node(None, None, self.problem.init_state, 0)
        heappush(fringe, (self.greedy_eval(root), root))
        while fringe:
            value, node = heappop(fringe)
            if self.problem.isgoal(node.state):
                return node.solution()
            if self.graph:
                if node.state not in closed or node.cost < closed[node.state]:
                    closed[node.state] = node.cost
                else:
                    continue
                for (action, state) in self.problem.successors(node.state):
                    step_cost = \
                        self.problem.stepcost(node.state, action, state)
                    newNode = Node(node, action, state, step_cost)
                    heappush(fringe, (self.greedy_eval(newNode), newNode))

    def astar_search(self, max_depth=None):
        closed = {}
        fringe = []
        root = Node(None, None, self.problem.init_state, 0)
        heappush(fringe, (self.astar_eval(root), root))
        while fringe:
            value, node = heappop(fringe)
            if self.problem.isgoal(node.state):
                return node.solution()
            if self.graph:
                if node.state not in closed or node.cost < closed[node.state]:
                    closed[node.state] = node.cost
                else:
                    continue
            if max_depth and node.depth >= max_depth:
                continue
            for (action, state) in self.problem.successors(node.state):
                step_cost = \
                    self.problem.stepcost(node.state, action, state)
                newNode = Node(node, action, state, step_cost)
                heappush(fringe, (self.astar_eval(newNode), newNode))

    def greedy_eval(self, node):
        return 0

    def astar_eval(self, node):
        return node.cost

    def __init__(self, problem, graph=True):
        self.problem = problem
        self.graph = graph


class Node(object):
    nodes_created = 0

    def __init__(self, parent, action, state, step_cost):
        Node.nodes_created += 1
        
        self.parent = parent
        self.state = state
        self.action = action
        if parent:
            self.cost = parent.cost + step_cost
            self.depth = parent.depth + 1
        else:
            self.cost = step_cost
            self.depth = 0

    def __lt__(self, other):
        """ Impemented because python 3 wants it for
        heappush and heappop.

        """
        return self.depth < other.depth

    def solution(self):
        """ Returns the cost of the solution, and a list
        of actions to execute the solution.

        """
        current_node = self
        actions = []
        while current_node.action != None:
            actions.append(current_node.action)
            current_node = current_node.parent
        actions.reverse()
        return Solution(current_node, actions, self.cost, self.depth)


class Solution(object):
    """ Contains init_state, a list of actions, and a cost
    
    """
    def __init__(self, init_state, actions, cost, depth):
        self.init_state = init_state
        self.actions = actions
        self.cost = cost
        self.depth = depth

    def __str__(self):
        result = 'Depth found: ' + str(self.depth) + '\n'
        result += 'Solution cost: ' + str(self.cost) + '\n\n'
        if self.actions:
            for action in self.actions:
                result += str(action) + ' '
        else:
            result += 'The task is already solved!'
        return result

