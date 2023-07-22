from collections import deque
import heapq

class Node:
    def __init__(self, data, level, move=None):
        self.data = data
        self.level = level
        self.move = move

    def find(self, x):
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if self.data[i][j] == x:
                    return i, j

    def generate_child(self, moves):
        x, y = self.find(0)
        children = []
        for move in moves:
            if move == "left" and y > 0:
                new_state = [row.copy() for row in self.data]
                new_state[x][y], new_state[x][y-1] = new_state[x][y-1], new_state[x][y]
                children.append(Node(new_state, self.level + 1, move))
            elif move == "up" and x > 0:
                new_state = [row.copy() for row in self.data]
                new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
                children.append(Node(new_state, self.level + 1, move))
            elif move == "right" and y < len(self.data) - 1:
                new_state = [row.copy() for row in self.data]
                new_state[x][y], new_state[x][y+1] = new_state[x][y+1], new_state[x][y]
                children.append(Node(new_state, self.level + 1, move))
            elif move == "down" and x < len(self.data) - 1:
                new_state = [row.copy() for row in self.data]
                new_state[x][y], new_state[x+1][y] = new_state[x+1][y], new_state[x][y]
                children.append(Node(new_state, self.level + 1, move))
        return children
    def __lt__(self, other):
        return self.level < other.level

def bfs(start, goal):
    moves = ["left", "up", "right", "down"]
    visited = set()
    queue = deque([Node(start, 0)])

    while queue:
        state = queue.popleft()
        if state.data == goal:
            return state.level, state

        if tuple(map(tuple, state.data)) in visited:
            continue
        visited.add(tuple(map(tuple, state.data)))

        for child in state.generate_child(moves):
            queue.append(child)

    return None, None

def dfs(start, goal):
    moves = ["left", "up", "right", "down"]
    visited = set()
    stack = [Node(start, 0)]

    while stack:
        state = stack.pop()
        if state.data == goal:
            return state.level, state

        if tuple(map(tuple, state.data)) in visited:
            continue
        visited.add(tuple(map(tuple, state.data)))

        for child in state.generate_child(moves):
            stack.append(child)

    return None, None

def dijkstra(start, goal):
    moves = ["left", "up", "right", "down"]
    visited = set()
    priority_queue = [(0, Node(start, 0))]

    while priority_queue:
        cost, state = heapq.heappop(priority_queue)
        if state.data == goal:
            return cost, state

        if tuple(map(tuple,    state.data)) in visited:
            continue
    visited.add(tuple(map(tuple, state.data)))

    for child in state.generate_child(moves):
        heapq.heappush(priority_queue, (cost + 1, child))

    return None, None

def main():
    print("Enter the start state matrix:")
    start = [list(map(int, input().split())) for _ in range(3)]
    print("Enter the goal state matrix:")
    goal = [list(map(int, input().split())) for _ in range(3)]
    bfs_cost, bfs_state = bfs(start, goal)
    dfs_cost, dfs_state = dfs(start, goal)
    dijkstra_cost, dijkstra_state = dijkstra(start, goal)

    min_cost = min(filter(None, [bfs_cost, dfs_cost, dijkstra_cost]))

    if bfs_cost == min_cost:
        print("BFS found the shortest path")
        final_state = bfs_state
    elif dfs_cost == min_cost:
        print("DFS found the shortest path")
        final_state = dfs_state
    else:
        print("Dijkstra found the shortest path")
        final_state = dijkstra_state

    print("Shortest path cost:", min_cost)
    print("Number of moves:", final_state.level)
    print("Shortest path:")
    for row in final_state.data:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    main()