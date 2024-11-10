import math
import time
from create_rtree import main as build_rtree, RTree, Node

# Function to calculate Euclidean distance between two points
def euclidean_distance(p1, p2):
    # Calculate the Euclidean distance using the formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    return math.sqrt((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2)

# Sequential Scan Based Method to find nearest neighbor
def sequential_scan(query, data):
    # Initialize the variables for tracking the nearest facility
    nearest_facility = None
    min_distance = float('inf')  # Set initial min_distance to infinity
    
    # Loop through all data points (facilities) to find the nearest one
    for facility in data:
        # Calculate the distance between the query point and the facility
        distance = euclidean_distance(query, facility)
        if distance < min_distance:
            # Update the nearest facility and the minimum distance
            min_distance = distance
            nearest_facility = facility
            
    return nearest_facility

# Best First (BF) Algorithm using R-tree to find the nearest neighbor
def best_first_search(query, rtree):
    # Initialize variables to track the nearest neighbor and minimum distance
    nearest = None
    min_distance = float('inf')
    
    # Use a stack to traverse the R-tree (initially contains the root node)
    stack = [rtree.root]
    
    while stack:
        node = stack.pop()
        
        # If the node is a leaf, check its data points for the nearest neighbor
        if node.is_leaf():
            for point in node.data_points:
                # Calculate the distance between the query and the point
                distance = euclidean_distance(query, point)
                if distance < min_distance:
                    # Update the nearest point if the current one is closer
                    min_distance = distance
                    nearest = point
        else:
            # For non-leaf nodes, sort the child nodes based on the distance to the query's MBR (Minimum Bounding Rectangle)
            sorted_children = sorted(node.child_nodes, key=lambda child: euclidean_distance(query, {
                'x': (child.MBR['x1'] + child.MBR['x2']) / 2,
                'y': (child.MBR['y1'] + child.MBR['y2']) / 2
            }))
            # Add sorted children to the stack for further exploration
            stack.extend(sorted_children)
    
    return nearest

# Best First with Divide-and-Conquer using two R-trees
def divide_and_conquer_search(left_rtree, right_rtree, query):
    # Perform best first search on the left R-tree and right R-tree separately
    left_nearest = best_first_search(query, left_rtree)
    right_nearest = best_first_search(query, right_rtree)
    
    # Calculate the Euclidean distance to the query for both results
    left_distance = euclidean_distance(query, left_nearest)
    right_distance = euclidean_distance(query, right_nearest)

    # Return the nearest neighbor from the R-tree with the smaller distance
    return left_nearest if left_distance < right_distance else right_nearest

# Load dataset from a text file
def load_dataset(filename):
    data = []
    with open(filename, 'r') as file:
        # Read each line and split the line into parts (id, x, y)
        for line in file:
            parts = line.split()
            # Append the parsed data as a dictionary with id, x, and y coordinates
            data.append({
                'id': int(parts[0]),
                'x': float(parts[1]),
                'y': float(parts[2])
            })
    return data

def main():
    # Load the dataset of points (facilities) and query points
    points_list = load_dataset("parking_dataset.txt")
    queries = load_dataset("query_points.txt")

    # Build the R-tree using the custom R-tree implementation
    print("Building R-tree...")
    rtree = build_rtree(points_list)
    print("R-tree built successfully.")

    # Divide the dataset into two halves and build separate R-trees for divide and conquer method
    print("Dividing dataset and building separate R-trees for divide and conquer...")
    left_rtree, right_rtree = build_rtree(points_list[:len(points_list)//2]), build_rtree(points_list[len(points_list)//2:])
    print("Separate R-trees built successfully.")

    # Initialize variables to track the total time taken by each search method
    total_time_seq = 0
    total_time_bf = 0
    total_time_dac = 0

    # Create a list to store the results of each query
    results = []

    # Process each query in 'queries'
    for i, query in enumerate(queries):
        # Sequential Scan - Find nearest neighbor using sequential scan method
        start_time = time.time()
        nearest_seq = sequential_scan(query, points_list)
        total_time_seq += time.time() - start_time
        results.append(f"Sequential Scan - Query {i + 1}: id={nearest_seq['id']}, x={nearest_seq['x']:.2f}, y={nearest_seq['y']:.2f}")

        # Best First Search using R-tree - Find nearest neighbor using best first search algorithm
        start_time = time.time()
        nearest_bf = best_first_search(query, rtree)
        total_time_bf += time.time() - start_time
        results.append(f"Best First - Query {i + 1}: id={nearest_bf['id']}, x={nearest_bf['x']:.2f}, y={nearest_bf['y']:.2f}")

        # Divide and Conquer with R-tree - Use divide and conquer method with two R-trees
        start_time = time.time()
        nearest_dac = divide_and_conquer_search(left_rtree, right_rtree, query)
        total_time_dac += time.time() - start_time
        results.append(f"Divide and Conquer - Query {i + 1}: id={nearest_dac['id']}, x={nearest_dac['x']:.2f}, y={nearest_dac['y']:.2f}")

    # Calculate the average time taken for each method
    average_time_seq = total_time_seq / len(queries)
    average_time_bf = total_time_bf / len(queries)
    average_time_dac = total_time_dac / len(queries)

    # Add summary of total and average times for each method to the results
    results.append(f"\nTotal running time (Sequential Scan): {total_time_seq:.6f} seconds, Average time: {average_time_seq:.6f} seconds")
    results.append(f"Total running time (Best First): {total_time_bf:.6f} seconds, Average time: {average_time_bf:.6f} seconds")
    results.append(f"Total running time (Divide and Conquer): {total_time_dac:.6f} seconds, Average time: {average_time_dac:.6f} seconds")

    # Write all the results to a text file
    output_filename = 'nearest_facilities_output1.txt'
    with open(output_filename, 'w') as f:
        for line in results:
            f.write(line + '\n')

    # Print a message confirming the output has been written
    print(f"Output written to {output_filename}")

# Entry point of the script
if __name__ == '__main__':
    main()
