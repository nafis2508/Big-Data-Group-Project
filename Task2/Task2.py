# skyline_search.py
import time  # I use this to measure how long each algorithm takes to run
import create_rtree  # I import my R-tree functions from the create_rtree module

# This function reads a dataset from a file and turns it into a list of points (each as a dictionary)
def read_dataset(file_path):
    points_list = []  # This will hold all the points from the file
    with open(file_path, 'r') as file:  # I open the file in read mode
        for line in file:  # I go through each line in the file
            parts = line.strip().split()  # Split the line into parts (ID, x, y)
            point = {'id': parts[0], 'x': float(parts[1]), 'y': float(parts[2])}  # Create a dictionary for the point
            points_list.append(point)  # Add the point to the list
    return points_list  # Return the complete list of points

# This function checks if point 'a' dominates point 'b'
def dominates(a, b):
    # 'a' dominates 'b' if 'a' is cheaper or the same price and bigger in size, and one of these conditions is strictly true
    return a['x'] <= b['x'] and a['y'] >= b['y'] and (a['x'] < b['x'] or a['y'] > b['y'])

# This function finds the skyline points using a simple, straightforward method (sequential scan)
def sequential_scan_skyline(points_list):
    skyline = []  # This will store the skyline points
    for point in points_list:  # For each point in the list
        # If no other point dominates this point, it's part of the skyline
        if not any(dominates(other, point) for other in points_list):
            skyline.append(point)  # Add the point to the skyline
    # Sort the skyline points by cost (x) in ascending order and by size (y) in descending order
    return sorted(skyline, key=lambda p: (p['x'], -p['y']))

# This function calculates the minimum distance from the origin (0, 0) to the MBR of a node
def mindist_to_origin(mbr):
    return mbr['x1']**2 + mbr['y2']**2  # Calculate the squared distance (no need for the square root)

# This function performs the BBS algorithm to find skyline points using an R-tree
def bbs_skyline_search(rtree):
    skyline = []  # This will store the final skyline points
    # Start with a list that contains the root node and its distance to the origin
    L = [(mindist_to_origin(rtree.root.MBR), rtree.root)]
    L.sort(key=lambda x: x[0])  # Sort the list by distance to the origin

    while L:  # Keep processing until the list is empty
        _, node = L.pop(0)  # Get the node with the smallest distance and remove it from the list
        if node.is_leaf():  # If the node is a leaf, I process its data points
            for point in node.data_points:
                # If the point is not dominated by any point in the current skyline, add it
                if not any(dominates(sky_point, point) for sky_point in skyline):
                    # Remove points from the skyline that are dominated by this new point
                    skyline = [sky_point for sky_point in skyline if not dominates(point, sky_point)]
                    skyline.append(point)  # Add the new point to the skyline
        else:  # If the node is not a leaf, I process its child nodes
            for child in node.child_nodes:
                # I use the top-left corner of the child's MBR as a point for comparison
                child_mbr_point = {'x': child.MBR['x1'], 'y': child.MBR['y2']}
                # If this MBR point is not dominated by the skyline, I add the child node to the list
                if not any(dominates(sky_point, child_mbr_point) for sky_point in skyline):
                    L.append((mindist_to_origin(child.MBR), child))
            L.sort(key=lambda x: x[0])  # Sort the list again after adding new nodes
    return skyline  # Return the final list of skyline points

# This function splits the dataset into two subspaces for divide-and-conquer
def divide_dataset(points_list, dimension='x'):
    # Sort the points by the chosen dimension (x or y)
    sorted_points = sorted(points_list, key=lambda p: p[dimension])
    mid_index = len(sorted_points) // 2  # Find the middle index
    # Return two halves of the sorted list
    return sorted_points[:mid_index], sorted_points[mid_index:]

# This function applies the BBS algorithm using a divide-and-conquer approach
def bbs_divide_and_conquer(points_list):
    # Split the dataset into two subspaces
    subspace1, subspace2 = divide_dataset(points_list)
    # Build an R-tree for each subspace and find the skyline for each
    rtree1 = create_rtree.main(subspace1)
    rtree2 = create_rtree.main(subspace2)

    skyline1 = bbs_skyline_search(rtree1)
    skyline2 = bbs_skyline_search(rtree2)

    # Combine the two skylines and filter out dominated points
    combined_skyline = skyline1 + skyline2
    final_skyline = []
    for point in combined_skyline:
        if not any(dominates(other_point, point) for other_point in combined_skyline):
            final_skyline.append(point)  # Add the point if it is not dominated
    return final_skyline  # Return the final combined skyline

# The main function orchestrates the execution of the different skyline algorithms
def main():
    dataset_path = "city2.txt"  # Path to the input dataset
    output_path = "output_city2.txt"  # Path for the output file

    # Read the dataset into a list of points
    points_list = read_dataset(dataset_path)

    # Open the output file for writing the results
    with open(output_path, 'w') as output_file:
        # Perform the sequential scan and time it
        start_time = time.time()
        sequential_skyline = sequential_scan_skyline(points_list)
        end_time = time.time()
        # Write the results of the sequential scan to the output file
        output_file.write("Sequential Scan Skyline Results:\n")
        for point in sequential_skyline:
            output_file.write(f"{point['id']} {point['x']} {point['y']}\n")
        output_file.write(f"Sequential Scan Time: {end_time - start_time:.4f} seconds\n\n")

        # Build an R-tree from the points and perform the BBS algorithm
        rtree = create_rtree.main(points_list)
        start_time = time.time()
        bbs_skyline = bbs_skyline_search(rtree)
        end_time = time.time()
        # Write the results of the BBS algorithm to the output file
        output_file.write("BBS Skyline Results:\n")
        for point in bbs_skyline:
            output_file.write(f"{point['id']} {point['x']} {point['y']}\n")
        output_file.write(f"BBS Execution Time: {end_time - start_time:.4f} seconds\n\n")

        # Perform the BBS with divide-and-conquer and time it
        start_time = time.time()
        divide_conquer_skyline = bbs_divide_and_conquer(points_list)
        end_time = time.time()
        # Write the results of the divide-and-conquer algorithm to the output file
        output_file.write("BBS with Divide-and-Conquer Skyline Results:\n")
        for point in divide_conquer_skyline:
            output_file.write(f"{point['id']} {point['x']} {point['y']}\n")
        output_file.write(f"Divide-and-Conquer Execution Time: {end_time - start_time:.4f} seconds\n")

# I use this to make sure the main function runs when I execute the script
if __name__ == "__main__":
    main()
