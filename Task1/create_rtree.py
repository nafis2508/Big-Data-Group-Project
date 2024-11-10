import sys
import math

# B sets the maximum capacity for the number of data points or child nodes that each node can hold before it needs to split
B = 4

def main(points_list):
    """
    Builds an R-tree from the data points in the parking dataset. When the main function is executed, it initiates the construction of
    an R-tree using the data from the parking dataset. Each point from the dataset is inserted into the RTree, ensuring that each node
    maintains a branching factor of B = 4 and that the Minimum Bounding Rectangles (MBRs) are as compact as possible.

    Arguments:
        points_list (list of dict): A list of dictionaries, where each dictionary contains 'x' and 'y' coordinates representing the 
        parking dataset's points.

    Returns:
        RTree: An instance of the RTree class containing all the coordinates from the parking dataset, organized within the tree structure.
    
    """

    # Create the root object of RTree from where the points insertion will be started
    rtree = RTree()
    
    for point in points_list:  # Insert data points from the root one by one 
        rtree.insert(rtree.root, point) 

    return rtree  # Return the final constructed RTree root with the location of all its children


class Node:
    """
    The base structure for a node in an R-tree, which can be a root, child, or leaf node. Each node stores essential information 
    and is responsible for maintaining a Minimum Bounding Rectangle (MBR) that is updated as new data points are added during the 
    R-tree construction. Leaf nodes contain actual data points, while internal nodes store references to child nodes. If a node 
    exceeds its capacity for child nodes or data points, a split operation is triggered.

    Attributes:
        id (int): Used to uniquely identify a node, useful for debugging purposes.
        child_nodes (list of Node): A list of child nodes for internal nodes.
        data_points (list of dict): A list of data points (represented as dictionaries with 'x' and 'y' coordinates) for leaf nodes. 
        For internal nodes, this list remains empty.
        parent (Node): The parent node of the current node, or `None` if the node is the root.
        MBR (dict): A dictionary representing the Minimum Bounding Rectangle with keys 'x1', 'y1', 'x2', 'y2'.
    """

    def __init__(self):
        """
        Creates a new Node with default settings, ready to either store data points (as a leaf node) or link to child nodes (as an 
        internal node). The MBR is initialized with undefined values.
        """

        self.id = 0
        self.child_nodes = []      # For internal nodes
        self.data_points = []      # For leaf nodes
        self.parent = None         # Only the root will have no parent after construction is done

        # Values of coordinates have been set to -1, assuming all coordinate values will be larger than this.
        # After each point insertion, MBR is updated for the associated nodes
        self.MBR = {
            'x1': -1,
            'y1': -1,
            'x2': -1,
            'y2': -1,
        }

    def perimeter(self):
        """
        Computes the half-perimeter of the node's Minimum Bounding Rectangle (MBR). This value is used during insertion to help 
        decide which node will experience the least perimeter increase when adding a new data point, ensuring the tree remains balanced. 
        The half-perimeter is sufficient for comparison purposes, as multiplying by 2 does not affect the result of the comparisons.
    
        Returns:
        float: The computed half-perimeter of the MBR.
        """

        return (self.MBR['x2'] - self.MBR['x1']) + (self.MBR['y2'] - self.MBR['y1'])

    def is_overflow(self):
        """
        Checks if the node surpasses the predefined threshold of data points or child nodes defined by B (branching factor). 
        For leaf nodes, it evaluates the number of data points, while for internal nodes, it assesses the number of child nodes.
    
        Returns:
        bool: True if the node exceeds B data points or child nodes, False if it does not.
    
        """

        if self.is_leaf():
            return len(self.data_points) > B
        else:
            return len(self.child_nodes) > B

    def is_root(self):
        """
        Checks whether this node is the root of the R-tree.

        Returns:
            bool: True if the node has no parent, otherwise False.
        """

        return self.parent is None

    def is_leaf(self):
        """
        Checks if the node is a leaf node by calculating the number of internal nodes. For an internal node, there will be at least two children or
        internal nodes.

        Returns:
            bool: True if the number of child nodes is 0, False otherwise.
        """

        return len(self.child_nodes) == 0


class RTree:
    """
    This class manages the dynamic arrangement of nodes in the R-tree.

    Attributes:
        root (Node): The starting node of the R-tree, responsible for overseeing all insertions and structural modifications.
    """    

    def __init__(self):
        """        
        Initializes an R-tree by setting up a root node, ready for adding data points.
        """

        self.root = Node()  # Create a root node

    def insert(self, u, p):
        """
        Inserts a data point into the R-tree, beginning from the specified node. If the node is a leaf, the data point is inserted directly.
        If this causes an overflow, the appropriate overflow handling is triggered. If the node is not a leaf, the function recursively 
        traverses the tree to locate the appropriate subtree for insertion, ensuring the point is placed in a way that minimizes MBR expansion.

        Arguments:
        u (Node): The node where the insertion begins.
        p (dict): The data point to insert, usually a dictionary containing 'x' and 'y' coordinates.

        Returns:
        None: The method modifies the R-tree structure in place without returning a value.
        """

        if u.is_leaf(): 
            self.add_data_point(u, p)  # Add the data point and update the corresponding MBR
            if u.is_overflow():
                self.handle_overflow(u)  # Handle overflow for leaf nodes
        else:
            v = self.choose_subtree(u, p)  # Choose a subtree to insert the data point to minimize the perimeter sum
            self.insert(v, p)  # Continue recursively until a leaf node is reached
            self.update_mbr(v)  # Update the MBR after insertion

    def choose_subtree(self, u, p): 
        """
        Chooses the most suitable subtree for inserting a new data point by minimizing the perimeter expansion of the MBR. This selection is 
        essential for preserving the spatial efficiency of the R-tree. The method evaluates the perimeter increase for each child node's 
        MBR and selects the one with the smallest increase.

        Arguments:
        u (Node): The internal node from which the child subtree will be selected.
        p (dict): The data point that needs to be inserted.

        Returns:
        Node: The selected child node that results in the smallest perimeter increase when the data point is inserted.
        """

        if u.is_leaf():  # If it's a leaf node, return it for insertion
            return u
        else:
            min_increase = sys.maxsize  # Initialize with a large number
            best_child = None
            for child in u.child_nodes:  # Iterate through child nodes to find the best insertion point
                increase = self.peri_increase(child, p)
                if increase < min_increase:
                    min_increase = increase
                    best_child = child
            return best_child

    def peri_increase(self, node, p):
        """
        Computes the potential increase in the perimeter of a node's Minimum Bounding Rectangle (MBR) if a new data point were added. 
        The function assesses the hypothetical change in perimeter by comparing the current MBR's extents with the new data point's location, 
        which helps in selecting the optimal subtree during insertion.

        Arguments:
        node (Node): The node for which the perimeter increase is to be calculated, usually a child of an internal node.
        p (dict): The new data point to be inserted, represented by 'x' and 'y' coordinates.

        Returns:
        float: The calculated perimeter increase resulting from adding the data point to the node's MBR. This value aids in selecting the 
        subtree that minimizes spatial expansion.
        """

        origin_mbr = node.MBR
        x1, x2, y1, y2 = origin_mbr['x1'], origin_mbr['x2'], origin_mbr['y1'], origin_mbr['y2']
        
        # Calculate new MBR after adding the new point
        new_x1 = min(x1, p['x'])
        new_x2 = max(x2, p['x'])
        new_y1 = min(y1, p['y'])
        new_y2 = max(y2, p['y'])
        
        # Calculate the increase in half-perimeter
        new_perimeter = (new_x2 - new_x1) + (new_y2 - new_y1)
        increase = new_perimeter - node.perimeter()
        return increase

    def handle_overflow(self, u):
        """
        Manages the overflow condition in a node by splitting it into two when the number of child nodes or data points exceeds the 
        maximum capacity defined by B. If the root node overflows, a new root is created to accommodate the split. If any other node 
        overflows, the resulting split nodes are handled by the current parent, maintaining the balance of the tree and minimizing area expansion.

        Arguments:
        u (Node): The node that has exceeded its capacity and requires splitting.

        Returns:
        None: This method modifies the tree structure in-place by splitting the overflowing node and, if necessary, creating a new root.
        """

        # Get the best split of two MBR based on whether u is a leaf node or an internal node.
        u1, u2 = self.split(u)  # u1 and u2 are the two splits returned by the split function

        if u.is_root():
            new_root = Node()  # Create a new root
            self.add_child(new_root, u1) 
            self.add_child(new_root, u2)
            self.root = new_root
            self.update_mbr(new_root)
        else:
            w = u.parent  # Parent node where u was a child
            w.child_nodes.remove(u)
            self.add_child(w, u1)  # Link the two splits and update the corresponding MBR
            self.add_child(w, u2)
            if w.is_overflow():  # Check recursively if the parent node now overflows
                self.handle_overflow(w) 

    def split(self, u):
        """
        Splits an overflowing node into two separate nodes to preserve the balance and efficiency of the R-tree structure. This method 
        assesses different splitting strategies based on the spatial arrangement of data points or child nodes within the node. The split 
        is optimized to minimize the combined perimeter of the resulting nodes, ensuring efficient space utilization and maintaining 
        tree balance. The function accounts for multiple dimensions and seeks to find the optimal split to reduce future overlap and 
        perimeter increase.

        Arguments:
        u (Node): The node to be split, which has exceeded its capacity due to an insertion.

        Returns:
        tuple: A pair of nodes resulting from the split, ensuring neither node exceeds the maximum capacity and both maintain 
        a balanced distribution of data points or child nodes.
        """

        best_s1 = Node()
        best_s2 = Node()
        best_perimeter = sys.maxsize

        if u.is_leaf():
            m = len(u.data_points)
            # Create two different kinds of divides: sorted by 'x' and sorted by 'y'
            divides = [
                sorted(u.data_points, key=lambda data_point: data_point['x']),
                sorted(u.data_points, key=lambda data_point: data_point['y'])
            ]
            for divide in divides:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1):
                    s1 = Node()
                    s1.data_points = divide[:i]
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.data_points = divide[i:]
                    self.update_mbr(s2)
                    current_perimeter = s1.perimeter() + s2.perimeter()
                    if current_perimeter < best_perimeter:
                        best_perimeter = current_perimeter
                        best_s1 = s1
                        best_s2 = s2

        else:
            m = len(u.child_nodes)
            # Create four different kinds of divides based on MBR coordinates
            divides = [
                sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x1']),
                sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x2']),
                sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y1']),
                sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y2'])
            ]
            for divide in divides:
                for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1):
                    s1 = Node()
                    s1.child_nodes = divide[:i]
                    self.update_mbr(s1)
                    s2 = Node()
                    s2.child_nodes = divide[i:]
                    self.update_mbr(s2)
                    current_perimeter = s1.perimeter() + s2.perimeter()
                    if current_perimeter < best_perimeter:
                        best_perimeter = current_perimeter
                        best_s1 = s1
                        best_s2 = s2

        # Update parent references for child nodes
        for child in best_s1.child_nodes:
            child.parent = best_s1
        for child in best_s2.child_nodes:
            child.parent = best_s2

        return best_s1, best_s2

    def add_child(self, node, child):
        """
        Adds a child node to the list of children of an existing node and updates the parent node's MBR to include the MBR of the new child.
        This method ensures the spatial integrity of the R-tree by maintaining an MBR that accurately covers all child nodes.

        Arguments:
        node (Node): The parent node that will receive the new child.
        child (Node): The child node to be added to the parent node's list of children.

        Returns:
        None: This method modifies the tree structure in-place by adding a child node and updating the parent's MBR.
        """
            
        node.child_nodes.append(child)  # Add child node to the current parent node
        child.parent = node 
        # Update the MBR to reflect the addition of the new child
        node.MBR['x1'] = min(node.MBR['x1'], child.MBR['x1'])
        node.MBR['x2'] = max(node.MBR['x2'], child.MBR['x2'])
        node.MBR['y1'] = min(node.MBR['y1'], child.MBR['y1'])
        node.MBR['y2'] = max(node.MBR['y2'], child.MBR['y2'])

    def add_data_point(self, node, data_point):
        """
        Adds a new data point to a leaf node and updates the node's MBR to encompass this point. This method plays a vital role in
        maintaining the accuracy of the spatial indexing as new data points are added to the tree.

        Arguments:
        node (Node): The leaf node where the data point will be inserted.
        data_point (dict): The data point to be added, represented by a dictionary containing 'x' and 'y' coordinates.

        Returns:
        None: This method updates the leaf node by adding the data point and modifying its MBR in-place.
        """
        
        # Add data point to the leaf node
        node.data_points.append(data_point)

        # Update the MBR to reflect the addition of the new data point
        node.MBR['x1'] = min(node.MBR['x1'], data_point['x'])
        node.MBR['x2'] = max(node.MBR['x2'], data_point['x'])
        node.MBR['y1'] = min(node.MBR['y1'], data_point['y'])
        node.MBR['y2'] = max(node.MBR['y2'], data_point['y'])

    def update_mbr(self, node):
        """
        Updates the Minimum Bounding Rectangle (MBR) of a node to correctly encompass all its child nodes or data points.
        This method is crucial for the proper operation of the R-tree, ensuring that each node's MBR accurately represents
        all spatial data it holds or points to.

        Arguments:
        node (Node): The node whose MBR is to be updated.

        Returns:
        None: This method modifies the node's MBR in-place to cover all the spatial data it contains or refers to, ensuring correct spatial indexing.
        """
        
        x_list = []
        y_list = []
        
        if node.is_leaf():
            # For leaf nodes, consider the 'x' and 'y' of all data points
            x_list = [point['x'] for point in node.data_points]
            y_list = [point['y'] for point in node.data_points]
        else:
            # For internal nodes, consider the 'x1', 'x2', 'y1', 'y2' of all child nodes
            x_list = [child.MBR['x1'] for child in node.child_nodes] + [child.MBR['x2'] for child in node.child_nodes]
            y_list = [child.MBR['y1'] for child in node.child_nodes] + [child.MBR['y2'] for child in node.child_nodes]
        
        # Update the MBR with the new min and max values
        node.MBR = {
            'x1': min(x_list),
            'x2': max(x_list),
            'y1': min(y_list),
            'y2': max(y_list)
        }
