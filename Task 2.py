from queue import Queue, LifoQueue


class Node:
    def __init__(self, left_cannibal, left_missionary, goal, boat_left, parent=None):
        # Assuming traveling from left of the river to the right
        # Cannibals and missionaries on the left of the river
        self.left_cannibal = left_cannibal
        self.left_missionary = left_missionary
        # Boat left?
        self.boat_left = boat_left
        self.parent = parent
        self.goal = goal

    def __eq__(self, other):
        if not isinstance(other, Node):
            return TypeError()
        # Equivalent states only when the numbers of cannibals and missionaries are equal and boat on the same side
        return ((self.left_cannibal == other.left_cannibal) and (self.left_missionary == other.left_missionary) and
                (self.boat_left == other.boat_left))

    def __hash__(self):
        return hash(tuple([self.left_cannibal, self.left_missionary, self.boat_left]))

    def get_next_moves(self):

        next_moves = set()

        for cannibal in range(3):
            for mis in range(3):
                # Cross the river with the boat
                # Number of people on the boat: 1 to 2
                if 1 <= mis + cannibal <= 2:
                    if self.boat_left:
                        left_cannibal = self.left_cannibal - cannibal
                        left_missionary = self.left_missionary - mis
                    else:
                        left_cannibal = self.left_cannibal + cannibal
                        left_missionary = self.left_missionary + mis
                    # If both sides cannibalibals are less than or equal to missionaryaries
                    # Append new nodes
                    if left_cannibal <= left_missionary and (3 - left_cannibal) <= (3 - left_missionary):
                        new_node = Node(left_cannibal, left_missionary, self.goal, not self.boat_left, parent=self)
                        next_moves.add(new_node)
                        # Else if no missionaryary on one side
                    elif left_missionary == 0 or 3 - left_missionary == 0:
                        new_node = Node(left_cannibal, left_missionary, self.goal, not self.boat_left, parent=self)
                        next_moves.add(new_node)
        return next_moves

    def is_goal(self):
        return self == self.goal


class Solver:
    def __init__(self):
        left_cannibal = 3
        left_missionary = 3
        # Goal state: No one on the left, boat on the right
        self.goal = Node(0, 0, None, boat_left=False)
        self.start = Node(left_cannibal, left_missionary, self.goal, boat_left=True)

    def bfs(self):
        queue = Queue()
        visited = set()

        queue.put(self.start)
        visited.add(self.start)

        # Number of nodes generated
        n_nodes = 0

        while queue:
            current = queue.get()
            n_nodes += 1

            # Check if current state is goal
            if current.is_goal():
                return n_nodes, current

            next_moves = current.get_next_moves()

            for child in next_moves:
                if child not in visited:
                    queue.put(child)
                    visited.add(child)

        return n_nodes, None


def print_solution(sol):
    stack = LifoQueue()
    node = sol
    while node.parent:
        stack.put(sol)
        node = node.parent

    step = 1
    while stack:
        node = stack.get()
        print(f"Step : {step}")
        print(f"Boat position at the beginning of the step: {'left' if node.boat_left else 'right'}")
        if node.boat_left:
            cannibal_on_boat = node.left_cannibal - node.parent.left_cannibal
            missionary_on_boat = node.left_missionary - node.parent.left_missionary
        else:
            # Count difference of people on the right to get the number of people on the boat
            cannibal_on_boat = - (node.left_cannibal - node.parent.left_cannibal)
            missionary_on_boat = - (node.left_missionary - node.parent.left_missionary)
        print(f"Number of cannibals on the boat: {cannibal_on_boat}")
        print(f"Number of missionary on the boat: {missionary_on_boat}")
        step += 1

# def print_solution(sol, step=0):
#     if sol:
#     print_solution(sol.parent, step+1)
#     print(f"Step : {step}")
#     print(f"Boat position at the beginning of the step: {'left' if sol.boat_left else 'right'}")
#     if sol.boat_left:
#         cannibal_on_boat = sol.left_cannibal - sol.parent.left_cannibal
#         missionary_on_boat = sol.left_missionary - sol.parent.left_missionary
#     else:
#         # Count difference of people on the right to get the number of people on the boat
#         cannibal_on_boat = - (sol.left_cannibal - sol.parent.left_cannibal)
#         missionary_on_boat = - (sol.left_missionary - sol.parent.left_missionary)
#     print(f"Number of cannibals on the boat: {cannibal_on_boat}")
#     print(f"Number of missionary on the boat: {missionary_on_boat}")

# Game starts

solver = Solver()
print("Game started")
print(f"Step : 0")
print(f"Boat position at the beginning of the step: Left")
print(f"Number of cannibals on the boat: 3")
print(f"Number of missionary on the boat: 3")

n_nodes, sol = solver.bfs()

# print_solution(sol)
print(n_nodes)