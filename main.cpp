#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <random>
#include <functional>
#include "src/SortAlgorithms.h"

// Print all elements in the array (for debugging)
void printArray(const std::vector<int>& arr) {
    for (int i : arr) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
}

// Function to generate random data
std::vector<int> generateRandomData(int size, int min = 1, int max = 10000) {
    std::vector<int> data(size);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(min, max);

    for (int i = 0; i < size; ++i) {
        data[i] = dis(gen);
    }

    return data;
}

// Function to generate sorted data
std::vector<int> generateSortedData(int size) {
    std::vector<int> data(size);
    for (int i = 0; i < size; ++i) {
        data[i] = i + 1;
    }
    return data;
}

// Function to generate reverse sorted data
std::vector<int> generateReverseSortedData(int size) {
    std::vector<int> data(size);
    for (int i = 0; i < size; ++i) {
        data[i] = size - i;
    }
    return data;
}

// Benchmark and record results
void benchmarkAndRecord(std::ofstream& file, const std::vector<int>& original, const std::string& algorithm_name, std::function<void()> sort_func, int input_size, const std::string& input_type) {
    std::vector<int> arr = original;
    auto start = std::chrono::high_resolution_clock::now();
    sort_func(); // Call the sorting algorithm
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;

    file << algorithm_name << "," << input_type << "," << input_size << "," << duration.count() * 1000 << std::endl; // Record result to CSV
}

int main() {
    // Create or open the CSV file
    std::ofstream result_file("benchmark_results.csv");
    result_file << "Algorithm,InputType,InputSize,ExecutionTime(ms)" << std::endl; // Header

    // Define the input sizes and types
    std::vector<int> input_sizes = {10, 50, 100, 1000, 10000}; // Smaller sizes for testing
    std::vector<std::string> input_types = {"Random", "Sorted", "ReverseSorted"};

    // Run benchmarks for each input size and type
    for (int size : input_sizes) {
        for (const std::string& type : input_types) {
            // Generate the appropriate input data
            std::vector<int> input_data;
            if (type == "Random") {
                input_data = generateRandomData(size);
            } else if (type == "Sorted") {
                input_data = generateSortedData(size);
            } else if (type == "ReverseSorted") {
                input_data = generateReverseSortedData(size);
            }

            // Debugging: print input size and type to verify
            std::cout << "Running benchmark for size " << size << " with type " << type << std::endl;

            // Benchmark each sorting algorithm with proper lambda capture by reference
            benchmarkAndRecord(result_file, input_data, "Bubble Sort", [&input_data]() { bubbleSort(input_data); }, size, type);
            benchmarkAndRecord(result_file, input_data, "Insertion Sort", [&input_data]() { insertionSort(input_data); }, size, type);
            benchmarkAndRecord(result_file, input_data, "Selection Sort", [&input_data]() { selectionSort(input_data); }, size, type);
            benchmarkAndRecord(result_file, input_data, "Merge Sort", [&input_data]() { mergeSort(input_data, 0, input_data.size() - 1); }, size, type);
            benchmarkAndRecord(result_file, input_data, "Quick Sort", [&input_data]() { quickSort(input_data, 0, input_data.size() - 1); }, size, type);
            benchmarkAndRecord(result_file, input_data, "Heap Sort", [&input_data]() { heapSort(input_data); }, size, type);
            int maxVal = *std::max_element(input_data.begin(), input_data.end());
            benchmarkAndRecord(result_file, input_data, "Counting Sort", [&input_data, maxVal]() { countingSort(input_data, maxVal); }, size, type);  // Use actual maximum value
            benchmarkAndRecord(result_file, input_data, "Radix Sort", [&input_data]() { radixSort(input_data); }, size, type);
            benchmarkAndRecord(result_file, input_data, "Bucket Sort", [&input_data]() { bucketSort(input_data); }, size, type);
            benchmarkAndRecord(result_file, input_data, "Shell Sort", [&input_data]() { shellSort(input_data); }, size, type);
        }
    }

    // Close the file
    result_file.close();

    std::cout << "Benchmarking complete. Results saved to benchmark_results.csv." << std::endl;
    return 0;
}