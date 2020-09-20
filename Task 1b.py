from queue import Queue, PriorityQueue
from itertools import count


class Node:
    def __init__(self, state, goal_state, is_h1, parent=None):
        self.state = state
        self.goal_state = goal_state
        self.parent = parent
        self.is_h1 = is_h1

        if not parent:
            self.level = 0
        else:
            self.level = parent.level + 1


        # self.h1 = sum([0 if self.state[i] == self.goal_state[i] else 1
        #                for i in range(1, len(self.state))])
        if is_h1:
            # Heuristic function: Number of misplaced tiles
            count = 0
            for tile_value, goal_tile_value in zip(self.state, self.goal_state):
                if tile_value != goal_tile_value:
                    count += 1

            self.h1 = count
            self.f = self.level + self.h1
        else:
            # Heuristic function: Sum of Manhattan distances
            horizontal_distance = sum(abs((self.state.index(i) % 3) - (self.goal_state.index(i) % 3))
                                      for i in range(1, len(self.state)))
            vertical_distance = sum(abs((self.state.index(i) // 3) - (self.goal_state.index(i) // 3))
                                    for i in range(1, len(self.state)))
            self.h2 = horizontal_distance + vertical_distance
            # Total costs
            self.f = self.level + self.h2

    def __eq__(self, other):
        if not isinstance(other, Node):
            return TypeError()
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(self.state))

    def move(self, start, des):
        new_state = self.state[:]
        new_state[start], new_state[des] = new_state[des], new_state[start]
        new_node = Node(new_state, self.goal_state, self.is_h1, parent=self)
        return new_node

    def get_next_moves(self):
        next_nodes = []
        state = self.state[:]
        pos = state.index(0)

        # If position in the left column
        if pos % 3 == 0:
            next_nodes.append(self.move(pos, pos + 1))
        # Position of zero in the middle column
        elif pos % 3 == 1:
            next_nodes.append(self.move(pos, pos + 1))
            next_nodes.append(self.move(pos, pos - 1))
        # Position of zero in the right column
        else:
            next_nodes.append(self.move(pos, pos - 1))

        # If position in the upper row
        if pos // 3 == 0:
            next_nodes.append(self.move(pos, pos + 3))
        # If position in the middle row
        elif pos // 3 == 1:
            next_nodes.append(self.move(pos, pos + 3))
            next_nodes.append(self.move(pos, pos - 3))
        # If position in the lower row
        else:
            next_nodes.append(self.move(pos, pos - 3))

        return next_nodes

    def is_winning(self):
        return self.state == self.goal_state


class AStarSolver:
    def __init__(self, start_state, goal_state, is_h1):
        self.start = Node(start_state, goal_state, is_h1)

    def astar_search(self):
        queue = PriorityQueue(maxsize=50000)
        unique = count()

        queue.put((self.start.f, next(unique), self.start))
        visited = set()
        n_nodes = 0

        while not queue.empty():

            # Get next node
            current = queue.get()[2]
            n_nodes += 1

            # If goal state, return number of nodes expanded and the node found
            if current.is_winning():
                return n_nodes, current

            if current not in visited:
                visited.add(current)
                next_moves = current.get_next_moves()

                # Go through children
                while next_moves:
                    child = next_moves.pop()
                    queue.put((child.f, next(unique), child))

        return n_nodes, None


def print_path(node):
    print(node.state)
    if node.parent:
        print("-->")
    else:
        return
    print_path(node.parent)


"""Task 1 a"""
# Initial state fo the game:
# 7 2 4
# 5 0 6
# 8 3 1
with open("initial_state.txt", "r") as file:
    # One line only
    line = file.readline().split()
    start_state = [int(i) for i in line]

# Goal state:
# 0 1 2
# 3 4 5
# 6 7 8

goal_state = [i for i in range(9)]
# Use heuristic function 1 or 2
is_h1 = True
solver = AStarSolver(start_state, goal_state, is_h1=is_h1)
total_moves, result = solver.astar_search()

if result:
    print_path(result)
    print(f"Number of moves: {total_moves}")

else:
    print("Solution not found")
