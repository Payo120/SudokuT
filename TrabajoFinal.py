import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import copy
import random

class SudokuGenerator:

    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_counter = 0

    def _find_empty(self, board):

        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None 

    def _is_valid(self, board, num, row, col):

        for c in range(9):
            if board[row][c] == num and c != col:
                return False
# NO ES VALIDO SI LA COLUMNA ES DIFERENTE 
        for r in range(9):
            if board[r][col] == num and r != row:
                return False
    
        start_row, start_col = 3 * (row // 3), 3 * (col // 3) 
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if board[r][c] == num and (r, c) != (row, col): #definir mejor / que es r y que es c en este caso
                    return False
        return True

    def _fill_grid(self, board):

        find = self._find_empty(board)
        if not find:
            return True
        else:
            row, col = find #aclarar mas
        
        nums = list(range(1, 10))
        random.shuffle(nums) #entender mas
        '''entender esto como si fuera un libro'''
        for num in nums:
            if self._is_valid(board, num, row, col):
                board[row][col] = num
                if self._fill_grid(board):
                    return True
                board[row][col] = 0
        return False

    def _count_solutions_recursive(self, board):

        if self.solution_counter > 1:
            return #entender mas

        find = self._find_empty(board)
        if not find:
            self.solution_counter += 1
            return #entender mas
        
        row, col = find
        for num in range(1, 10):
            if self._is_valid(board, num, row, col):
                board[row][col] = num
                self._count_solutions_recursive(board)
                board[row][col] = 0 # Backtrack/Tilin

    def generate_puzzle(self, difficulty):

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self._fill_grid(self.board)
        
        self.solution = copy.deepcopy(self.board)

        if difficulty == 'easy':
            squares_to_remove = 40
        elif difficulty == 'medium':
            squares_to_remove = 50
        else: # 'hard'
            squares_to_remove = 56

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        removed_count = 0
        for r, c in cells:
            if removed_count >= squares_to_remove:
                break

            temp = self.board[r][c]
            self.board[r][c] = 0
            
            board_copy = copy.deepcopy(self.board)
            self.solution_counter = 0
            self._count_solutions_recursive(board_copy)

            if self.solution_counter != 1:
                self.board[r][c] = temp
            else:
                removed_count += 1
                
        return self.board

class SudokuApp:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku")
        master.resizable(False, False)

        style = ttk.Style()
        style.configure("TButon", font=("Arial", 12), padding=5)
        style.configure("TFrame", padding="10 10 10 10")
        
        self.generator = SudokuGenerator
        self.initial_board = []
        self.solution_board = []
        self.curret_board = []
        self.cells = {}
        self.cells_var = {}
        