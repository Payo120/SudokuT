import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import copy
import random

class SudokuGenerator:
    """
    Clase para generar un puzzle de Sudoku válido y con solución única.
    """
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_counter = 0

    def _find_empty(self, board):
        """Encuentra una celda vacía (con 0)."""
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0: 
                    return (r, c)
        return None

    def _is_valid(self, board, num, row, col):
        """Verifica si un número es válido en una posición."""
        # Comprobar fila
        for c in range(9):
            if board[row][c] == num and c != col:
                return False
        # Comprobar columna
        for r in range(9):
            if board[r][col] == num and r != row:
                return False
        # Comprobar bloque 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if board[r][c] == num and (r, c) != (row, col):
                    return False
        return True

    def _fill_grid(self, board):
        """Rellena recursivamente el tablero para crear una solución completa."""
        find = self._find_empty(board)
        if not find:
            return True
        else:
            row, col = find
        
        nums = list(range(1, 10))
        random.shuffle(nums)

        for num in nums:
            if self._is_valid(board, num, row, col):
                board[row][col] = num
                if self._fill_grid(board):
                    return True
                board[row][col] = 0
        return False

    def _count_solutions_recursive(self, board):
        """Cuenta el número de soluciones posibles para un tablero."""
        if self.solution_counter > 1:
            return

        find = self._find_empty(board)
        if not find:
            self.solution_counter += 1
            return
        
        row, col = find
        for num in range(1, 10):
            if self._is_valid(board, num, row, col):
                board[row][col] = num
                self._count_solutions_recursive(board)
                board[row][col] = 0 # Backtrack

    def generate_puzzle(self, difficulty):
        """Genera el puzzle completo: crea solución y quita números."""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self._fill_grid(self.board)
        
        self.solution = copy.deepcopy(self.board)

        if difficulty == 'easy':
            squares_to_remove = 40
        elif difficulty == 'medium':
            squares_to_remove = 50
        else: # hard
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
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TFrame", padding="10 10 10 10")
        
        self.generator = SudokuGenerator()
        self.initial_board = []
        self.solution_board = []
        self.current_board = []
        self.cells = {}
        self.cell_vars = {}

        self.create_widgets()
        self.new_game('easy')

    def create_widgets(self):
        self.difficulty_frame = ttk.Frame(self.master)
        self.difficulty_frame.pack(fill=tk.X, padx=10, pady=(10,0))
        ttk.Label(self.difficulty_frame, text="Dificultad:", font=("Arial", 12)).pack(side=tk.LEFT, padx=(0,10))
        
        self.easy_button = ttk.Button(self.difficulty_frame, text="Fácil", command=lambda: self.new_game('easy'))
        self.easy_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        self.medium_button = ttk.Button(self.difficulty_frame, text="Medio", command=lambda: self.new_game('medium'))
        self.medium_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        self.hard_button = ttk.Button(self.difficulty_frame, text="Difícil", command=lambda: self.new_game('hard'))
        self.hard_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.grid_frame = ttk.Frame(self.master, borderwidth=2, relief="groove")
        self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        vcmd = (self.master.register(self.validate_input), '%P')

        for r in range(9):
            for c in range(9):
                cell_var = tk.StringVar(self.master)
                cell_var.trace_add("write", lambda name, index, mode, var=cell_var, row=r, col=c: self.update_cell(var, row, col))
                
                entry = ttk.Entry(self.grid_frame, textvariable=cell_var, width=3,
                                  font=('Arial', 20, 'bold'), justify='center',
                                  validate="key", validatecommand=vcmd)
                
                padx_val = (1, 15) if (c + 1) % 3 == 0 and c != 8 else 1
                pady_val = (1, 15) if (r + 1) % 3 == 0 and r != 8 else 1

                entry.grid(row=r, column=c, padx=padx_val, pady=pady_val, ipady=5, sticky="nsew")
                
                self.cells[(r, c)] = entry
                self.cell_vars[(r, c)] = cell_var
        
        self.buttons_frame = ttk.Frame(self.master)
        self.buttons_frame.pack(fill=tk.X, expand=True, padx=10, pady=(5, 10))

        self.solve_button = ttk.Button(self.buttons_frame, text="Resolver", command=self.solve_and_display)
        self.solve_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.reset_button = ttk.Button(self.buttons_frame, text="Reiniciar", command=self.reset_board)
        self.reset_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.check_button = ttk.Button(self.buttons_frame, text="Comprobar", command=self.check_solution)
        self.check_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def new_game(self, difficulty):
        self.master.config(cursor="watch")
        self.master.update()

        self.initial_board = self.generator.generate_puzzle(difficulty)
        self.solution_board = self.generator.solution
        self.current_board = copy.deepcopy(self.initial_board)
        
        for r in range(9):
            for c in range(9):
                value = self.initial_board[r][c]
                cell_var = self.cell_vars[(r, c)]
                entry = self.cells[(r, c)]
                
                if value != 0:
                    cell_var.set(str(value))
                    entry.config(state='readonly', foreground='black')
                else:
                    cell_var.set("")
                    entry.config(state='normal', foreground='blue')

        self.master.config(cursor="")

    def reset_board(self):
        """Limpia el progreso del usuario en el tablero actual."""
        for r in range(9):
            for c in range(9):

                if self.initial_board[r][c] == 0:
                    self.cell_vars[(r,c)].set("")
                    self.cells[(r,c)].config(foreground='blue')
        self.current_board = copy.deepcopy(self.initial_board)


    def validate_input(self, P):
        return (P == "" or (P.isdigit() and 1 <= int(P) <= 9 and len(P) == 1))

    def update_cell(self, var, row, col):
        value_str = var.get()
        entry = self.cells[(row, col)]
        
        if not value_str:
            self.current_board[row][col] = 0
            entry.config(foreground='blue')
            return

        value = int(value_str)
        self.current_board[row][col] = value
        

        if self.generator._is_valid(self.current_board, value, row, col):
            entry.config(foreground='blue')
        else:
            entry.config(foreground='red')

    def solve_and_display(self):
        self.current_board = copy.deepcopy(self.solution_board) 
        for r in range(9):
            for c in range(9):
                self.cell_vars[(r,c)].set(str(self.current_board[r][c]))
                if self.initial_board[r][c] == 0:
                    self.cells[(r, c)].config(foreground='#339933') 
                else:
                    self.cells[(r, c)].config(foreground='black')


    def is_board_full(self):
        return all(self.current_board[r][c] != 0 for r in range(9) for c in range(9))

    def is_board_correct(self):

        return self.current_board == self.solution_board

    def check_solution(self):
        if not self.is_board_full():
            tkinter.messagebox.showwarning("Incompleto", "El tablero aún no está completo.")
            return

        if self.is_board_correct():
            self.show_victory_message()
        else:
            tkinter.messagebox.showerror("Incorrecto", "Hay errores en tu solución. ¡Sigue intentando!")

    def show_victory_message(self):
        tkinter.messagebox.showinfo("¡Felicidades!", "¡Has resuelto el Sudoku correctamente!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
