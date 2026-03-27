import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Patch


# =========================
# Visual configuration
# =========================
COLORS = {
    "default": "#4C78A8",   # xanh mặc định
    "compare": "#F58518",   # cam
    "swap": "#E45756",      # đỏ
    "pivot": "#B279A2",     # tím
    "sorted": "#54A24B",    # xanh lá
    "write": "#72B7B2",     # xanh ngọc
}

ROLE_PRIORITY = ["sorted", "pivot", "swap", "write", "compare"]


# =========================
# Frame helpers
# =========================
def make_frame(state, highlights=None, note=""):
    """
    state: list[int]
    highlights: dict[str, list[int] | int]  vd:
        {"compare": [2, 3], "pivot": 7, "sorted": [8, 9]}
    """
    return (state.copy(), highlights or {}, note)


def sanitize_filename(name):
    return name.lower().replace(" ", "_").replace("/", "_")


def normalize_indices(indices, n):
    if indices is None:
        return set()
    if isinstance(indices, int):
        return {indices} if 0 <= indices < n else set()

    result = set()
    for idx in indices:
        if 0 <= idx < n:
            result.add(idx)
    return result


def normalize_highlights(highlights, n):
    normalized = {}
    for role, indices in highlights.items():
        normalized[role] = normalize_indices(indices, n)
    return normalized


# =========================
# Sorting algorithms
# =========================
def bubble_sort_visualize(arr):
    arr = list(arr)
    frames = []
    n = len(arr)

    if n == 0:
        return frames

    frames.append(make_frame(arr, {}, "Initial array"))

    for i in range(n):
        swapped = False
        sorted_tail = list(range(n - i, n)) if i > 0 else []

        for j in range(0, n - i - 1):
            frames.append(
                make_frame(
                    arr,
                    {"compare": [j, j + 1], "sorted": sorted_tail},
                    f"Compare indices {j} and {j + 1}",
                )
            )

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                frames.append(
                    make_frame(
                        arr,
                        {"swap": [j, j + 1], "sorted": sorted_tail},
                        f"Swap indices {j} and {j + 1}",
                    )
                )

        if not swapped:
            remaining_sorted = list(range(0, n - i))
            frames.append(make_frame(arr, {"sorted": remaining_sorted + sorted_tail}, "Already sorted"))
            break

        frames.append(
            make_frame(
                arr,
                {"sorted": list(range(n - i - 1, n))},
                f"Index {n - i - 1} fixed",
            )
        )

    frames.append(make_frame(arr, {"sorted": list(range(n))}, "Sorted"))
    return frames


def selection_sort_visualize(arr):
    arr = list(arr)
    frames = []
    n = len(arr)

    if n == 0:
        return frames

    frames.append(make_frame(arr, {}, "Initial array"))

    for i in range(n):
        min_index = i
        sorted_prefix = list(range(i))

        frames.append(
            make_frame(
                arr,
                {"pivot": min_index, "sorted": sorted_prefix},
                f"Start pass at index {i}",
            )
        )

        for j in range(i + 1, n):
            frames.append(
                make_frame(
                    arr,
                    {"compare": [min_index, j], "pivot": min_index, "sorted": sorted_prefix},
                    f"Compare current minimum {min_index} with index {j}",
                )
            )

            if arr[j] < arr[min_index]:
                min_index = j
                frames.append(
                    make_frame(
                        arr,
                        {"pivot": min_index, "sorted": sorted_prefix},
                        f"New minimum found at index {min_index}",
                    )
                )

        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            frames.append(
                make_frame(
                    arr,
                    {"swap": [i, min_index], "sorted": sorted_prefix},
                    f"Swap indices {i} and {min_index}",
                )
            )

        frames.append(
            make_frame(
                arr,
                {"sorted": list(range(i + 1))},
                f"Index {i} fixed",
            )
        )

    frames.append(make_frame(arr, {"sorted": list(range(n))}, "Sorted"))
    return frames


def insertion_sort_visualize(arr):
    arr = list(arr)
    frames = []
    n = len(arr)

    if n == 0:
        return frames

    frames.append(make_frame(arr, {}, "Initial array"))
    frames.append(make_frame(arr, {"sorted": [0]}, "First element is trivially sorted"))

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        frames.append(
            make_frame(
                arr,
                {"pivot": i, "sorted": list(range(i))},
                f"Insert value {key} from index {i}",
            )
        )

        while j >= 0 and arr[j] > key:
            frames.append(
                make_frame(
                    arr,
                    {"compare": [j, j + 1], "sorted": list(range(j + 1))},
                    f"Compare key {key} with index {j}",
                )
            )

            arr[j + 1] = arr[j]
            frames.append(
                make_frame(
                    arr,
                    {"write": [j, j + 1], "sorted": list(range(j + 1))},
                    f"Shift value from index {j} to {j + 1}",
                )
            )
            j -= 1

        arr[j + 1] = key
        frames.append(
            make_frame(
                arr,
                {"pivot": j + 1, "sorted": list(range(i + 1))},
                f"Place key at index {j + 1}",
            )
        )

    frames.append(make_frame(arr, {"sorted": list(range(n))}, "Sorted"))
    return frames


def merge_sort_visualize(arr):
    a = list(arr)
    frames = []
    n = len(a)

    if n == 0:
        return frames

    temp = a.copy()
    frames.append(make_frame(a, {}, "Initial array"))

    def merge_sort(left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        merge_sort(left, mid)
        merge_sort(mid + 1, right)
        merge(left, mid, right)

    def merge(left, mid, right):
        i, j, k = left, mid + 1, left

        frames.append(
            make_frame(
                a,
                {"pivot": list(range(left, right + 1))},
                f"Merge range {left}-{right}",
            )
        )

        while i <= mid and j <= right:
            frames.append(
                make_frame(
                    a,
                    {"compare": [i, j], "pivot": list(range(left, right + 1))},
                    f"Compare left[{i}] and right[{j}]",
                )
            )

            if a[i] <= a[j]:
                temp[k] = a[i]
                chosen = i
                i += 1
            else:
                temp[k] = a[j]
                chosen = j
                j += 1

            frames.append(
                make_frame(
                    a,
                    {"write": [k], "pivot": list(range(left, right + 1))},
                    f"Write next merged value into index {k}",
                )
            )
            k += 1

        while i <= mid:
            temp[k] = a[i]
            frames.append(
                make_frame(
                    a,
                    {"write": [k], "pivot": list(range(left, right + 1))},
                    f"Copy remaining left value into index {k}",
                )
            )
            i += 1
            k += 1

        while j <= right:
            temp[k] = a[j]
            frames.append(
                make_frame(
                    a,
                    {"write": [k], "pivot": list(range(left, right + 1))},
                    f"Copy remaining right value into index {k}",
                )
            )
            j += 1
            k += 1

        for idx in range(left, right + 1):
            a[idx] = temp[idx]

        frames.append(
            make_frame(
                a,
                {"sorted": list(range(left, right + 1))},
                f"Merged range {left}-{right}",
            )
        )

    merge_sort(0, n - 1)
    frames.append(make_frame(a, {"sorted": list(range(n))}, "Sorted"))
    return frames


def quick_sort_visualize(arr):
    arr = list(arr)
    frames = []
    n = len(arr)

    if n == 0:
        return frames

    frames.append(make_frame(arr, {}, "Initial array"))

    def quick_sort(low, high):
        if low < high:
            pivot_index = partition(low, high)
            quick_sort(low, pivot_index - 1)
            quick_sort(pivot_index + 1, high)
        elif low == high:
            frames.append(make_frame(arr, {"sorted": [low]}, f"Index {low} fixed"))

    def partition(low, high):
        pivot = arr[high]
        i = low - 1

        frames.append(
            make_frame(
                arr,
                {"pivot": high},
                f"Choose pivot {pivot} at index {high}",
            )
        )

        for j in range(low, high):
            frames.append(
                make_frame(
                    arr,
                    {"compare": [j], "pivot": high},
                    f"Compare index {j} with pivot",
                )
            )

            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    frames.append(
                        make_frame(
                            arr,
                            {"swap": [i, j], "pivot": high},
                            f"Swap indices {i} and {j}",
                        )
                    )

        if i + 1 != high:
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            frames.append(
                make_frame(
                    arr,
                    {"swap": [i + 1, high]},
                    f"Place pivot at index {i + 1}",
                )
            )

        frames.append(
            make_frame(
                arr,
                {"sorted": [i + 1]},
                f"Pivot fixed at index {i + 1}",
            )
        )
        return i + 1

    quick_sort(0, n - 1)
    frames.append(make_frame(arr, {"sorted": list(range(n))}, "Sorted"))
    return frames


def heap_sort_visualize(arr):
    arr = list(arr)
    frames = []
    n = len(arr)

    if n == 0:
        return frames

    frames.append(make_frame(arr, {}, "Initial array"))

    def heapify(heap_size, root_index, sorted_tail=None):
        if sorted_tail is None:
            sorted_tail = []

        largest = root_index
        left = 2 * root_index + 1
        right = 2 * root_index + 2

        frames.append(
            make_frame(
                arr,
                {"pivot": root_index, "sorted": sorted_tail},
                f"Heapify at root {root_index}",
            )
        )

        if left < heap_size:
            frames.append(
                make_frame(
                    arr,
                    {"compare": [largest, left], "sorted": sorted_tail},
                    f"Compare root {largest} with left child {left}",
                )
            )
            if arr[left] > arr[largest]:
                largest = left

        if right < heap_size:
            frames.append(
                make_frame(
                    arr,
                    {"compare": [largest, right], "sorted": sorted_tail},
                    f"Compare current largest {largest} with right child {right}",
                )
            )
            if arr[right] > arr[largest]:
                largest = right

        if largest != root_index:
            arr[root_index], arr[largest] = arr[largest], arr[root_index]
            frames.append(
                make_frame(
                    arr,
                    {"swap": [root_index, largest], "sorted": sorted_tail},
                    f"Swap {root_index} and {largest}",
                )
            )
            heapify(heap_size, largest, sorted_tail)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    frames.append(make_frame(arr, {"pivot": [0]}, "Max heap built"))

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        frames.append(
            make_frame(
                arr,
                {"swap": [0, end], "sorted": list(range(end, n))},
                f"Move current max to index {end}",
            )
        )
        heapify(end, 0, list(range(end, n)))

    frames.append(make_frame(arr, {"sorted": list(range(n))}, "Sorted"))
    return frames


def radix_sort_visualize(arr):
    original = list(arr)
    frames = []
    n = len(original)

    if n == 0:
        return frames

    min_value = min(original)
    shift = -min_value if min_value < 0 else 0
    adjusted = [value + shift for value in original]

    frames.append(make_frame(original, {}, "Initial array"))

    def counting_sort(exp):
        output = [0] * n
        count = [0] * 10

        for value in adjusted:
            digit = (value // exp) % 10
            count[digit] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            digit = (adjusted[i] // exp) % 10
            output[count[digit] - 1] = adjusted[i]
            count[digit] -= 1

        adjusted[:] = output

    max_num = max(adjusted)
    exp = 1

    while max_num // exp > 0:
        frames.append(
            make_frame(
                [value - shift for value in adjusted],
                {"pivot": list(range(n))},
                f"Process digit place {exp}",
            )
        )
        counting_sort(exp)
        frames.append(
            make_frame(
                [value - shift for value in adjusted],
                {"write": list(range(n))},
                f"Array reordered by digit place {exp}",
            )
        )
        exp *= 10

    frames.append(make_frame([value - shift for value in adjusted], {"sorted": list(range(n))}, "Sorted"))
    return frames


def bucket_sort_visualize(arr):
    arr = list(arr)
    frames = []
    n = len(arr)

    if n == 0:
        return frames

    frames.append(make_frame(arr, {}, "Initial array"))

    min_value = min(arr)
    max_value = max(arr)

    if min_value == max_value:
        frames.append(make_frame(arr, {"sorted": list(range(n))}, "All values are equal"))
        return frames

    bucket_count = n
    buckets = [[] for _ in range(bucket_count)]

    def get_bucket_index(value):
        normalized = (value - min_value) / (max_value - min_value)
        return min(bucket_count - 1, int(normalized * bucket_count))

    for idx, value in enumerate(arr):
        bucket_index = get_bucket_index(value)
        buckets[bucket_index].append(value)

        placed = [item for bucket in buckets for item in bucket]
        snapshot = placed + arr[idx + 1:]
        active = [len(placed) - 1] if placed else []

        frames.append(
            make_frame(
                snapshot,
                {"pivot": active},
                f"Put value {value} into bucket {bucket_index}",
            )
        )

    sorted_prefix = []
    for bucket_index, bucket in enumerate(buckets):
        if not bucket:
            continue

        bucket.sort()
        start = len(sorted_prefix)
        sorted_prefix.extend(bucket)
        remaining = [item for later_bucket in buckets[bucket_index + 1:] for item in later_bucket]
        snapshot = sorted_prefix + remaining

        frames.append(
            make_frame(
                snapshot,
                {
                    "write": list(range(start, len(sorted_prefix))),
                    "sorted": list(range(start))
                },
                f"Sort bucket {bucket_index}",
            )
        )

    arr[:] = sorted_prefix
    frames.append(make_frame(arr, {"sorted": list(range(n))}, "Sorted"))
    return frames


# =========================
# Animation
# =========================
def animate_sort_algorithm(arr, sort_function, algorithm_name, interval=500, show_values=True):
    arr = list(arr)

    if len(arr) == 0:
        print(f"Skip {algorithm_name}: empty array.")
        return

    frames = sort_function(arr)
    if not frames:
        print(f"Error: No frames generated for {algorithm_name}")
        return

    fig, ax = plt.subplots(figsize=(12, 7))
    x_positions = list(range(len(arr)))
    initial_state = frames[0][0]

    bars = ax.bar(
        x_positions,
        initial_state,
        color=COLORS["default"],
        edgecolor="black",
        linewidth=0.8
    )

    min_val = min(min(frame[0]) for frame in frames)
    max_val = max(max(frame[0]) for frame in frames)
    value_range = max_val - min_val
    padding = max(1, value_range * 0.15 if value_range != 0 else 1)

    ax.set_xlim(-0.6, len(arr) - 0.4)
    ax.set_ylim(min(0, min_val - padding), max_val + padding)
    ax.set_xticks(x_positions)
    ax.set_title(f"{algorithm_name} Visualization", fontsize=16, fontweight="bold", pad=28)
    ax.set_ylabel("Value")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    legend_handles = [
        Patch(facecolor=COLORS["compare"], edgecolor="black", label="Compare"),
        Patch(facecolor=COLORS["swap"], edgecolor="black", label="Swap"),
        Patch(facecolor=COLORS["pivot"], edgecolor="black", label="Pivot"),
        Patch(facecolor=COLORS["write"], edgecolor="black", label="Write"),
        Patch(facecolor=COLORS["sorted"], edgecolor="black", label="Sorted"),
    ]

    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.06),
        ncol=5,
        frameon=False,
        fontsize=9
    )

    note_text = ax.text(
        0.5, -0.12, "",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=11
    )

    value_labels = []
    if show_values:
        for x, v in zip(x_positions, initial_state):
            y = v + padding * 0.05 if v >= 0 else v - padding * 0.05
            va = "bottom" if v >= 0 else "top"
            txt = ax.text(
                x, y, str(v),
                ha="center",
                va=va,
                fontsize=9,
                fontweight="bold"
            )
            value_labels.append(txt)

    def resolve_color(index, highlights):
        for role in ROLE_PRIORITY:
            if index in highlights.get(role, set()):
                return COLORS[role]
        return COLORS["default"]

    def update(frame):
        state, raw_highlights, note = frame
        highlights = normalize_highlights(raw_highlights, len(state))

        for idx, (bar, value) in enumerate(zip(bars, state)):
            bar.set_height(value)
            bar.set_color(resolve_color(idx, highlights))

            if show_values:
                y = value + padding * 0.05 if value >= 0 else value - padding * 0.05
                va = "bottom" if value >= 0 else "top"
                value_labels[idx].set_position((idx, y))
                value_labels[idx].set_text(str(value))
                value_labels[idx].set_verticalalignment(va)

        note_text.set_text(note)
        return list(bars) + value_labels + [note_text]

    fig.subplots_adjust(top=0.80, bottom=0.18)

    ani = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=interval,
        repeat=False,
        blit=False
    )

    fps = max(1, round(1000 / interval))
    filename = f"{sanitize_filename(algorithm_name)}_visualization.gif"
    ani.save(filename, writer="pillow", fps=fps)
    plt.close(fig)

    print(f"Saved: {filename}")


# =========================
# Main
# =========================
if __name__ == "__main__":
    arr = np.random.randint(1, 100, 20).tolist()
    interval_value = 500

    algorithms = [
        ("Bubble Sort", bubble_sort_visualize),
        ("Selection Sort", selection_sort_visualize),
        ("Insertion Sort", insertion_sort_visualize),
        ("Merge Sort", merge_sort_visualize),
        ("Quick Sort", quick_sort_visualize),
        ("Heap Sort", heap_sort_visualize),
        ("Radix Sort", radix_sort_visualize),
        ("Bucket Sort", bucket_sort_visualize),
    ]

    for name, func in algorithms:
        animate_sort_algorithm(
            arr,
            func,
            name,
            interval=interval_value,
            show_values=True
        )