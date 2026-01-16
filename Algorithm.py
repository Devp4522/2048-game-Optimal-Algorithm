import numpy as np
import copy

class ExpectimaxAI:
    def __init__(self, depth=3):
        self.depth = depth
        self.directions = [-1, 1, -2, 2]  # UP, DOWN, LEFT, RIGHT
    
    def get_best_move(self, grid):
        best_move = None
        best_score = float('-inf')
        
        # Try all possible moves
        for direction in self.directions:
            grid_copy = copy.deepcopy(grid)
            moved = grid_copy.move(direction)
            
            # If the move is valid
            if moved:
                # Calculate the score for this move
                score = self.expectimax(grid_copy, 0, False)
                
                # Update best move if this move has a higher score
                if score > best_score:
                    best_score = score
                    best_move = direction
        
        return best_move


    def expectimax(self, grid, depth, is_max_turn):
        board = grid.get_board()
    
        # If I've reached the maximum depth
        if depth >= self.depth:
            return self.calculate_final_score(board)
        
        if is_max_turn:
            max_score = float('-inf')
            
            for direction in self.directions:
                grid_copy = copy.deepcopy(grid)
                moved = grid_copy.move(direction)
                
                if moved:
                    score = self.expectimax(grid_copy, depth + 1, False)
                    max_score = max(max_score, score)
            
            # If no valid moves, evaluate the board
            if max_score == float('-inf'):
                return self.calculate_final_score(board)
            
            return max_score
        else:
           
            empty_cells = []
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == 0:
                        empty_cells.append((i, j))
            
            if not empty_cells:
                return self.calculate_final_score(board)
            
            # Calculate the expected score for one random empty cell
            # (for performance reasons, I did't check all empty cells)
            i, j = empty_cells[0]
            
            # Spawn a 2 (90% chance)
            grid_copy_2 = copy.deepcopy(grid)
            grid_copy_2.get_board()[i][j] = 2
            score_2 = self.expectimax(grid_copy_2, depth + 1, True)
            
            # Spawn a 4 (10% chance)
            grid_copy_4 = copy.deepcopy(grid)
            grid_copy_4.get_board()[i][j] = 4
            score_4 = self.expectimax(grid_copy_4, depth + 1, True)
            
            # Calculate the expected score (weighted average)
            return 0.9 * score_2 + 0.1 * score_4


    def calculate_final_score(self, board):

        # taken from a research paper (weights of parameter)
        # Empty Cells (Prioritize flexibility)
        empty_cells = np.sum(board == 0)
        
        scores = [0, 0, 0, 0]
        # Calculate monotonicity for rows
        for i in range(len(board)):
            for j in range(len(board[0]) - 1):
                if board[i][j] > 0 and board[i][j+1] > 0:
                    if board[i][j] > board[i][j+1]:
                        scores[0] -= np.log2(board[i][j]) - np.log2(board[i][j+1])
                    else:
                        scores[1] -= np.log2(board[i][j+1]) - np.log2(board[i][j])
        
        # Calculate monotonicity for columns
        for j in range(len(board[0])):
            for i in range(len(board) - 1):
                if board[i][j] > 0 and board[i+1][j] > 0:
                    if board[i][j] > board[i+1][j]:
                        scores[2] -= np.log2(board[i][j]) - np.log2(board[i+1][j])
                    else:
                        scores[3] -= np.log2(board[i+1][j]) - np.log2(board[i][j])


        mono_score = max(scores)
        
        # 3. Smoothness
        smoothness = 0
        # Calculate smoothness for rows
        for i in range(len(board)):
            for j in range(len(board[0]) - 1):
                if board[i][j] > 0 and board[i][j+1] > 0:
                    smoothness -= abs(np.log2(board[i][j]) - np.log2(board[i][j+1]))
        
        # Calculate smoothness for columns
        for j in range(len(board[0])):
            for i in range(len(board) - 1):
                if board[i][j] > 0 and board[i+1][j] > 0:
                    smoothness -= abs(np.log2(board[i][j]) - np.log2(board[i+1][j]))
        
        # Gradient Weights (Snake pattern matrix)
        gradient_matrix = np.array([[15,14,13,12],
                                    [8,9,10,11],
                                    [7,6,5,4],
                                    [0,1,2,3]])
        gradient_score = np.sum(board * gradient_matrix)
        
        # Merge Potential (Immediate merge opportunities)
        merge_potential = 0
        for row in board:
            merge_potential += sum(1 for i in range(3) if row[i] == row[i+1] and row[i] != 0)
        for col in board.T:
            merge_potential += sum(1 for i in range(3) if col[i] == col[i+1] and col[i] != 0)
        
        # Clustering Penalty (Avoid fragmented tiles)
        cluster_penalty = 0
        for x in range(4):
            for y in range(4):
                if board[x,y] == 0: continue
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    if 0 <= x+dx <4 and 0 <= y+dy <4:
                        cluster_penalty += abs(board[x,y] - board[x+dx,y+dy])
        
        # Max Tile Position (Prefer corner placement)
        max_tile = np.max(board)
        max_pos = np.argmax(board)
        position_bonus = 100 if max_pos in [0,3,12,15] else 0  # Corner positions
        
        # Trapped Tile Penalty (Avoid stuck positions)
        trapped = 0
        for x in range(4):
            for y in range(4):
                if board[x,y] == 0: continue
                movable = False
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    if 0 <= x+dx <4 and 0 <= y+dy <4:
                        if board[x+dx,y+dy] in (0, board[x,y]):
                            movable = True
                            break
                if not movable: trapped += 1

        score = (
            450.0 * empty_cells + 
            15.0 * smoothness +
            10.0 * merge_potential +
            8.0 * gradient_score -
            5.0 * mono_score -
            2.5 * cluster_penalty -
            75.0 * trapped +
            30.0 * position_bonus +
            np.log2(max_tile + 1) * 150
        )
        
        return max(score, 0.1)

    def calculate_monotonicity(self, board):
        scores = [0, 0, 0, 0]
        
        # Calculate monotonicity for rows (left and right)
        for i in range(len(board)):
            for j in range(len(board[0]) - 1):
                if board[i][j] > 0 and board[i][j+1] > 0:
                    if board[i][j] > board[i][j+1]:
                        scores[0] -= np.log2(board[i][j]) - np.log2(board[i][j+1])
                    else:
                        scores[1] -= np.log2(board[i][j+1]) - np.log2(board[i][j])
        
        # Calculate monotonicity for columns (up and down)
        for j in range(len(board[0])):
            for i in range(len(board) - 1):
                if board[i][j] > 0 and board[i+1][j] > 0:
                    if board[i][j] > board[i+1][j]:
                        scores[2] -= np.log2(board[i][j]) - np.log2(board[i+1][j])
                    else:
                        scores[3] -= np.log2(board[i+1][j]) - np.log2(board[i][j])
        
        return max(scores)
    
    def calculate_smoothness(self, board):
        smoothness = 0
        
        # Calculate smoothness for rows
        for i in range(len(board)):
            for j in range(len(board[0]) - 1):
                if board[i][j] > 0 and board[i][j+1] > 0:
                    smoothness -= abs(np.log2(board[i][j]) - np.log2(board[i][j+1]))
        
        # Calculate smoothness for columns
        for j in range(len(board[0])):
            for i in range(len(board) - 1):
                if board[i][j] > 0 and board[i+1][j] > 0:
                    smoothness -= abs(np.log2(board[i][j]) - np.log2(board[i+1][j]))
        
        return smoothness
