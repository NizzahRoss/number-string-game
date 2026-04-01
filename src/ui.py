import tkinter as tk
from tkinter import messagebox, simpledialog
from src.game_state import GameState
from src.alphabeta import alpha_beta

class NumberStringGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number String Game")
        self.state = None
        self.ai_depth = 5   # default search depth for AI
        self.human_vs_ai = False
        self.ai_player = 'first'   # 'first' or 'second'

        # Create widgets
        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        # Top frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        tk.Button(control_frame, text="New Game", command=self.new_game_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="AI Move", command=self.ai_move).pack(side=tk.LEFT, padx=5)

        # Main game display
        display_frame = tk.Frame(self.root)
        display_frame.pack(pady=10)

        self.numbers_label = tk.Label(display_frame, text="", font=("Courier", 24))
        self.numbers_label.pack()

        self.info_label = tk.Label(display_frame, text="", font=("Arial", 12))
        self.info_label.pack()

        # Move buttons frame
        self.move_frame = tk.Frame(self.root)
        self.move_frame.pack(pady=10)

        self.move_buttons = []

    def new_game_dialog(self):
        # Ask for game mode and length
        mode = messagebox.askyesno("Game Mode", "Play against AI? (Yes = vs AI, No = two human)")
        self.human_vs_ai = mode
        if mode:
            ai_side = messagebox.askyesno("AI Side", "AI plays as first player? (Yes = AI first, No = AI second)")
            self.ai_player = 'first' if ai_side else 'second'

        length = simpledialog.askinteger("String Length", "Enter length (15‑25):",
                                         minvalue=15, maxvalue=25)
        if length:
            self.state = GameState.random_initial(length)
            self.update_display()
            # If AI is first player and it's AI's turn, make AI move automatically
            if self.human_vs_ai and self.state.turn == self.ai_player:
                self.root.after(500, self.ai_move)   # slight delay for visibility

    def new_game(self):
        # Default new game with random length 15
        self.state = GameState.random_initial(15)
        self.update_display()

    def update_display(self):
        # Update the string and info
        self.numbers_label.config(text=" ".join(str(n) for n in self.state.nums))
        player_str = "First Player" if self.state.turn == 'first' else "Second Player"
        self.info_label.config(text=f"Score: {self.state.points}   Bank: {self.state.bank}   Turn: {player_str}")

        # Clear old move buttons
        for btn in self.move_buttons:
            btn.destroy()
        self.move_buttons.clear()

        # Create new move buttons from the move dicts
        moves = self.state.get_moves()
        for move in moves:
            # Create a readable label
            if move['type'] == 'pair':
                text = f"Pair {move['pair_idx']} (positions {move['pair_idx']*2}, {move['pair_idx']*2+1})"
            else:
                text = "Delete last"
            btn = tk.Button(self.move_frame, text=text, command=lambda m=move: self.human_move(m))
            btn.pack(side=tk.LEFT, padx=2)
            self.move_buttons.append(btn)

        # Check for game over
        if self.state.is_terminal():
            self.show_result()

    def human_move(self, move):
        if self.state.is_terminal():
            return
        self.state = self.state.apply_move(move)
        self.update_display()

        # If playing against AI and now it's AI's turn, make AI move
        if self.human_vs_ai and not self.state.is_terminal() and self.state.turn == self.ai_player:
            self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.state.is_terminal():
            return
        # Use alpha-beta to choose move
        _, move = alpha_beta(self.state, self.ai_depth)
        if move is None:
            # fallback to random (should not happen)
            import random
            move = random.choice(self.state.get_moves())
        self.state = self.state.apply_move(move)
        self.update_display()

    def show_result(self):
        result = self.state.get_result()
        if result == 'first':
            msg = "First player wins!"
        elif result == 'second':
            msg = "Second player wins!"
        else:
            msg = "It's a draw!"
        messagebox.showinfo("Game Over", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberStringGameUI(root)
    root.mainloop()
