import tkinter as tk
from tkinter import messagebox
import graphviz
from PIL import Image, ImageTk

class MorseDecoderFSA:
    def __init__(self):
        self.state = 'START'
        self.current_morse = ''
        self.decoded_message = []
        self.morse_to_letter = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
            '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
            '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
            '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
            '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
            '-----': '0'
        }

    def transition(self, symbol):
        if symbol == '.':
            self.current_morse += symbol
            self.state = 'DOT'
        elif symbol == '-':
            self.current_morse += symbol
            self.state = 'DASH'
        elif symbol == ' ':
            if self.current_morse:
                self.decode_current_morse()
            self.state = 'START'
        elif symbol == '/':
            if self.current_morse:
                self.decode_current_morse()
            self.decoded_message.append(' ')
            self.state = 'START'

    def decode_current_morse(self):
        if self.current_morse in self.morse_to_letter:
            self.decoded_message.append(self.morse_to_letter[self.current_morse])
        self.current_morse = ''

    def decode(self, morse_code):
        self.decoded_message = []
        self.current_morse = ''
        for symbol in morse_code:
            self.transition(symbol)
        if self.current_morse:
            self.decode_current_morse()
        return ''.join(self.decoded_message)

    def generate_finite_state_diagram(self, morse_code=None):
        dot = graphviz.Digraph(comment='Morse Decoder FSA')
        dot.attr(rankdir='LR')

        # Start node
        dot.node('START', 'START', shape='circle', style='filled', fillcolor='lightblue')

        # Track edges to avoid duplicates
        edges = set()
        path_followed = []

        # Generate FSA structure
        for morse_code_key, letter in self.morse_to_letter.items():
            current_state = 'START'
            path = ''
            for symbol in morse_code_key:
                path += symbol
                next_state = f'{path}'

                # Add node and edge
                if (current_state, next_state, symbol) not in edges:
                    dot.node(next_state, f'{path} ({symbol})')
                    dot.edge(current_state, next_state, label=symbol, color='black')
                    edges.add((current_state, next_state, symbol))

                current_state = next_state

            # Final node for the decoded letter
            final_state = f'{current_state}_decoded'
            dot.node(final_state, f'{letter}', shape='doublecircle', style='filled', fillcolor='yellow')
            dot.edge(current_state, final_state, label=f'Decode: {letter}', color='black')

        # Add the path followed if morse_code is provided
        if morse_code:
            current_state = 'START'
            path = ''
            for symbol in morse_code:
                path += symbol
                next_state = f'{path}'

                # Highlight the path by changing color to red
                if (current_state, next_state, symbol) in edges:
                    dot.edge(current_state, next_state, label=symbol, color='red', penwidth='2')
                current_state = next_state

            # Highlight the final state for the last character
            final_state = f'{current_state}_decoded'
            if final_state in dot.node_attr:
                dot.node(final_state, style='filled', fillcolor='orange')

        # Handle space (separation of words)
        dot.edge('START', 'START', label='/ (space)')
        dot.edge('START', 'START', label='space')

        # Render and output the diagram as a PNG
        dot.render('morse_decoder_fsa', format='png', cleanup=True)

# GUI Setup using Tkinter
class MorseDecoderGUI:
    def __init__(self, root):
        self.decoder = MorseDecoderFSA()

        root.title("Morse Code Decoder")
        root.geometry("400x400")

        # Create input and output areas
        self.label = tk.Label(root, text="Enter Morse Code (use '/' for word separation):")
        self.label.pack(pady=10)

        self.input_text = tk.Entry(root, width=50)
        self.input_text.pack(pady=10)

        self.decode_button = tk.Button(root, text="Decode", command=self.decode_morse)
        self.decode_button.pack(pady=10)

        self.output_label = tk.Label(root, text="Decoded Message:")
        self.output_label.pack(pady=10)

        self.output_text = tk.Text(root, height=4, width=50)
        self.output_text.pack(pady=10)

        self.diagram_button = tk.Button(root, text="Generate FSA Diagram", command=self.generate_diagram)
        self.diagram_button.pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

    def decode_morse(self):
        morse_code = self.input_text.get()
        decoded_message = self.decoder.decode(morse_code)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, decoded_message)

    def generate_diagram(self):
        morse_code = self.input_text.get()
        self.decoder.generate_finite_state_diagram(morse_code)

        # Load and display the diagram image
        img = Image.open("morse_decoder_fsa.png")
        img = img.resize((1200, 600), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)

        self.image_label.config(image=img)
        self.image_label.image = img

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = MorseDecoderGUI(root)
    root.mainloop()