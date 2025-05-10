import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ecc.stats_tracker import get_success_rates  # <-- New import

# ===============================
# 🟩 1. Bit-by-Bit Visualization
# ===============================
def visualize_bits(title, labels, sequences, highlights=None):
    fig, ax = plt.subplots(figsize=(12, len(sequences)))

    for i, seq in enumerate(sequences):
        for j, bit in enumerate(seq):
            color = 'red' if highlights and highlights[i][j] else 'green'
            ax.text(j, -i, bit, ha='center', va='center', fontsize=12,
                    bbox=dict(facecolor=color, alpha=0.6))
    
    ax.set_xlim(-1, max(len(seq) for seq in sequences))
    ax.set_ylim(-len(sequences)+0.5, 1)
    ax.axis('off')
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


# ========================================
# 📊 2. Live Accuracy Dashboard (NEW)
# ========================================
def show_live_accuracy_dashboard():
    def animate(i):
        plt.cla()
        data = get_success_rates()
        ecc_types = list(data.keys())
        values = list(data.values())
        plt.bar(ecc_types, values, color='skyblue')
        plt.ylim(0, 100)
        plt.ylabel("Success Rate (%)")
        plt.title("ECC Live Accuracy Dashboard")
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.show()
