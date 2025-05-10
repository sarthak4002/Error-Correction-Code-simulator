from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QComboBox, QTextEdit, QHBoxLayout
)
import sys
import random
from ui.error_visualizer import plot_error_patterns
import matplotlib.pyplot as plt
from ecc.hamming import hamming_encode, hamming_decode
from ecc.reed_solomon import rs_encode, rs_decode
from ecc.convolutional import conv_encode, conv_decode
from ecc.noise import flip_bit_str, flip_random_bits, burst_flip, gaussian_flip
from ui.bitplot import visualize_bits
from ui.animation_window import AnimationWindow

class ECCWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECC Studio: Simulate. Learn. Compare. Win.")
        self.setGeometry(300, 200, 700, 500)

        self.total_inputs = 0
        self.total_errors = 0
        self.total_corrected = 0

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.select_algo = QComboBox()
        self.select_algo.addItems([
            "Hamming Code",
            "Reed-Solomon",
            "Convolutional Code",
            "🔀 Compare All (Side-by-Side)",
            "Parity Step Animation (Hamming)",
            "Parity Step Animation (Convolutional)",
            "Parity Step Animation (Reed-Solomon)",
            "🚀 ECC Battle Mode"
        ])

        self.select_noise = QComboBox()
        self.select_noise.addItems([
            "Random Flip",
            "Burst Error",
            "Gaussian Noise"
        ])

        self.input_label = QLabel("Enter Input Data:")
        self.input_field = QLineEdit()

        self.encode_button = QPushButton("Encode ➤ Add Noise ➤ Decode")
        self.encode_button.clicked.connect(self.run_simulation)

        self.recommend_button = QPushButton("⚙️ Auto Recommend ECC")
        self.recommend_button.clicked.connect(self.recommend_ecc)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        layout.addWidget(QLabel("Select ECC Method:"))
        layout.addWidget(self.select_algo)

        layout.addWidget(self.input_label)
        layout.addWidget(self.input_field)

        layout.addWidget(QLabel("Select Noise Model:"))
        layout.addWidget(self.select_noise)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.encode_button)
        btn_layout.addWidget(self.recommend_button)

        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def apply_noise(self, data: str) -> str:
        noise_model = self.select_noise.currentText()
        data_len = len(data)

        if noise_model == "Random Flip":
            flip_count = 1 if data_len <= 10 else 2
            return flip_random_bits(data, flip_count=flip_count)
        elif noise_model == "Burst Error":
            burst_length = 2 if data_len <= 10 else 3
            return burst_flip(data, burst_length=burst_length)
        elif noise_model == "Gaussian Noise":
            intensity = 0.1 if data_len <= 10 else 0.2
            return gaussian_flip(data, intensity=intensity)
        else:
            return flip_random_bits(data, flip_count=1)

    def recommend_ecc(self):
        data = self.input_field.text().strip()
        if not data:
            QMessageBox.warning(self, "Input Error", "Please enter some input data first.")
            return

        recommendation = ""
        reason = ""

        if all(c in '01' for c in data):
            if len(data) <= 4:
                recommendation = "Hamming Code"
                reason = "Short binary input (≤ 4 bits) is best handled by Hamming."
            else:
                recommendation = "Convolutional Code"
                reason = "Long binary input is better suited to Convolutional codes."
        else:
            recommendation = "Reed-Solomon"
            reason = "Text input is best protected by Reed-Solomon codes."

        if self.total_errors > 0:
            rate = self.total_corrected / self.total_errors
            if rate > 0.8:
                reason += f"\nNote: High correction rate so far ({rate*100:.1f}%)."

        QMessageBox.information(self, "ECC Recommendation",
            f"🔍 Recommended ECC: {recommendation}\n\n📌 Reason: {reason}"
        )

    def run_battle_mode(self):
            rounds = 100
            data_samples = ["1101", "1010", "hello", "0110", "world", "1110", "0011", "data"]
            hamming_success = 0
            conv_success = 0
            rs_success = 0

            for _ in range(rounds):
                data = random.choice(data_samples)

            if len(data) == 4 and all(c in '01' for c in data):
                encoded = hamming_encode(data)
                noisy = self.apply_noise(encoded)
                decoded, err_pos = hamming_decode(noisy)
                if decoded == data:
                    hamming_success += 1

            if all(c in '01' for c in data):
                encoded = conv_encode(data)
                noisy = self.apply_noise(encoded)
                decoded = conv_decode(noisy)
                if decoded == data:
                    conv_success += 1

            if not all(c in '01' for c in data):
                encoded = rs_encode(data)
                noisy = self.apply_noise(encoded)
                decoded, error = rs_decode(noisy)
                if decoded == data:
                    rs_success += 1

            hamming_accuracy = (hamming_success / rounds) * 100
            conv_accuracy = (conv_success / rounds) * 100
            rs_accuracy = (rs_success / rounds) * 100

            result_text = f"""
        🏆 ECC Battle Mode Results ({rounds} rounds)

        Hamming Code Accuracy:       {hamming_accuracy:.2f}%
        Convolutional Code Accuracy: {conv_accuracy:.2f}%
        Reed-Solomon Code Accuracy:   {rs_accuracy:.2f}%
            """

            self.output_text.setText(result_text.strip())

            ecc_names = ['Hamming', 'Convolutional', 'Reed-Solomon']
            accuracies = [hamming_accuracy, conv_accuracy, rs_accuracy]

            plt.figure(figsize=(8,5))
            plt.bar(ecc_names, accuracies, color=['blue', 'green', 'orange'])
            plt.ylim(0, 100)
            plt.ylabel('Accuracy (%)')
            plt.title('ECC Battle Mode: Correction Accuracy')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.show()


    def run_simulation(self):
        algo = self.select_algo.currentText()
        data = self.input_field.text().strip()
        noise_model = self.select_noise.currentText()
        result = ""
        labels = []
        sequences = []
        highlights = []

        if algo == "🚀 ECC Battle Mode":
            self.run_battle_mode()
            return

        self.total_inputs += 1

        if algo.startswith("Parity Step Animation"):
            ecc_type = algo.split("(")[-1].split(")")[0]
            if ecc_type == "Hamming" and (len(data) != 4 or any(c not in '01' for c in data)):
                QMessageBox.warning(self, "Input Error", "Enter 4-bit binary for Hamming Animation.")
                return
            if ecc_type == "Convolutional" and (not all(c in '01' for c in data)):
                QMessageBox.warning(self, "Input Error", "Enter binary string for Convolutional Animation.")
                return
            if ecc_type == "Reed-Solomon" and (not data or all(c in '01' for c in data)):
                QMessageBox.warning(self, "Input Error", "Enter TEXT data for Reed-Solomon Animation.")
                return
            self.anim_window = AnimationWindow(data, ecc_type=ecc_type)
            self.anim_window.show()
            return

        if algo == "Hamming Code":
            if len(data) != 4 or any(c not in '01' for c in data):
                QMessageBox.warning(self, "Input Error", "Enter 4-bit binary for Hamming.")
                return

            encoded = hamming_encode(data)
            noisy = self.apply_noise(encoded)
            decoded, err_pos = hamming_decode(noisy)

            success = decoded == data
            self.total_errors += 1
            if success:
                self.total_corrected += 1

            status = "✅ Recovered Correctly" if success else "❌ Decoding Failed"

            result = f"""
[HAMMING CODE]
Input:              {data}
Encoded:            {encoded}
Noisy Encoded:      {noisy}
Decoded:            {decoded}
Error Corrected At: {err_pos if err_pos else 'None'}
Status:             {status}
"""

            labels = ["Encoded", "Noisy", "Decoded"]
            sequences = [encoded, noisy, hamming_encode(decoded)]
            highlights = [[False]*len(encoded) for _ in range(3)]

            plot_error_patterns(data, noisy, decoded)

        elif algo == "Reed-Solomon":
            if not data or all(c in '01' for c in data):
                QMessageBox.warning(self, "Input Error", "Enter text (non-binary) data for Reed-Solomon.")
                return

            encoded = rs_encode(data)
            noisy = self.apply_noise(encoded)
            decoded, error = rs_decode(noisy)

            success = decoded == data
            self.total_errors += 1
            if success:
                self.total_corrected += 1

            status = "✅ Recovered Correctly" if success else "❌ Decoding Failed"

            result = f"""
[REED-SOLOMON]
Input:         {data}
Encoded:       {encoded}
Noisy:         {noisy}
Decoded:       {decoded if decoded else 'Decoding Failed'}
Error:         {error if error else 'None'}
Status:        {status}
"""

        elif algo == "Convolutional Code":
            if len(data) == 0 or any(c not in '01' for c in data):
                QMessageBox.warning(self, "Input Error", "Enter binary string for Convolutional Code.")
                return

            encoded = conv_encode(data)
            noisy = self.apply_noise(encoded)
            decoded = conv_decode(noisy)

            success = decoded == data
            self.total_errors += 1
            if success:
                self.total_corrected += 1

            status = "✅ Recovered Correctly" if success else "❌ Decoding Failed"

            result = f"""
[CONVOLUTIONAL CODE]
Input:              {data}
Encoded:            {encoded}
Noisy Encoded:      {noisy}
Decoded:            {decoded}
Status:             {status}
"""

            labels = ["Encoded", "Noisy", "Decoded"]
            sequences = [encoded, noisy, conv_encode(decoded)]
            highlights = [[False]*len(encoded) for _ in range(3)]

            plot_error_patterns(data, noisy, decoded)

        elif algo == "🔀 Compare All (Side-by-Side)":
            result = "[COMPARISON MODE]\n\n"

            if len(data) == 4 and all(c in '01' for c in data):
                encoded = hamming_encode(data)
                noisy = self.apply_noise(encoded)
                decoded, err_pos = hamming_decode(noisy)
                status = "✅" if decoded == data else "❌"
                result += f"🔹 Hamming Code: {status}\n"

            if all(c in '01' for c in data):
                encoded = conv_encode(data)
                noisy = self.apply_noise(encoded)
                decoded = conv_decode(noisy)
                status = "✅" if decoded == data else "❌"
                result += f"🔹 Convolutional Code: {status}\n"

            if data and not all(c in '01' for c in data):
                encoded = rs_encode(data)
                noisy = self.apply_noise(encoded)
                decoded, error = rs_decode(noisy)
                status = "✅" if decoded == data else "❌"
                result += f"🔹 Reed-Solomon Code: {status}\n"
            else:
                result += "🔹 Reed-Solomon Code: Skipped (binary input)\n"

        self.output_text.setText(result.strip())

        if labels and sequences:
            visualize_bits(f"{algo} - Bit Visualization", labels, sequences, highlights)
        
        

def launch_app():
    app = QApplication(sys.argv)
    window = ECCWindow()
    window.show()
    sys.exit(app.exec_())
