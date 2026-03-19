// SortAlgorithms.h
#ifndef SORTALGORITHMS_H
#define SORTALGORITHMS_H

#include <vector>

void bubbleSort(std::vector<int>& arr);
void insertionSort(std::vector<int>& arr);
void selectionSort(std::vector<int>& arr);
void mergeSort(std::vector<int>& arr, int left, int right);
void quickSort(std::vector<int>& arr, int low, int high);
void heapSort(std::vector<int>& arr);
void countingSort(std::vector<int>& arr, int k);
void radixSort(std::vector<int>& arr);
void bucketSort(std::vector<int>& arr);
void shellSort(std::vector<int>& arr);

#endif // SORTALGORITHMS_H