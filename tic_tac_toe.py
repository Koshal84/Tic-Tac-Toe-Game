import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide main window initially
        self.root.title("Tic Tac Toe 🧩")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle closing
        self.current_player = "X"
        self.game_mode = None  # "2P" or "AI"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.show_welcome_popup()

    def show_welcome_popup(self):
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome 🎉")
        welcome_window.geometry("400x250")
        welcome_window.grab_set()

        tk.Label(welcome_window, text="🎮 Welcome to Tic Tac Toe!", font=("Arial", 16)).pack(pady=20)
        tk.Label(welcome_window, text="👥 Play with Kushal!", font=("Arial", 14)).pack(pady=10)

        tk.Button(welcome_window, text="Proceed ➡️", font=("Arial", 12),
                  command=lambda: self.proceed_to_mode_selection(welcome_window)).pack(pady=30)

    def proceed_to_mode_selection(self, welcome_window):
        welcome_window.destroy()
        self.show_mode_selection()

    def show_mode_selection(self):
        mode_window = tk.Toplevel(self.root)
        mode_window.title("Select Game Mode")
        mode_window.geometry("300x200")
        mode_window.grab_set()  # Force focus

        tk.Label(mode_window, text="Choose Game Mode:", font=("Arial", 14)).pack(pady=20)

        tk.Button(mode_window, text="2 Player Mode", font=("Arial", 12),
                  command=lambda: self.start_game(mode_window, "2P")).pack(pady=10)

        tk.Button(mode_window, text="Play vs Computer", font=("Arial", 12),
                  command=lambda: self.start_game(mode_window, "AI")).pack(pady=10)

    def start_game(self, window, mode):
        window.destroy()
        self.game_mode = mode
        self.root.deiconify()  # Show main window
        self.root.attributes('-fullscreen', True)  # Fullscreen
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))  # Exit fullscreen
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        for row in range(3):
            for col in range(3):
                btn = tk.Button(frame, text="", font=("Arial", 48), width=5, height=2,
                                command=lambda r=row, c=col: self.make_move(r, c))
                btn.grid(row=row, column=col, padx=20, pady=20)
                self.buttons[row][col] = btn

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=20)

        self.reset_button = tk.Button(control_frame, text="🔁 Restart", font=("Arial", 16),
                                      command=self.reset_game)
        self.reset_button.pack(side="left", padx=20)

        self.close_button = tk.Button(control_frame, text="❌ Close", font=("Arial", 16),
                                      command=self.on_close)
        self.close_button.pack(side="left", padx=20)

    def make_move(self, row, col):
        if self.buttons[row][col]["text"] == "" and not self.check_winner():
            self.buttons[row][col]["text"] = self.current_player
            self.board[row][col] = self.current_player

            if self.check_winner():
                messagebox.showinfo("Game Over", f"🏆 Player {self.current_player} wins!")
                self.disable_all_buttons()
                return
            elif self.check_draw():
                messagebox.showinfo("Game Over", "🤝 It's a draw!")
                return

            self.current_player = "O" if self.current_player == "X" else "X"

            if self.game_mode == "AI" and self.current_player == "O":
                self.root.after(500, self.computer_move)

    def computer_move(self):
        empty_cells = [(r, c) for r in range(3) for c in range(3)
                       if self.board[r][c] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)

    def check_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != "":
                return True
            if b[0][i] == b[1][i] == b[2][i] != "":
                return True
        if b[0][0] == b[1][1] == b[2][2] != "":
            return True
        if b[0][2] == b[1][1] == b[2][0] != "":
            return True
        return False

    def check_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in self.buttons:
            for btn in row:
                btn.config(text="", state="normal")

    def on_close(self):
        thank_window = tk.Toplevel(self.root)
        thank_window.title("Goodbye 👋")
        thank_window.geometry("350x150")
        thank_window.grab_set()

        tk.Label(thank_window, text="🙏 Thanks for playing with Kushal!", font=("Arial", 14)).pack(pady=30)

        self.root.after(1500, self.root.destroy)  # Close the app after 1.5 seconds


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
