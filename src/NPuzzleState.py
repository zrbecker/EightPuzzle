
import random

__all__ = ['NPuzzleState', 'RandomNPuzzleState']


class NPuzzleState:
    def __init__(self, size, state=None, free=0):
        self.size = size
        self.state = state
        self.free = free

    def __eq__(self, other):
        return all((self.size == other.size,
                    self.state == other.state,
                    self.free == self.free))

    def __hash__(self):
        return hash((self.size, self.free, tuple(self.state)))

    def __str__(self):
        result = ''
        for row in range(self.size):
            for col in range(self.size):
                result += '%4d' % (self.state[row * self.size + col])
            result += '\n'
        return result

    def valid_moves(self):
        index = self.state.index(self.free)
        moves = []
        row = index // self.size
        col = index % self.size
        if row > 0:
            moves.append((row - 1, col, 'DOWN'))
        if row < self.size - 1:
            moves.append((row + 1, col, 'UP'))
        if col > 0:
            moves.append((row, col - 1, 'RIGHT'))
        if col < self.size - 1:
            moves.append((row, col + 1, 'LEFT'))
        return moves

    def do_action(self, row, col, action):
        if (row, col, action) in self.valid_moves():
            src = row * self.size + col
            if action == 'UP':
                dst = src - self.size
            elif action == 'DOWN':
                dst = src + self.size
            elif action == 'LEFT':
                dst = src - 1
            elif action == 'RIGHT':
                dst = src + 1
            new_state = self.state[:]
            new_state[src], new_state[dst] = new_state[dst], new_state[src]
            return NPuzzleState(self.size, new_state, self.free)
        else:
            return None

    def is_solved(self):
        return self.state == sorted(self.state)


def RandomNPuzzleState(size, free=0):
    puzzle = NPuzzleState(size, range(0, size ** 2), free)
    for _ in range(1000):
        action = random.choice(puzzle.valid_moves())
        puzzle = puzzle.do_action(*action)
    return puzzle


class NPuzzleGame:
    def __init__(self, size):
        self.state = RandomNPuzzleState(size, 0)

    def move(self, row, col, action):
        self.state = self.state.do_action(row, col, action)

    def game_loop(self):
        while not self.state.is_solved():
            print self.state
            try:
                row = int(raw_input('Row: '))
                col = int(raw_input('Col: '))
                action = raw_input('Action: ')
                print
            except KeyboardInterrupt:
                print
                break
            except:
                print 'Invalid entry. Try again.'
                continue
            if (row, col, action) in self.state.valid_moves():
                self.move(row, col, action)
            else:
                print 'Invalid action. Try again.'
        if self.state.is_solved():
            print 'Congrats, You win!'


if __name__ == '__main__':
    game = NPuzzleGame(3)
    game.game_loop()

