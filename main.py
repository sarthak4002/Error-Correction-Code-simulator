# main.py
from ui.window import launch_app
from ui.bitplot import visualize_bits, show_live_accuracy_dashboard

# To show bit visualization
# visualize_bits("Hamming Demo", ["Input", "Encoded"], [["1", "0", "1"], ["1", "1", "0"]], highlights=[[False, True, False], [True, False, True]])

# To launch the live dashboard
show_live_accuracy_dashboard()

if __name__ == "__main__":
    launch_app()
