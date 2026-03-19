import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# Bubble Sort Algorithm with visualization
def bubble_sort_visualize(arr):
    frames = []  # To store the frames for the animation

    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                frames.append(arr.copy())
    return frames

# Selection Sort Algorithm with visualization
def selection_sort_visualize(arr):
    frames = []
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
        frames.append(arr.copy())
    return frames

# Insertion Sort Algorithm with visualization
def insertion_sort_visualize(arr):
    frames = []
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        frames.append(arr.copy())
    return frames

# Merge Sort Algorithm with visualization
def merge_sort_visualize(arr):
    frames = []
    
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        merged = merge(left, right)
        frames.append(merged)
        return merged

    def merge(left, right):
        result = []
        while len(left) > 0 and len(right) > 0:
            if left[0] < right[0]:
                result.append(left[0]) 
                left = left[1:]  
            else:
                result.append(right[0])  
                right = right[1:] 
        result.extend(left)
        result.extend(right)  
        return result

    merge_sort(arr)
    return frames

# Quick Sort Algorithm with visualization
def quick_sort_visualize(arr):
    frames = []
    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[low]
        left = low + 1
        right = high
        done = False
        while not done:
            while left <= right and arr[left] <= pivot:
                left = left + 1
            while arr[right] > pivot:
                right = right - 1
            if left <= right:
                arr[left], arr[right] = arr[right], arr[left]
            else:
                done = True
        arr[low], arr[right] = arr[right], arr[low]
        frames.append(arr.copy())
        return right

    quick_sort(arr, 0, len(arr) - 1)
    return frames


# Heap Sort Algorithm with visualization
def heap_sort_visualize(arr):
    frames = []

    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            frames.append(arr.copy())
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        frames.append(arr.copy())
        heapify(arr, i, 0)

    return frames

# Radix Sort Algorithm with visualization
def radix_sort_visualize(arr):
    frames = []
    max_num = max(arr)

    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1

        for i in range(n):
            arr[i] = output[i]

    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        frames.append(arr.copy())
        exp *= 10

    return frames

# Bucket Sort Algorithm with visualization
def bucket_sort_visualize(arr):
    frames = []
    max_value = max(arr)
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]

    for num in arr:
        index = int(num * bucket_count / (max_value + 1))
        buckets[index].append(num)

    for i in range(bucket_count):
        buckets[i].sort()
        frames.append([item for sublist in buckets for item in sublist])  # Flatten the list

    return frames
# Function to plot the array for each frame
def plot_frame(arr, ax):
    ax.clear()  # Clear the previous plot
    ax.bar(range(len(arr)), arr, color="blue")  # Plot the array as bars
    ax.set_title("Sorting Visualization")
    ax.set_ylim(0, max(arr) + 1)  # Ensure bars don't exceed the Y-axis limit

# Function to animate and save GIF for a sorting algorithm
def animate_sort_algorithm(arr, sort_function, algorithm_name, interval=200):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create the frames for animation using the sort function
    frames = sort_function(arr.copy())
    
    # Create the animation
    ani = FuncAnimation(fig, lambda i: plot_frame(frames[i], ax), frames=len(frames), interval=interval, repeat=False)
    
    # Save the animation as a GIF
    ani.save(f'{algorithm_name.lower().replace(" ", "_")}_visualization.gif', writer='pillow', fps=20)  # Save the GIF at 20fps
    plt.close()

# Generate a random array for testing
arr = np.random.randint(1, 100, 20)

# Call the animation function for each sorting algorithm
animate_sort_algorithm(arr, bubble_sort_visualize, "Bubble Sort", interval=200)
animate_sort_algorithm(arr, selection_sort_visualize, "Selection Sort", interval=200)
animate_sort_algorithm(arr, insertion_sort_visualize, "Insertion Sort", interval=200)
animate_sort_algorithm(arr, merge_sort_visualize, "Merge Sort", interval=300)
animate_sort_algorithm(arr, quick_sort_visualize, "Quick Sort", interval=300)

# Call the animation functions for the new sorting algorithms
animate_sort_algorithm(arr, heap_sort_visualize, "Heap Sort", interval=300)
animate_sort_algorithm(arr, radix_sort_visualize, "Radix Sort", interval=300)
animate_sort_algorithm(arr, bucket_sort_visualize, "Bucket Sort", interval=300)