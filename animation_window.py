from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QProgressBar, QHBoxLayout
)
from PyQt5.QtCore import QTimer
from ecc.hamming import hamming_encode, hamming_decode
from ecc.convolutional import conv_encode, conv_decode
from ecc.reed_solomon import rs_encode, rs_decode
from ecc.noise import flip_random_bits
import random
from PyQt5.QtCore import Qt

class AnimationWindow(QWidget):
    def __init__(self, data, ecc_type="Hamming"):
        super().__init__()
        self.data = data
        self.ecc_type = ecc_type
        self.setWindowTitle(f"{ecc_type} Animation Demo")
        self.setGeometry(400, 200, 800, 400)
        self.current_step = 0
        self.steps = []
        self.setup_steps()

        self.label = QLabel(self.steps[self.current_step], self)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 22px; font-family: Arial; color: #333; padding: 10px;")
        self.label.setAlignment(Qt.AlignCenter)

        self.next_button = QPushButton("Next Step ➡️", self)
        self.next_button.setStyleSheet(
            "font-size: 18px; background-color: #4CAF50; color: white; padding: 10px; border-radius: 8px;"
        )
        self.next_button.clicked.connect(self.next_step)

        self.progress = QProgressBar(self)
        self.progress.setMaximum(len(self.steps))
        self.progress.setValue(1)
        self.progress.setStyleSheet(
            "QProgressBar {"
            "border: 2px solid #aaa;"
            "border-radius: 5px;"
            "text-align: center;"
            "}"
            "QProgressBar::chunk {"
            "background-color: #4CAF50;"
            "width: 20px;"
            "}"
        )

        # Optional: Auto-Play
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.timer.start(4000)  # Every 4 seconds

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_button)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #f2f6fc;")  # Soft background color

    def setup_steps(self):
        if self.ecc_type == "Hamming":
            self.animate_hamming()
        elif self.ecc_type == "Convolutional":
            self.animate_convolutional()
        elif self.ecc_type == "Reed-Solomon":
            self.animate_reed_solomon()

    def animate_hamming(self):
        self.steps.append(f"Input 4-bit data: {self.data}")

        d = list(map(int, self.data))
        p1 = d[0] ^ d[1] ^ d[3]
        p2 = d[0] ^ d[2] ^ d[3]
        p3 = d[1] ^ d[2] ^ d[3]
        encoded = f"{p1}{p2}{d[0]}{p3}{d[1]}{d[2]}{d[3]}"
        self.encoded = encoded

        self.steps.append(f"Calculated parity bits:\nP1={p1}, P2={p2}, P3={p3}")
        self.steps.append(f"7-bit Encoded data:\n{encoded}")

        flip_index = random.randint(0, len(encoded) - 1)
        noisy = list(encoded)
        noisy[flip_index] = '1' if noisy[flip_index] == '0' else '0'
        noisy = ''.join(noisy)
        self.noisy = noisy
        self.flip_index = flip_index

        self.steps.append(f"Introduced error by flipping bit {flip_index+1}:\n{noisy}")

        e = list(map(int, noisy))
        s1 = e[0] ^ e[2] ^ e[4] ^ e[6]
        s2 = e[1] ^ e[2] ^ e[5] ^ e[6]
        s3 = e[3] ^ e[4] ^ e[5] ^ e[6]
        error_pos = s1 * 1 + s2 * 2 + s3 * 4
        self.steps.append(f"Detected error at position: {error_pos}")

        corrected = list(noisy)
        if error_pos != 0:
            corrected[error_pos - 1] = '1' if corrected[error_pos - 1] == '0' else '0'
        corrected = ''.join(corrected)

        decoded = f"{corrected[2]}{corrected[4]}{corrected[5]}{corrected[6]}"
        self.steps.append(f"Corrected data: {corrected}")
        self.steps.append(f"Recovered original 4-bit data: {decoded}")

    def animate_convolutional(self):
        self.steps.append(f"Input binary data: {self.data}")

        encoded = conv_encode(self.data)
        self.steps.append(f"Convolutional Encoding Steps:")
        
        for i in range(0, len(encoded), 2):
            pair = encoded[i:i+2]
            self.steps.append(f"Output bits at step {i//2+1}: {pair}")

        flip_index = random.randint(0, len(encoded) - 1)
        noisy = list(encoded)
        noisy[flip_index] = '1' if noisy[flip_index] == '0' else '0'
        noisy = ''.join(noisy)

        self.steps.append(f"Introduced error by flipping bit {flip_index+1}:\n{noisy}")

        decoded = conv_decode(noisy)
        self.steps.append(f"Decoded back to original: {decoded}")

    def animate_reed_solomon(self):
        self.steps.append(f"Input text data: {self.data}")

        encoded = rs_encode(self.data)
        self.steps.append(f"Reed-Solomon Encoded bytes (partial shown):\n{encoded[:10]}...")

        noisy = flip_random_bits(encoded, flip_count=2)
        self.steps.append(f"Introduced noise (flipped random bits)")

        decoded, error = rs_decode(noisy)
        self.steps.append(f"Decoded output: {decoded if decoded else 'Decoding Failed'}")

    def next_step(self):
        self.current_step += 1
        if self.current_step < len(self.steps):
            self.label.setText(self.steps[self.current_step])
            self.progress.setValue(self.current_step + 1)
        else:
            self.label.setText("🎯 Animation Complete!")
            self.next_button.setEnabled(False)
            self.timer.stop()
