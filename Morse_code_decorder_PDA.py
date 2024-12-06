import tkinter as tk
from tkinter import messagebox

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
    def __init__(self, display_callback, stack_callback):
        self.stack = []
        self.current_state = 'START'
        self.display_callback = display_callback
        self.update_stack_visual = stack_callback
        self.decoded_message = ""
        self.current_index = 0
        self.morse_code_sequence = ""
    
    def set_input(self, morse_code_sequence):
        # Initialize or reset PDA state and input sequence
        self.morse_code_sequence = morse_code_sequence
        self.current_index = 0
        self.decoded_message = ""
        self.stack.clear()
        self.current_state = 'START'
        self.display_callback("Ready to decode. Press 'Step' or 'Decode All'.")
        self.update_stack_visual(self.stack)
    
    def step_decode(self):
        # Process one symbol at a time and show its effect on the PDA
        if self.current_index >= len(self.morse_code_sequence):
            self.display_callback("End of sequence reached.")
            return

        symbol = self.morse_code_sequence[self.current_index]
        self.current_index += 1

        if symbol == '.' or symbol == '-':
            # Push . or - to the stack
            self.stack.append(symbol)
            self.visualize('Push', symbol)
        elif symbol == ' ':
            # A space signifies the end of a letter; decode the letter
            self.decoded_message += self.decode_stack()
            self.visualize('Space', 'Decode')
        elif symbol == '/':
            # A slash signifies the end of a word; decode and add space
            self.decoded_message += self.decode_stack() + " "
            self.visualize('Slash', 'New Word')
        
        self.update_stack_visual(self.stack)
    
    def decode_all(self):
        # Decode the entire Morse sequence at once
        while self.current_index < len(self.morse_code_sequence):
            self.step_decode()
        
        # Final decode of any remaining content in the stack
        if self.stack:
            self.decoded_message += self.decode_stack()
        
        self.display_callback(f"Final Decoded Message: {self.decoded_message.strip()}")
    
    def decode_stack(self):
        # Decode the Morse sequence in the stack into an English character
        if not self.stack:
            return ""
        
        morse_char = ''.join(self.stack)
        self.stack.clear()  # Clear stack after decoding
        decoded_char = morse_code_dict.get(morse_char, '?')  # Use '?' if character not found
        self.visualize('Decode', decoded_char)
        return decoded_char
    
    def visualize(self, action, detail):
        # Show detailed actions taken by the PDA in the output
        self.display_callback(f"Action: {action} | Detail: {detail} | Stack: {self.stack} | State: {self.current_state}")

# GUI Application        
class MorseCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code PDA Decoder")        
        
        # Instructions
        instruction_label = tk.Label(root, text="Enter Morse Code (Use '.' for dot, '-' for dash, ' ' for letter separation, '/' for word separation):")
        instruction_label.pack(pady=10)
        
        # Input Textbox
        self.input_text = tk.Entry(root, width=50)
        self.input_text.pack(pady=5)
        
        # Control Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        step_button = tk.Button(button_frame, text="Step", command=self.handle_step)
        step_button.grid(row=0, column=0, padx=5)
        
        decode_all_button = tk.Button(button_frame, text="Decode All", command=self.handle_decode_all)
        decode_all_button.grid(row=0, column=1, padx=5)
        
        reset_button = tk.Button(button_frame, text="Reset", command=self.reset)
        reset_button.grid(row=0, column=2, padx=5)
        
        # PDA Visualization Area
        self.output_text = tk.Text(root, width=50, height=10, state="disabled")
        self.output_text.pack(pady=5)

        # Stack Visualization
        self.stack_label = tk.Label(root, text="Stack:", font=("Arial", 12))
        self.stack_label.pack(pady=5)
        self.stack_display = tk.Text(root, width=20, height=5, state="disabled")
        self.stack_display.pack(pady=5)

        # Step-by-step Explanation
        self.step_explanation = tk.Label(root, text="Current Step Explanation:", font=("Arial", 12))
        self.step_explanation.pack(pady=5)

        # Final Decoded Message Display
        self.final_message_label = tk.Label(root, text="Final Decoded Message:", font=("Arial", 12))
        self.final_message_label.pack(pady=5)
        self.final_message_display = tk.Text(root, width=50, height=2, state="disabled")
        self.final_message_display.pack(pady=5)

        # Initialize PDA decoder
        self.pda_decoder = PDAMorseDecoder(self.display_message, self.update_stack_display)

    def handle_step(self):
        # Ensure input is set and output is reset
        self.initialize_input()
        # Trigger single step decode in PDA
        self.pda_decoder.step_decode()

    def handle_decode_all(self):
        # Ensure input is set and output is reset
        self.initialize_input()
        # Trigger full sequence decode in PDA
        self.pda_decoder.decode_all()

    def initialize_input(self):
        # Reset output and initialize PDA with new input
        morse_code = self.input_text.get()
        if not morse_code:
            messagebox.showerror("Error", "Please enter Morse code.")
            return
        self.reset_output()
        self.pda_decoder.set_input(morse_code)

    def reset_output(self):
        # Clear output and stack displays
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")
        
        self.stack_display.config(state="normal")
        self.stack_display.delete(1.0, tk.END)
        self.stack_display.config(state="disabled")

        self.final_message_display.config(state="normal")
        self.final_message_display.delete(1.0, tk.END)
        self.final_message_display.config(state="disabled")

    def display_message(self, message):
        # Update the output box with each message
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.config(state="disabled")
        self.final_message_display.config(state="normal")
        self.final_message_display.delete(1.0, tk.END)
        self.final_message_display.insert(tk.END, self.pda_decoder.decoded_message.strip())
        self.final_message_display.config(state="disabled")
    
    def update_stack_display(self, stack):
        # Display the current stack visually
        self.stack_display.config(state="normal")
        self.stack_display.delete(1.0, tk.END)
        for symbol in stack:
            self.stack_display.insert(tk.END, f"{symbol} ")
        self.stack_display.config(state="disabled")

    def reset(self):
        # Reset input, output, and stack displays
        self.input_text.delete(0, tk.END)
        self.reset_output()

# Main Application
root = tk.Tk()
app = MorseCodeApp(root)
root.mainloop()



