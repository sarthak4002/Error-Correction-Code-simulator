import matplotlib.pyplot as plt

def plot_error_patterns(original, noisy, decoded, title="Error Pattern Visualization"):
    fig, axs = plt.subplots(3, 1, figsize=(10, 6), sharex=True)

    axs[0].plot(list(map(int, original)), marker='o', linestyle='-', color='blue')
    axs[0].set_title('Original Data')

    axs[1].plot(list(map(int, noisy)), marker='o', linestyle='-', color='red')
    axs[1].set_title('Noisy Data')

    axs[2].plot(list(map(int, decoded)), marker='o', linestyle='-', color='green')
    axs[2].set_title('Decoded Data')

    plt.suptitle(title, fontsize=16)
    plt.xlabel('Bit Position')
    plt.tight_layout()
    plt.show()
