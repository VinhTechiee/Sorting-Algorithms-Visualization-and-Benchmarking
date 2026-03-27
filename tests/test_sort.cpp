#include "catch_amalgamated.hpp"
#include <vector>
#include <algorithm>
#include "../src/SortAlgorithms.h"

void expectSorted(void (*sortFn)(std::vector<int>&), std::vector<int> arr) {
    std::vector<int> expected = arr;
    std::sort(expected.begin(), expected.end());

    sortFn(arr);
    REQUIRE(arr == expected);
}

void runMergeSort(std::vector<int>& arr) {
    mergeSort(arr, 0, static_cast<int>(arr.size()) - 1);
}

void runQuickSort(std::vector<int>& arr) {
    quickSort(arr, 0, static_cast<int>(arr.size()) - 1);
}

void runCountingSort(std::vector<int>& arr) {
    if (arr.empty()) {
        countingSort(arr, 0);
        return;
    }

    int k = *std::max_element(arr.begin(), arr.end());
    countingSort(arr, k);
}

void runRadixSort(std::vector<int>& arr) {
    radixSort(arr);
}

TEST_CASE("Comparison-based sorting algorithms sort correctly") {
    std::vector<std::vector<int>> testCases = {
        {},
        {1},
        {1, 2, 3, 4, 5},
        {5, 4, 3, 2, 1},
        {5, 3, 8, 1, 2},
        {3, -1, 4, -5, 0, 3},
        {7, 7, 7, 7},
        {2, 1, 2, 1, 2}
    };

    SECTION("bubbleSort") {
        for (auto arr : testCases) expectSorted(bubbleSort, arr);
    }

    SECTION("insertionSort") {
        for (auto arr : testCases) expectSorted(insertionSort, arr);
    }

    SECTION("selectionSort") {
        for (auto arr : testCases) expectSorted(selectionSort, arr);
    }

    SECTION("mergeSort") {
        for (auto arr : testCases) expectSorted(runMergeSort, arr);
    }

    SECTION("quickSort") {
        for (auto arr : testCases) expectSorted(runQuickSort, arr);
    }

    SECTION("heapSort") {
        for (auto arr : testCases) expectSorted(heapSort, arr);
    }

    SECTION("bucketSort") {
        for (auto arr : testCases) expectSorted(bucketSort, arr);
    }

    SECTION("shellSort") {
        for (auto arr : testCases) expectSorted(shellSort, arr);
    }
}

TEST_CASE("Non-negative integer sorting algorithms sort correctly") {
    std::vector<std::vector<int>> testCases = {
        {},
        {0},
        {1, 2, 3, 4, 5},
        {5, 4, 3, 2, 1},
        {5, 3, 8, 1, 2},
        {0, 9, 3, 1, 4, 9, 2},
        {7, 7, 7, 7},
        {10, 100, 1, 50, 23, 8}
    };

    SECTION("countingSort") {
        for (auto arr : testCases) expectSorted(runCountingSort, arr);
    }

    SECTION("radixSort") {
        for (auto arr : testCases) expectSorted(runRadixSort, arr);
    }
}