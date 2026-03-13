from typing import List, Tuple
import heapq
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import copy
import sys


class MazeSolver:

    @staticmethod
    def get_adjacent_cells(x: int, y: int, grid: List[List[str]]) -> List[Tuple[int, int]]:
        """Retrieve valid neighboring cells in clockwise order: Up, Right, Bottom, Bottom-Right, Left, Top-Left"""
        neighbors = []
        rows, cols = len(grid), len(grid[0])
        # Clockwise order: Up, Right, Bottom, Bottom-Right (Diagonal), Left, Top-Left (Diagonal)
        directions = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != '-1':
                neighbors.append((nx, ny))
        return neighbors

    @staticmethod
    def locate_start_and_target(grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Locate the start ('S') and target ('T') positions in the grid"""
        start = target = None
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j].lower() == 's':
                    start = (i, j)
                elif grid[i][j].lower() == 't':
                    target = (i, j)
        return start, target

    @staticmethod
    def calculate_manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Compute Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def trace_visited_path(grid: List[List[str]], visited: List[Tuple[int, int]], start: Tuple[int, int], target: Tuple[int, int]) -> List[List[str]]:
        grid_copy = copy.deepcopy(grid)
        step = 1
        for x, y in visited:
            if (x, y) != start and (x, y) != target:
                grid_copy[x][y] = str(step)
                step += 1
        return grid_copy

    @staticmethod
    def bfs(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        """Breadth-First Search implementation"""
        start, target = MazeSolver.locate_start_and_target(grid)
        if not start or not target:
            return -1, grid

        queue = deque([(start, [start])])
        visited = set()
        exploration_order = []

        while queue:
            (x, y), path = queue.popleft()
            exploration_order.append((x, y))

            if (x, y) == target:
                return 1, MazeSolver.trace_visited_path(grid, exploration_order, start, target)

            for nx, ny in MazeSolver.get_adjacent_cells(x, y, grid):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return -1, grid

    @staticmethod
    def dfs(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        """Depth-First Search implementation"""
        start, target = MazeSolver.locate_start_and_target(grid)
        if not start or not target:
            return -1, grid

        stack = [(start, [start])]
        visited = set()
        exploration_order = []

        while stack:
            (x, y), path = stack.pop()
            exploration_order.append((x, y))

            if (x, y) == target:
                return 1, MazeSolver.trace_visited_path(grid, exploration_order, start, target)

            for nx, ny in MazeSolver.get_adjacent_cells(x, y, grid):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append(((nx, ny), path + [(nx, ny)]))

        return -1, grid

    @staticmethod
    def ucs(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        """Uniform Cost Search implementation"""
        start, target = MazeSolver.locate_start_and_target(grid)
        if not start or not target:
            return -1, grid

        pq = [(0, start, [start])]
        visited = set()
        exploration_order = []

        while pq:
            cost, (x, y), path = heapq.heappop(pq)
            exploration_order.append((x, y))

            if (x, y) == target:
                return 1, MazeSolver.trace_visited_path(grid, exploration_order, start, target)

            for nx, ny in MazeSolver.get_adjacent_cells(x, y, grid):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    heapq.heappush(pq, (cost + 1, (nx, ny), path + [(nx, ny)]))

        return -1, grid

    @staticmethod
    def dls(grid: List[List[str]], depth_limit: int = 10) -> Tuple[int, List[List[str]]]:
        """Depth-Limited Search implementation"""
        start, target = MazeSolver.locate_start_and_target(grid)
        if not start or not target:
            return -1, grid

        exploration_order = []

        def dls_recursive(node, depth, visited_path):
            x, y = node
            exploration_order.append((x, y))

            if node == target:
                return True
            if depth <= 0:
                return False

            for nx, ny in MazeSolver.get_adjacent_cells(x, y, grid):
                if (nx, ny) not in visited_path:
                    visited_path.add((nx, ny))
                    if dls_recursive((nx, ny), depth - 1, visited_path):
                        return True
                    visited_path.remove((nx, ny))
            return False

        visited = {start}
        if dls_recursive(start, depth_limit, visited):
            return 1, MazeSolver.trace_visited_path(grid, exploration_order, start, target)
        return -1, grid

    @staticmethod
    def iddfs(grid: List[List[str]], max_depth: int = 50) -> Tuple[int, List[List[str]]]:
        """Iterative Deepening Depth-First Search implementation"""
        start, target = MazeSolver.locate_start_and_target(grid)
        if not start or not target:
            return -1, grid

        all_exploration_order = []

        for depth in range(max_depth):
            exploration_order = []

            def dls_recursive(node, depth_limit, visited_path):
                x, y = node
                exploration_order.append((x, y))

                if node == target:
                    return True
                if depth_limit <= 0:
                    return False

                for nx, ny in MazeSolver.get_adjacent_cells(x, y, grid):
                    if (nx, ny) not in visited_path:
                        visited_path.add((nx, ny))
                        if dls_recursive((nx, ny), depth_limit - 1, visited_path):
                            return True
                        visited_path.remove((nx, ny))
                return False

            visited = {start}
            if dls_recursive(start, depth, visited):
                all_exploration_order.extend(exploration_order)
                return 1, MazeSolver.trace_visited_path(grid, all_exploration_order, start, target)

            all_exploration_order.extend(exploration_order)

        return -1, grid

    @staticmethod
    def bidirectional_search(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
        """Bidirectional Search implementation"""
        start, target = MazeSolver.locate_start_and_target(grid)
        if not start or not target:
            return -1, grid
        if start == target:
            return 1, grid

        forward_queue = deque([start])
        forward_visited = {start: None}

        backward_queue = deque([target])
        backward_visited = {target: None}

        exploration_order = []

        while forward_queue and backward_queue:
            # Expand forward frontier
            if forward_queue:
                current = forward_queue.popleft()
                exploration_order.append(current)

                for neighbor in MazeSolver.get_adjacent_cells(current[0], current[1], grid):
                    if neighbor in backward_visited:
                        exploration_order.append(neighbor)
                        return 1, MazeSolver.trace_visited_path(grid, exploration_order, start, target)
                    if neighbor not in forward_visited:
                        forward_visited[neighbor] = current
                        forward_queue.append(neighbor)

            # Expand backward frontier
            if backward_queue:
                current = backward_queue.popleft()
                exploration_order.append(current)

                for neighbor in MazeSolver.get_adjacent_cells(current[0], current[1], grid):
                    if neighbor in forward_visited:
                        exploration_order.append(neighbor)
                        return 1, MazeSolver.trace_visited_path(grid, exploration_order, start, target)
                    if neighbor not in backward_visited:
                        backward_visited[neighbor] = current
                        backward_queue.append(neighbor)

        return -1, grid

    @staticmethod
    def visualize_grid(grid: List[List[str]], title: str, found: int):
        """Visualize the grid with obstacles, start, target, and visited path"""
        grid_array = np.zeros((len(grid), len(grid[0])))

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '-1':
                    grid_array[i, j] = -1  # Obstacle
                elif grid[i][j].lower() == 's':
                    grid_array[i, j] = -2  # Start
                elif grid[i][j].lower() == 't':
                    grid_array[i, j] = -3  # Target
                else:
                    try:
                        grid_array[i, j] = int(grid[i][j])  # Visited order
                    except ValueError:
                        grid_array[i, j] = 0  # Unvisited

        plt.figure(figsize=(10, 10))
        plt.imshow(grid_array, cmap='plasma', interpolation='nearest')

        # Add numbering to the grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid_array[i, j] >= 0:  # Only label path and unvisited cells
                    plt.text(j, i, grid[i][j], ha='center', va='center', color='white')

        plt.colorbar(label='Cell Types')
        plt.title(f"{title} (Path Found: {found})")
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.show()

    @staticmethod
    def read_grid_from_file(file_path: str) -> List[List[str]]:
        """Read and parse grid from input file"""
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file.readlines() if line.strip()]
            return [line.split() for line in lines]
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    @staticmethod
    def run_search_algorithm(grid: List[List[str]], algorithm_choice: str) -> Tuple[int, List[List[str]]]:
        """Run the specified search algorithm on the grid"""
        algorithms = {
            "BFS": MazeSolver.bfs,
            "DFS": MazeSolver.dfs,
            "UCS": MazeSolver.ucs,
            "DLS": MazeSolver.dls,
            "IDDFS": MazeSolver.iddfs,
            "BIDIRECTIONAL": MazeSolver.bidirectional_search
        }

        if algorithm_choice not in algorithms:
            print(f"Error: Invalid algorithm choice. Choose from: {', '.join(algorithms.keys())}")
            sys.exit(1)

        return algorithms[algorithm_choice](grid)

    @staticmethod
    def solve_maze(grid: List[List[str]], algorithm_choice: str = "BFS"):
        """Solve the maze using the specified algorithm"""
        found, exploration_grid = MazeSolver.run_search_algorithm(grid, algorithm_choice)

        print(f"\n{algorithm_choice} Results:")
        print(f"Path found: {found}")
        print("Final Grid State:")
        for row in exploration_grid:
            print('\t'.join(row))

        MazeSolver.visualize_grid(exploration_grid, f"{algorithm_choice} Exploration Order", found)
        return found, exploration_grid


if __name__ == "__main__":
    # 'S' = Start, 'T' = Target, '-1' = Obstacle/Wall, '0' = Open path
    grid = [
        ['S', '0', '0', '-1', '0', '0'],
        ['0', '-1', '0', '-1', '0', '0'],
        ['0', '0', '0', '0', '-1', '0'],
        ['-1', '-1', '0', '-1', '0', '0'],
        ['0', '0', '0', '0', '0', 'T']
    ]

    # Choose Algorithm choice from the following: BFS, DFS, UCS, DLS, IDDFS, BIDIRECTIONAL
    algorithm_choice = "BFS"
    MazeSolver.solve_maze(grid, algorithm_choice)
