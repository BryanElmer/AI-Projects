# CS3243: Intro to AI Project1

## Finding a Valid Path using Search Algorithms To Solve King's Maze Problem

Every instance of the chess board consists of obstacles, and enemy pieces that cannot be moved or captured. The goal of this problem is to move the king piece from a start position to any goal positions.

## The Four Search Algorithms used:
- **BFS**: Searches for a valid path from start position to goal position. The algorithm outputs the required moves, and number of nodes explored.
- **DFS**: Searches for a valid path from start position to goal position. The algorithm outputs the required moves, and number of nodes explored.
- **UCS**: Searches for a valid, optimal path from start position to goal position. The algorithm outputs the required moves, number of nodes explored, and the total path cost.
- **AStar**: Searches for a valid, optimal path from start position to goal position. The algorithm outputs the required moves, number of nodes explored, and the total path cost.

## Implementation Details:
- **BFS**:  
    - Follows best-first search algorithm with an early goal test
    - Frontier: queue
    - Keeps track of reached nodes
    - Only adds node to frontier if not explored or has lower cost than previously reached  

- **DFS**: 
    - Follows best-first search algorithm with an early goal test
    - Frontier: stack
    - Keeps track of reached nodes
    - Only adds node to frontier if not explored or has lower cost than previously reached.  

- **UCS**: 
    - Follows best-first search algorithm with a late goal test
    - Frontier: priority queue, where path cost becomes the priority attribute
    - Keeps track of reached nodes
    - Only adds node to frontier if not explored or has lower cost than previously reached 

- **AStar**: 
    - Follows best-first search algorithm with a late goal test
    - Frontier: priority queue, where path cost + heuristic value becomes the priority attribute
    - Heuristic: max((x1 - x2), abs(y1 - y2)), where (x1, y1) is the current position, and (x2, y2) is the nrearest goal state
    - Keeps track of reached nodes
    - Only adds node to frontier if not explored or has lower cost than previously reached