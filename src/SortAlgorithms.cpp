// SortAlgorithms.cpp
#include "SortAlgorithms.h"
#include <algorithm> // For std::swap, std::sort, std::min_element, std::max_element

// Bubble Sort algorithm
void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            // Swap adjacent elements if they are in the wrong order
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// Insertion Sort algorithm
void insertionSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;

        // Shift elements greater than key to the right
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }

        // Insert key into its correct position
        arr[j + 1] = key;
    }
}

// Selection Sort algorithm
void selectionSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;

        // Find the index of the smallest element in the unsorted part
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }

        // Place the smallest element at the beginning
        std::swap(arr[i], arr[minIdx]);
    }
}

// Merge two sorted subarrays for Merge Sort
void merge(std::vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    std::vector<int> L(n1), R(n2);

    // Copy data into temporary arrays
    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (int i = 0; i < n2; i++)
        R[i] = arr[mid + 1 + i];

    int i = 0, j = 0, k = left;

    // Merge the temporary arrays back into arr
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy any remaining elements of L
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copy any remaining elements of R
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

// Merge Sort algorithm
void mergeSort(std::vector<int>& arr, int left, int right) {
    // Base case: one or zero elements
    if (left >= right) return;

    int mid = left + (right - left) / 2;

    // Sort both halves recursively
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);

    // Merge the sorted halves
    merge(arr, left, mid, right);
}

// Partition function for Quick Sort
int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high]; // Choose the last element as pivot
    int i = low - 1;

    // Move elements smaller than or equal to pivot to the left
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }

    // Place the pivot in its correct position
    std::swap(arr[i + 1], arr[high]);
    return (i + 1);
}

// Quick Sort algorithm
void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        // Recursively sort the left and right partitions
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// Heapify function for Heap Sort
void heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;       // Assume the root is the largest
    int left = 2 * i + 1;  // Left child
    int right = 2 * i + 2; // Right child

    // Check if left child is larger than root
    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }

    // Check if right child is larger than the current largest
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }

    // If root is not the largest, swap and continue heapifying
    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

// Heap Sort algorithm
void heapSort(std::vector<int>& arr) {
    int n = arr.size();

    // Build a max heap
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }

    // Extract elements one by one from the heap
    for (int i = n - 1; i > 0; i--) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

// Counting Sort algorithm
void countingSort(std::vector<int>& arr, int k) {
    int n = arr.size();
    std::vector<int> count(k + 1, 0);
    std::vector<int> output(n);

    // Count occurrences of each value
    for (int i = 0; i < n; i++) {
        count[arr[i]]++;
    }

    // Compute cumulative counts
    for (int i = 1; i <= k; i++) {
        count[i] += count[i - 1];
    }

    // Build the output array in stable order
    for (int i = n - 1; i >= 0; i--) {
        output[count[arr[i]] - 1] = arr[i];
        count[arr[i]]--;
    }

    // Copy the result back to the original array
    for (int i = 0; i < n; i++) {
        arr[i] = output[i];
    }
}

// Counting Sort by digit for Radix Sort
void countingSortRadix(std::vector<int>& arr, int exp) {
    int n = arr.size();
    std::vector<int> output(n);
    int count[10] = {0};

    // Count occurrences of digits at the current place value
    for (int i = 0; i < n; i++) {
        count[(arr[i] / exp) % 10]++;
    }

    // Compute cumulative counts
    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    // Build the output array in stable order
    for (int i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }

    // Copy the result back to the original array
    for (int i = 0; i < n; i++) {
        arr[i] = output[i];
    }
}

// Radix Sort algorithm
void radixSort(std::vector<int>& arr) {
    // Return immediately if the array is empty
    if (arr.empty()) return;

    int maxVal = *std::max_element(arr.begin(), arr.end());

    // Sort by each digit from least significant to most significant
    for (int exp = 1; maxVal / exp > 0; exp *= 10) {
        countingSortRadix(arr, exp);
    }
}

// Bucket Sort algorithm
void bucketSort(std::vector<int>& arr) {
    int n = arr.size();
    if (n <= 1) return;

    // Find the minimum and maximum values in the array
    int minVal = *std::min_element(arr.begin(), arr.end());
    int maxVal = *std::max_element(arr.begin(), arr.end());

    // Create buckets
    int bucketCount = (maxVal - minVal) / n + 1;
    std::vector<std::vector<int>> buckets(bucketCount);

    // Distribute elements into buckets
    for (int i = 0; i < n; i++) {
        int idx = (arr[i] - minVal) / n;
        buckets[idx].push_back(arr[i]);
    }

    // Sort each bucket and merge them back into the original array
    int idx = 0;
    for (int i = 0; i < bucketCount; i++) {
        std::sort(buckets[i].begin(), buckets[i].end());
        for (int j = 0; j < buckets[i].size(); j++) {
            arr[idx++] = buckets[i][j];
        }
    }
}

// Shell Sort algorithm
void shellSort(std::vector<int>& arr) {
    int n = arr.size();

    // Reduce the gap and perform insertion sort on each gap group
    for (int gap = n / 2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i++) {
            int temp = arr[i];
            int j;

            // Shift earlier gap-sorted elements up until the correct position is found
            for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
                arr[j] = arr[j - gap];
            }

            // Place temp in its correct position
            arr[j] = temp;
        }
    }
}