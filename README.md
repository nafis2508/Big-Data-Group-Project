# Big-Data-Group-Project: Skyline Query and Nearest Neighbor Search Using R-Trees

This repository contains the source code, project documentation, and sample outputs for a group project in **COMP6210**, focusing on implementing Skyline Query and Nearest Neighbor Search using R-trees. R-trees provide an efficient spatial indexing structure, allowing for optimized performance in managing and querying spatial data. Our project applies these structures to solve two computational geometry tasks: **Nearest Neighbor Search** and **Skyline Query Search**.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Dataset Format](#dataset-format)
- [Task 1: Nearest Neighbor Search](#task-1-nearest-neighbor-search)
  - [Sequential Scan](#sequential-scan)
  - [Best-First Search](#best-first-search)
  - [Divide and Conquer](#divide-and-conquer)
- [Task 2: Skyline Query Search](#task-2-skyline-query-search)
  - [Sequential Scan Skyline Search](#sequential-scan-skyline-search)
  - [Branch-and-Bound Skyline (BBS) Search](#branch-and-bound-skyline-bbs-search)
  - [Divide and Conquer BBS Skyline Search](#divide-and-conquer-bbs-skyline-search)
- [Usage Instructions](#usage-instructions)
- [Performance Analysis](#performance-analysis)
- [Project Report and Presentation](#project-report-and-presentation)
- [References](#references)

## Project Overview

In this project, we developed Python implementations for two spatial search tasks using R-trees: **Nearest Neighbor Search** and **Skyline Query Search**. These tasks involve working with spatial datasets to answer complex queries efficiently, leveraging the R-tree data structure's hierarchical, spatial organization capabilities. The project’s primary goals were to:
- Implement and compare different algorithms for Nearest Neighbor and Skyline Search tasks.
- Evaluate algorithm performance based on execution time and accuracy.
- Demonstrate the advantages of R-trees in managing and querying spatial data.

## Project Structure

The repository includes the following files and folders:

- **`Task1.py`**: Implements Nearest Neighbor Search algorithms.
- **`Task2.py`**: Implements Skyline Query Search algorithms.
- **`create_rtree.py`**: Contains helper classes and functions for constructing and managing R-trees, utilized in both tasks.
- **`output_nearest_neighbors.txt`**: Sample output for Task 1 showing nearest neighbor search results and timing information.
- **`output_skyline.txt`**: Sample output for Task 2 showing skyline query results and timing information.
- **`Project_Report.pdf`**: Detailed report on the project, including algorithm design, implementation details, and performance analysis.
- **`Presentation_Slides.pdf`**: Group presentation slides summarizing the project’s objectives, methods, and findings.

## Dataset Format

Each task operates on datasets formatted as follows:

```
<id> <x> <y>
```

- `<id>`: Unique identifier for each point.
- `<x>` and `<y>`: 2D coordinates representing properties of the point (e.g., cost and size for Skyline Search or location coordinates for Nearest Neighbor Search).

Example:
```
74464 300.0 790.74
280895 300.2 793.77
60245 300.27 794.59
```

## Task 1: Nearest Neighbor Search

Task 1 implements three algorithms to find the nearest neighbor of a query point within a dataset. These algorithms explore different approaches to balance computational efficiency and accuracy in proximity searches:

### Sequential Scan

- **Algorithm**: Calculates the Euclidean distance between each point in the dataset and the query point, iterating through all points to identify the nearest neighbor.
- **Time Complexity**: \(O(n)\)
- **Usage**: Suitable for small datasets where R-tree indexing might add unnecessary complexity.

### Best-First Search (BFS) Using R-tree

- **Algorithm**: Constructs an R-tree for the dataset, then performs a best-first search, prioritizing nodes based on the minimum bounding rectangles (MBRs) that are closest to the query point.
- **Time Complexity**: Dependent on the depth and branching of the R-tree, generally more efficient than sequential scanning for large datasets.
- **Usage**: Optimized for larger datasets due to the hierarchical structure of R-trees, reducing the search space.

### Divide and Conquer Using Two R-trees

- **Algorithm**: Divides the dataset into two parts (subspaces), builds separate R-trees, and performs nearest neighbor searches in each subspace. The results are then compared to determine the closest point.
- **Time Complexity**: Lower search space complexity with some additional overhead from tree management.
- **Usage**: Effective for very large datasets, leveraging dataset division to reduce search complexity.

## Task 2: Skyline Query Search

Task 2 focuses on Skyline Query Search, which identifies points in a dataset that are not dominated by any other point. A point is considered a **skyline point** if there is no other point that is both cheaper and larger (for cost-size data) than it.

### Sequential Scan Skyline Search

- **Algorithm**: Compares each point in the dataset against every other point to check for dominance, adding non-dominated points to the skyline.
- **Time Complexity**: \(O(n^2)\)
- **Usage**: Suitable for small datasets; impractical for large datasets due to quadratic complexity.

### Branch-and-Bound Skyline (BBS) Search Using R-tree

- **Algorithm**: Uses an R-tree with a branch-and-bound strategy, which filters out points that are unlikely to be part of the skyline. Only necessary nodes are expanded, significantly reducing the number of comparisons.
- **Time Complexity**: \(O(n \log n)\), depending on dataset size and tree structure.
- **Usage**: Highly effective for larger datasets due to optimized node exploration, leveraging R-tree properties.

### Divide and Conquer BBS Skyline Search

- **Algorithm**: Splits the dataset into two parts based on a single dimension, performs the BBS skyline search on each half, and combines results while eliminating any dominated points in the combined skyline.
- **Time Complexity**: \(O(n \log n)\) for each subset, with added complexity in merging.
- **Usage**: Particularly advantageous for extremely large datasets, as it reduces the number of dominance checks.

## Usage Instructions

To run the tasks and generate output files, follow these steps:

1. **Prepare Dataset Files**: Ensure that dataset files are correctly formatted and located in the working directory. Supported datasets include city and facility data files (e.g., `city2.txt`, `parking_dataset.txt`).
   
2. **Run Task 1 (Nearest Neighbor Search)**:
   ```bash
   python Task1.py
   ```
   Results will be saved to `output_nearest_neighbors.txt`.

3. **Run Task 2 (Skyline Query Search)**:
   ```bash
   python Task2.py
   ```
   Results will be saved to `output_skyline.txt`.

## Performance Analysis

Each task’s output file includes both results and performance metrics for comparing algorithm efficiency. The performance data includes:

- **Task 1 Output**: Lists nearest neighbors found for each query point by each algorithm, along with execution times.
- **Task 2 Output**: Lists skyline points identified by each algorithm and the respective execution times.

### Sample Output for Task 1 (Nearest Neighbor Search):

```
Sequential Scan - Query 1: id=69898, x=47.31, y=128.88
Best First - Query 1: id=69898, x=47.31, y=128.88
Divide and Conquer - Query 1: id=69898, x=47.31, y=128.88

Total running time (Sequential Scan): 7.18 seconds, Average time: 0.036 seconds
Total running time (Best First): 30.61 seconds, Average time: 0.153 seconds
Total running time (Divide and Conquer): 28.90 seconds, Average time: 0.145 seconds
```

### Sample Output for Task 2 (Skyline Query Search):

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

## Project Report and Presentation

- **[Project Report](./Project_Report.pdf)**: Contains a detailed description of the project’s goals, algorithm designs, implementation details, and performance evaluations.
- **[Presentation Slides](./Presentation_Slides.pdf)**: Summarizes the project in a concise format, suitable for group presentation, with key findings and visual aids.

## References

1. Guttman, A. (1984). R-trees: A Dynamic Index Structure for Spatial Searching.
2. Ding, W., et al. (2006). Branch-and-Bound Skyline Computation in Metric Spaces.
3. Video Presentation: [Watch here](https://drive.google.com/file/d/1X_emUTL5RpSel_yf7hZepjiltIfzWa3R/view?usp=sharing)

This README provides a comprehensive overview of the project, including usage,

 algorithm details, and performance insights, to help users understand and interact with the code effectively.
