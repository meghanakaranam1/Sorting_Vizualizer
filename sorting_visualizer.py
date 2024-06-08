import tkinter as tk
from tkinter import ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("800x600")

        self.array = []
        self.algorithm = tk.StringVar()
        self.animation_speed = tk.DoubleVar(value=0.1)  # Default animation speed
        self.create_widgets()
        self.create_canvas()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        size_label = ttk.Label(control_frame, text="Array Size:")
        size_label.pack(side=tk.LEFT, padx=(10, 5))

        self.size_entry = ttk.Entry(control_frame, width=5)
        self.size_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.size_entry.insert(0, "50")

        algorithm_label = ttk.Label(control_frame, text="Algorithm:")
        algorithm_label.pack(side=tk.LEFT, padx=(10, 5))

        self.algorithm_combobox = ttk.Combobox(control_frame, textvariable=self.algorithm, values=[
            "Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"
        ])
        self.algorithm_combobox.pack(side=tk.LEFT, padx=(0, 10))
        self.algorithm_combobox.current(0)

        generate_button = ttk.Button(control_frame, text="Generate Array", command=self.generate_array)
        generate_button.pack(side=tk.LEFT, padx=5)

        sort_button = ttk.Button(control_frame, text="Sort", command=self.start_sorting)
        sort_button.pack(side=tk.LEFT, padx=5)

        # Animation speed control
        speed_label = ttk.Label(control_frame, text="Animation Speed:")
        speed_label.pack(side=tk.LEFT, padx=(10, 5))

        speed_scale = ttk.Scale(control_frame, from_=0.1, to=2.0, length=200, orient=tk.HORIZONTAL,
                                variable=self.animation_speed, command=self.update_speed)
        speed_scale.pack(side=tk.LEFT, padx=(0, 10))
        speed_scale.set(0.1)  # Set default speed

        # Legend for color representation
        legend_frame = ttk.Frame(self.root)
        legend_frame.pack(side=tk.TOP, fill=tk.X)

        legend_blue = ttk.Label(legend_frame, text="Blue: Unsorted elements")
        legend_blue.pack(side=tk.LEFT, padx=(10, 5))

        legend_orange = ttk.Label(legend_frame, text="Orange: Elements being swapped")
        legend_orange.pack(side=tk.LEFT, padx=(10, 5))

        legend_yellow = ttk.Label(legend_frame, text="Yellow: Elements being compared")
        legend_yellow.pack(side=tk.LEFT, padx=(10, 5))

    def create_canvas(self):
        self.figure, self.ax = plt.subplots()
        self.ax.set_title("Sorting Algorithm Visualization")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def generate_array(self):
        size = int(self.size_entry.get())
        self.array = [random.randint(1, 100) for _ in range(size)]
        self.plot_array()

    def plot_array(self, colorArray=None):
        self.ax.clear()
        colorArray = colorArray if colorArray else ["blue"] * len(self.array)
        self.ax.bar(range(len(self.array)), self.array, color=colorArray)
        self.canvas.draw()

    def start_sorting(self):
        selected_algorithm = self.algorithm.get()
        algorithms = {
            "Bubble Sort": self.bubble_sort,
            "Selection Sort": self.selection_sort,
            "Insertion Sort": self.insertion_sort,
            "Merge Sort": self.merge_sort,
            "Quick Sort": self.quick_sort
        }
        sort_function = algorithms.get(selected_algorithm, self.bubble_sort)
        sort_function()

    def update_speed(self, event):
        # Update animation speed based on the scale value
        self.animation_speed.set(float(event))
        
    def animate_step(self, colorArray, swap_indices=None, compare_indices=None):
        # Function to animate a single step of sorting process
        self.ax.clear()
        self.ax.bar(range(len(self.array)), self.array, color=colorArray)
        
        # Highlight elements being swapped
        if swap_indices:
            for idx in swap_indices:
                self.ax.patches[idx].set_color('orange')
                
        # Highlight elements being compared
        if compare_indices:
            for idx in compare_indices:
                self.ax.patches[idx].set_color('yellow')
        
        self.canvas.draw()
        self.root.update()
        time.sleep(self.animation_speed.get())

    def bubble_sort(self):
        array_length = len(self.array)
        for i in range(array_length):
            for j in range(0, array_length - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.animate_step(["blue"] * len(self.array), swap_indices=[j, j+1])
                else:
                    self.animate_step(["blue"] * len(self.array), compare_indices=[j, j+1])

    def selection_sort(self):
        array_length = len(self.array)
        for i in range(array_length):
            min_idx = i
            for j in range(i + 1, array_length):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            self.animate_step(["blue"] * len(self.array), swap_indices=[i, min_idx])

    def insertion_sort(self):
        array_length = len(self.array)
        for i in range(1, array_length):
            key = self.array[i]
            j = i - 1
            while j >= 0 and key < self.array[j]:
                self.array[j + 1] = self.array[j]
                j -= 1
            self.array[j + 1] = key
            self.animate_step(["blue"] * len(self.array), swap_indices=[j+1, i])

    def merge_sort(self, left=0, right=None):
        if right is None:
            right = len(self.array) - 1
        if left < right:
            middle = (left + right) // 2
            self.merge_sort(left, middle)
            self.merge_sort(middle + 1, right)
            self.merge(left, middle, right)
            self.animate_step(["green" if x >= left and x <= right else "blue" for x in range(len(self.array))])

    def merge(self, left, middle, right):
        left_sub = self.array[left:middle + 1]
        right_sub = self.array[middle + 1:right + 1]
        left_idx, right_idx, merge_idx = 0, 0, left

        while left_idx < len(left_sub) and right_idx < len(right_sub):
            if left_sub[left_idx] <= right_sub[right_idx]:
                self.array[merge_idx] = left_sub[left_idx]
                left_idx += 1
            else:
                self.array[merge_idx] = right_sub[right_idx]
                right_idx += 1
            merge_idx += 1

        while left_idx < len(left_sub):
            self.array[merge_idx] = left_sub[left_idx]
            left_idx += 1
            merge_idx += 1

        while right_idx < len(right_sub):
            self.array[merge_idx] = right_sub[right_idx]
            right_idx += 1
            merge_idx += 1

    def quick_sort(self, low=0, high=None):
        if high is None:
            high = len(self.array) - 1
        if low < high:
            pivot_index = self.partition(low, high)
            self.animate_step(["green" if x == pivot_index else "blue" for x in range(len(self.array))])
            self.quick_sort(low, pivot_index - 1)
            self.quick_sort(pivot_index + 1, high)

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
