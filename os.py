import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PageReplacementSimulator:
    def __init__(self, master):
        try:
            self.master = master
            master.title("Page Replacement Algorithm Simulator")
            master.geometry("1000x700")

            # Page Reference String Frame
            ref_frame = ttk.LabelFrame(master, text="Page Reference String")
            ref_frame.pack(padx=10, pady=10, fill="x")

            # Input for page reference string
            ttk.Label(ref_frame, text="Enter Page Reference String (space-separated):").pack(side=tk.LEFT, padx=5)
            self.ref_string_entry = ttk.Entry(ref_frame, width=50)
            self.ref_string_entry.pack(side=tk.LEFT, padx=5)
            self.ref_string_entry.insert(0, "7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1")

            # Frame Size Input
            ttk.Label(ref_frame, text="Frame Size:").pack(side=tk.LEFT, padx=5)
            self.frame_size_entry = ttk.Entry(ref_frame, width=5)
            self.frame_size_entry.pack(side=tk.LEFT, padx=5)
            self.frame_size_entry.insert(0, "3")

            # Simulate Button
            ttk.Button(ref_frame, text="Simulate", command=self.simulate_algorithms).pack(side=tk.LEFT, padx=10)

            # Results Frame
            self.results_frame = ttk.Frame(master)
            self.results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Initialization Error", str(e))

    def fifo_algorithm(self, pages, frame_size):
        try:
            frames = []
            page_faults = 0
            fault_timeline = []

            for i, page in enumerate(pages):
                if page not in frames:
                    page_faults += 1
                    if len(frames) < frame_size:
                        frames.append(page)
                    else:
                        frames.pop(0)
                        frames.append(page)
                fault_timeline.append(page_faults)
            
            return page_faults, fault_timeline
        except Exception as e:
            messagebox.showerror("FIFO Algorithm Error", str(e))
            return 0, []

    def lru_algorithm(self, pages, frame_size):
        try:
            frames = []
            page_faults = 0
            fault_timeline = []

            for page in pages:
                if page not in frames:
                    page_faults += 1
                    if len(frames) < frame_size:
                        frames.append(page)
                    else:
                        lru_page = min(frames, key=lambda x: pages.index(x) if x in pages[:pages.index(page)] else float('inf'))
                        frames.remove(lru_page)
                        frames.append(page)
                else:
                    frames.remove(page)
                    frames.append(page)
                fault_timeline.append(page_faults)
            
            return page_faults, fault_timeline
        except Exception as e:
            messagebox.showerror("LRU Algorithm Error", str(e))
            return 0, []

    def optimal_algorithm(self, pages, frame_size):
        try:
            frames = []
            page_faults = 0
            fault_timeline = []

            for i, page in enumerate(pages):
                if page not in frames:
                    page_faults += 1
                    if len(frames) < frame_size:
                        frames.append(page)
                    else:
                        max_distance_page = self.find_optimal_replacement(pages[i+1:], frames)
                        frames.remove(max_distance_page)
                        frames.append(page)
                fault_timeline.append(page_faults)
            
            return page_faults, fault_timeline
        except Exception as e:
            messagebox.showerror("Optimal Algorithm Error", str(e))
            return 0, []

    def find_optimal_replacement(self, future_pages, current_frames):
        try:
            max_distance = -1
            replace_page = current_frames[0]

            for frame in current_frames:
                try:
                    distance = future_pages.index(frame)
                except ValueError:
                    return frame
                
                if distance > max_distance:
                    max_distance = distance
                    replace_page = frame
            
            return replace_page
        except Exception as e:
            messagebox.showerror("Optimal Replacement Error", str(e))
            return current_frames[0]

    def simulate_algorithms(self):
        try:
            # Clear previous results
            for widget in self.results_frame.winfo_children():
                widget.destroy()

            # Get input values
            ref_string = list(map(int, self.ref_string_entry.get().split()))
            frame_size = int(self.frame_size_entry.get())

            # Run algorithms
            fifo_faults, fifo_timeline = self.fifo_algorithm(ref_string, frame_size)
            lru_faults, lru_timeline = self.lru_algorithm(ref_string, frame_size)
            optimal_faults, optimal_timeline = self.optimal_algorithm(ref_string, frame_size)

            # Create visualization
            plt.close('all')  # Close any existing plots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            
            # Fault Comparison Bar Chart
            algorithms = ['FIFO', 'LRU', 'Optimal']
            faults = [fifo_faults, lru_faults, optimal_faults]
            ax1.bar(algorithms, faults, color=['blue', 'green', 'red'])
            ax1.set_ylabel('Number of Page Faults')
            ax1.set_title('Page Fault Comparison')

            # Fault Timeline Plot
            ax2.plot(fifo_timeline, label='FIFO', marker='o')
            ax2.plot(lru_timeline, label='LRU', marker='s')
            ax2.plot(optimal_timeline, label='Optimal', marker='^')
            ax2.set_xlabel('Page Reference')
            ax2.set_ylabel('Cumulative Page Faults')
            ax2.set_title('Page Fault Timeline')
            ax2.legend()

            plt.tight_layout()

            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.results_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)

            # Results Text
            results_text = f"""
            Page Replacement Algorithm Results:
            Reference String: {ref_string}
            Frame Size: {frame_size}

            Page Faults:
            FIFO: {fifo_faults}
            LRU: {lru_faults}
            Optimal: {optimal_faults}
            """
            ttk.Label(self.results_frame, text=results_text, wraplength=900).pack()

        except Exception as e:
            messagebox.showerror("Simulation Error", str(e))

def main():
    try:
        import tkinter as tk  # Ensure tkinter is installed
    except ImportError:
        print("Error: tkinter is not installed. Install it using 'sudo apt install python3-tk' on Linux or check Python installation on macOS/Windows.")
        return

    try:
        root = tk.Tk()
        app = PageReplacementSimulator(root)
        root.mainloop()
    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == "__main__":
    print("Running Page Replacement Simulator... Open the GUI window to proceed.")
    main()