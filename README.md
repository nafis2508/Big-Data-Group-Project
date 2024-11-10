# Big-Data-Group-Project
# Skyline Query and Nearest Neighbor Search using R-Trees

This repository provides Python implementations for solving two main computational geometry tasks: **Skyline Query Search** and **Nearest Neighbor Search**. Both tasks leverage **R-tree** spatial indexing to efficiently perform complex spatial operations. The repository is divided into two tasks, each of which implements different query processing techniques on a spatial dataset.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Dataset Format](#dataset-format)
3. [Task 1: Nearest Neighbor Search](#task-1-nearest-neighbor-search)
   - [Sequential Scan](#sequential-scan)
   - [Best-First Search](#best-first-search)
   - [Divide and Conquer](#divide-and-conquer)
4. [Task 2: Skyline Query Search](#task-2-skyline-query-search)
   - [Sequential Scan Skyline Search](#sequential-scan-skyline-search)
   - [Branch-and-Bound Skyline (BBS) Search](#branch-and-bound-skyline-bbs-search)
   - [Divide and Conquer BBS Skyline Search](#divide-and-conquer-bbs-skyline-search)
5. [Usage](#usage)
6. [Performance Analysis](#performance-analysis)
7. [References](#references)

## Project Structure

The repository is organized as follows:

- `Task1.py`: Contains the code for Task 1, which implements Nearest Neighbor Search algorithms.
- `Task2.py`: Contains the code for Task 2, which implements Skyline Query Search algorithms.
- `create_rtree.py`: Shared module with classes and methods for constructing and managing R-trees, used in both tasks.
- `output_nearest_neighbors.txt`: Sample output file from Task 1.
- `output_skyline.txt`: Sample output file from Task 2.

## Dataset Format

Each task uses a dataset where each entry represents a point in 2D space. Points are structured as:
```
<id> <x> <y>
```

For example:
```
74464 300.0 790.74
280895 300.2 793.77
60245 300.27 794.59
```

- `<id>` is a unique identifier for each point.
- `<x>` and `<y>` are the coordinates in 2D space.

## Task 1: Nearest Neighbor Search

Task 1 implements algorithms to find the **nearest neighbor** to a given query point within a dataset. This task includes three main search methods:

### Sequential Scan

**Algorithm:** Sequentially scans all points and calculates the Euclidean distance to the query point to find the nearest neighbor.

**Time Complexity:** O(n)

**Usage:** Useful for small datasets where an R-tree might add unnecessary complexity.

### Best-First Search (BFS) using R-tree

**Algorithm:** Uses the R-tree data structure to prioritize nodes based on their minimum bounding rectangles (MBRs), exploring the tree in best-first order.

**Time Complexity:** Depends on the depth and branching of the R-tree, but generally more efficient than sequential scan for large datasets.

**Usage:** More effective than sequential scan for large datasets due to the R-tree’s hierarchical structure.

### Divide and Conquer using Two R-trees

**Algorithm:** Divides the dataset into two parts and builds separate R-trees for each subset. Performs a nearest neighbor search on each tree, then combines results to determine the closest neighbor.

**Time Complexity:** Reduces the search space compared to a single R-tree but incurs additional overhead in tree management.

**Usage:** Provides further optimization for large datasets by reducing search complexity through subdivision.

## Task 2: Skyline Query Search

Task 2 implements **Skyline Query Search** algorithms that filter points to find a set of non-dominated points. Skyline points are those that are not dominated by any other point across both dimensions.

### Sequential Scan Skyline Search

**Algorithm:** Compares each point to all other points to determine if it’s part of the skyline.

**Time Complexity:** O(n²)

**Usage:** Best suited for small datasets; performs poorly on larger datasets due to quadratic complexity.

### Branch-and-Bound Skyline (BBS) Search using R-tree

**Algorithm:** Leverages an R-tree and a branch-and-bound strategy to efficiently filter points, only expanding nodes that are necessary for skyline evaluation.

**Time Complexity:** O(n log n) on average, depending on the dataset and tree structure.

**Usage:** Well-suited for large datasets due to its optimized node exploration.

### Divide and Conquer BBS Skyline Search

**Algorithm:** Splits the dataset into two halves and applies the BBS algorithm on each half. Combines the results and removes any dominated points in the combined skyline.

**Time Complexity:** O(n log n) for each subset, but with added complexity in merging results.

**Usage:** Particularly effective for very large datasets with clear divisions, as it limits the search space in each subset.

## Usage

1. **Prepare Dataset Files:**
   - Ensure datasets are in the correct format and named appropriately (e.g., `parking_dataset.txt`, `city2.txt`).
   
2. **Run Task 1 (Nearest Neighbor Search):**
   ```bash
   python Task1.py
   ```
   Output will be saved to `output_nearest_neighbors.txt`.

3. **Run Task 2 (Skyline Query Search):**
   ```bash
   python Task2.py
   ```
   Output will be saved to `output_skyline.txt`.

## Performance Analysis

The output files provide both results and timings for each algorithm:

- **Task 1 Output:**
  - Provides details on the nearest neighbors found by each algorithm.
  - Displays execution time for each algorithm to illustrate performance differences.

- **Task 2 Output:**
  - Lists the skyline points identified by each algorithm.
  - Includes timing data for sequential scan, BBS, and divide-and-conquer approaches.

**Sample output for Task 1 (Nearest Neighbor Search):**
```
Sequential Scan - Query 1: id=69898, x=47.31, y=128.88
Best First - Query 1: id=69898, x=47.31, y=128.88
Divide and Conquer - Query 1: id=69898, x=47.31, y=128.88
...
Total running time (Sequential Scan): 7.177494 seconds, Average time: 0.035887 seconds
Total running time (Best First): 30.607147 seconds, Average time: 0.153036 seconds
Total running time (Divide and Conquer): 28.899093 seconds, Average time: 0.144495 seconds
```

**Sample output for Task 2 (Skyline Query Search):**
```
Sequential Scan Skyline Results:
74464 300.0 790.74
...
Sequential Scan Time: 1.9445 seconds

BBS Skyline Results:
74464 300.0 790.74
...
BBS Execution Time: 0.0106 seconds

BBS with Divide-and-Conquer Skyline Results:
74464 300.0 790.74
...
Divide-and-Conquer Execution Time: 21.4461 seconds
```

## References

- *R-Trees: A Dynamic Index Structure for Spatial Searching* by Antonin Guttman.
- *Branch-and-Bound Skyline Computation in Metric Spaces* by Ding et al.

---

This README provides an overview of the project, usage instructions, and sample outputs for evaluating algorithm performance.
