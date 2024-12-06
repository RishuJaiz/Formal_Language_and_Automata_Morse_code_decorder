import tkinter as tk
from tkinter import messagebox, font as tkfont

# Morse Code dictionary for reference
morse_code_dict = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G',
    '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N',
    '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U',
    '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', '-----': '0',
    '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6',
    '--...': '7', '---..': '8', '----.': '9'
}

class PDAMorseDecoder:
    def __init__(self, display_callback, update_stack_visual, update_letter_stack_visual, update_state_visual):
        self.stack = []
        self.letter_stack = []
        self.decoded_message = ""
        self.morse_code_sequence = ""
        self.current_index = 0
        self.current_state = "START"
        self.display_callback = display_callback
        self.update_stack_visual = update_stack_visual
        self.update_letter_stack_visual = update_letter_stack_visual
        self.update_state_visual = update_state_visual

    def set_input(self, morse_code_sequence):
        self.morse_code_sequence = morse_code_sequence.strip()
        self.current_index = 0
        self.decoded_message = ""
        self.stack = []
        self.letter_stack = []
        self.current_state = "START"
        self.display_callback("Ready to decode. Press 'Step' or 'Decode All'.")
        self.update_stack_visual(self.stack)
        self.update_letter_stack_visual(self.letter_stack)
        self.update_state_visual(self.current_state)

    def step_decode(self):
        if self.current_index >= len(self.morse_code_sequence):
            if self.stack:
                decoded_char = self.decode_stack()
                self.decoded_message += decoded_char
                self.letter_stack.append(decoded_char)
                self.update_letter_stack_visual(self.letter_stack)
            self.current_state = "END"
            self.display_callback("End of sequence reached.")
            self.update_stack_visual(self.stack)
            self.update_state_visual(self.current_state)
            return

        symbol = self.morse_code_sequence[self.current_index]
        self.current_index += 1

        if symbol in '.-':
            self.stack.append(symbol)
            self.current_state = "READ_SYMBOL"
            action = 'Push'
        elif symbol == ' ':
            if self.stack:
                decoded_char = self.decode_stack()
                self.decoded_message += decoded_char
                self.letter_stack.append(decoded_char)
                self.update_letter_stack_visual(self.letter_stack)
            self.current_state = "SPACE"
            action = 'Space'
        elif symbol == '/':
            if self.stack:
                decoded_char = self.decode_stack()
                self.decoded_message += decoded_char
                self.letter_stack.append(decoded_char)
                self.update_letter_stack_visual(self.letter_stack)
            self.decoded_message += ' '
            self.letter_stack.append(' ')
            self.current_state = "SLASH"
            self.update_letter_stack_visual(self.letter_stack)
            action = 'Slash'
        else:
            action = 'Invalid'
            symbol = f"Invalid symbol '{symbol}' ignored"
            self.current_state = "ERROR"

        self.display_callback(f"Action: {action} | Symbol: {symbol}")
        self.update_stack_visual(self.stack)
        self.update_state_visual(self.current_state)

    def decode_stack(self):
        if not self.stack:
            return ""
        morse_char = ''.join(self.stack)
        self.stack = []
        decoded_char = morse_code_dict.get(morse_char, '?')
        self.current_state = "DECODE"
        self.display_callback(f"Decoded: {decoded_char} from {morse_char}")
        self.update_stack_visual(self.stack)
        self.update_state_visual(self.current_state)
        return decoded_char

    def decode_all(self):
        while self.current_index < len(self.morse_code_sequence):
            self.step_decode()

class MorseCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Funky Morse Code PDA Decoder")
        self.root.configure(bg='black')

        title_font = tkfont.Font(family='Helvetica', size=16, weight="bold", underline=True)
        text_font = tkfont.Font(family='Helvetica', size=12)

        instruction_label = tk.Label(root, text="Enter Morse Code:", font=title_font, bg='black', fg='lime')
        instruction_label.pack(pady=20)

        self.input_text = tk.Entry(root, font=text_font, width=50)
        self.input_text.pack(pady=10)

        button_frame = tk.Frame(root, bg='black')
        button_frame.pack(pady=20)

        step_button = tk.Button(button_frame, text="Step", font=text_font, command=self.handle_step)
        step_button.grid(row=0, column=0, padx=10)

        decode_all_button = tk.Button(button_frame, text="Decode All", font=text_font, command=self.handle_decode_all)
        decode_all_button.grid(row=0, column=1, padx=10)

        reset_button = tk.Button(button_frame, text="Reset", font=text_font, command=self.reset)
        reset_button.grid(row=0, column=2, padx=10)

        self.output_text = tk.Text(root, height=10, width=100, font=text_font, bg='black', fg='white', wrap=tk.WORD)
        self.output_text.pack(pady=10)

        self.stack_canvas = tk.Canvas(root, width=400, height=100, bg='black')
        self.stack_canvas.pack(pady=10)

        self.letter_stack_canvas = tk.Canvas(root, width=800, height=100, bg='black')
        self.letter_stack_canvas.pack(pady=10)

        self.state_canvas = tk.Canvas(root, width=800, height=50, bg='black')
        self.state_canvas.pack(pady=10)

        self.pda_decoder = PDAMorseDecoder(
            self.display_message,
            self.update_stack_visual,
            self.update_letter_stack_visual,
            self.update_state_visual
        )

    def handle_step(self):
        if not self.input_text.get():
            messagebox.showinfo("Error", "Please enter Morse code.")
            return
        if not self.pda_decoder.morse_code_sequence:
            self.reset_output()
            self.pda_decoder.set_input(self.input_text.get())
        self.pda_decoder.step_decode()

    def handle_decode_all(self):
        if not self.input_text.get():
            messagebox.showinfo("Error", "Please enter Morse code.")
            return
        if not self.pda_decoder.morse_code_sequence:
            self.reset_output()
            self.pda_decoder.set_input(self.input_text.get())
        self.pda_decoder.decode_all()

    def reset_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")
        self.stack_canvas.delete("all")
        self.letter_stack_canvas.delete("all")
        self.state_canvas.delete("all")

    def display_message(self, message):
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.config(state="disabled")

    def update_stack_visual(self, stack):
        self.stack_canvas.delete("all")
        x, y = 20, 50
        for symbol in reversed(stack):
            self.stack_canvas.create_text(x, y, text=symbol, fill="lime", font=('Helvetica', 18, 'bold'))
            x += 20

    def update_letter_stack_visual(self, letter_stack):
        self.letter_stack_canvas.delete("all")
        x, y = 20, 50
        for letter in letter_stack:
            self.letter_stack_canvas.create_text(x, y, text=letter, fill="cyan", font=('Helvetica', 18, 'bold'))
            x += 20

    def update_state_visual(self, state):
        self.state_canvas.delete("all")
        self.state_canvas.create_text(400, 25, text=f"Current State: {state}", fill="yellow", font=('Helvetica', 18, 'bold'))

    def reset(self):
        self.input_text.delete(0, tk.END)
        self.reset_output()
        self.pda_decoder.set_input("")

# Main Application
root = tk.Tk()
app = MorseCodeApp(root)
root.mainloop()
