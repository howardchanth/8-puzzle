from queue import LifoQueue, Queue


class Node:
    def __init__(self, state, goal_state, parent=None):
        self.state = state
        self.goal_state = goal_state
        self.parent = parent

        if not parent:
            self.level = 0
        else:
            self.level = parent.level + 1

        # Heuristic function: Number of misplaced tiles
        self.h1 = sum(1 if self.state[i] == self.goal_state[i] else 0
                      for i in range(len(self.state)))

        # Heuristic function: Sum of Manhattan distances
        horizontal_distance = sum(abs((self.state.index(i) % 3) - (self.goal_state.index(i) % 3))
                                  for i in range(len(self.state)))
        vertical_distance = sum(abs((self.state.index(i) // 3) - (self.goal_state.index(i) // 3))
                                for i in range(len(self.state)))
        self.h2 = horizontal_distance + vertical_distance

    def __eq__(self, other):
        if not isinstance(other, Node):
            return TypeError()
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(self.state))

    def move(self, start, des):
        new_state = self.state[:]
        new_state[start], new_state[des] = new_state[des], new_state[start]
        new_node = Node(new_state, self.goal_state, parent=self)
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


class IDDFSSolver:
    def __init__(self, start_state, goal_state):

        self.start = Node(start_state, goal_state)

    # Depth-Limited Search
    def depth_limited_search(self, max_depth):
        stack = LifoQueue()
        visited = set()

        stack.put(self.start)
        visited.add(self.start)
        n_nodes = 0
        while True:
            if stack.empty():
                return n_nodes, None
            current = stack.get()
            n_nodes += 1

            # If winning state, return search results and number of nodes expanded for this depth
            if current.is_winning():
                return n_nodes, current

            if current.level < max_depth:
                next_moves = current.get_next_moves()
                while next_moves:
                    child = next_moves.pop()
                    if child not in visited:
                        stack.put(child)
                        visited.add(child)

    def iterative_deepening_dfs(self, max_nodes=1000000):
        print("Iterative Deepening Search")
        # Repeat depth-limit search until maximum nodes explored
        depth = 0
        total_moves = 0

        while True:
            n_nodes, result = self.depth_limited_search(depth)
            total_moves += n_nodes
            if result:
                return total_moves, result
            if n_nodes > max_nodes:
                return total_moves, None
            print(f"Depth level: {depth}")
            print(f"Number of nodes of depth {depth}: {n_nodes}")
            print(f"Total number of nodes expanded: {total_moves}")
            depth += 1


def print_path(node, step=0):
    def get_move_dir(node):
        pos = node.parent.state.index(0) - node.state.index(0)
        if pos == 3:
            return 'Up'
        elif pos == -3:
            return 'Down'
        elif pos == 1:
            return 'Right'
        else:
            return 'Left'
    if not node.parent:
        print(f"Number of moves:{step}")
        print("Path found. The path generated is (from goal to start):")
        return
    print_path(node.parent, step + 1)
    print(node.state)
    print(f"Move {get_move_dir(node)}")


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

solver = IDDFSSolver(start_state, goal_state)
total_moves, result = solver.iterative_deepening_dfs()

if result:
    print_path(result)
    print(f"Number of nodes generated: {total_moves}")

else:
    print("Solution not found")
