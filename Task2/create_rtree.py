# create_rtree.py
import sys
import math

# The maximum number of entries a node can have before it needs to split
B = 4

# This class represents a Node in my R-tree.
class Node(object):
    def __init__(self):
        # This is a unique ID for the node (not used in this example, but I could use it if needed)
        self.id = 0
        # These are child nodes, which are used when the node is not a leaf
        self.child_nodes = []
        # These are data points for when the node is a leaf (the actual entries)
        self.data_points = []
        # I keep track of the parent node so I can backtrack if needed
        self.parent = None
        # This is the Minimum Bounding Rectangle (MBR) that defines the space this node covers
        self.MBR = {
            'x1': float('inf'),  # The leftmost x-coordinate (starts as infinity for initialization)
            'y1': float('inf'),  # The bottommost y-coordinate (starts as infinity)
            'x2': float('-inf'), # The rightmost x-coordinate (starts as negative infinity)
            'y2': float('-inf')  # The topmost y-coordinate (starts as negative infinity)
        }

    # Here, I calculate the perimeter of the node's MBR (I use this for finding optimal placement)
    def perimeter(self):
        return (self.MBR['x2'] - self.MBR['x1']) + (self.MBR['y2'] - self.MBR['y1'])

    # I check if the node has more entries than allowed (i.e., it's overflowing)
    def is_overflow(self):
        if self.is_leaf():
            return len(self.data_points) > B  # For leaf nodes, I check data points
        else:
            return len(self.child_nodes) > B  # For non-leaf nodes, I check child nodes

    # This helps me check if this node is the root (i.e., it doesn't have a parent)
    def is_root(self):
        return self.parent is None

    # I check if this node is a leaf (i.e., it doesn't have child nodes)
    def is_leaf(self):
        return len(self.child_nodes) == 0

# This is my class for the R-tree itself.
class RTree(object):
    def __init__(self):
        # The tree starts with an empty root node
        self.root = Node()

    # I use this function to insert a new data point into the R-tree, starting from the given node (u)
    def insert(self, u, p):
        if u.is_leaf():
            # If the current node is a leaf, I can add the data point here
            self.add_data_point(u, p)
            # I check if adding the point caused an overflow (too many entries)
            if u.is_overflow():
                self.handle_overflow(u)  # If it's overflowing, I split the node
        else:
            # If it's not a leaf, I need to find the best subtree to insert the point
            v = self.choose_subtree(u, p)
            self.insert(v, p)  # I recursively insert into the chosen subtree
            self.update_mbr(v)  # I update the MBR of the chosen subtree

    # Here, I find the best child node to insert the new point to minimize the perimeter increase
    def choose_subtree(self, u, p):
        min_increase = sys.maxsize  # I start with a very large number
        best_child = None
        for child in u.child_nodes:
            # I calculate how much the perimeter would increase if I added the point to this child
            increase = self.peri_increase(child, p)
            if increase < min_increase:
                min_increase = increase
                best_child = child  # I keep track of the best child found so far
        return best_child

    # I use this to calculate how much the perimeter of a node's MBR would increase if I added a new point
    def peri_increase(self, node, p):
        origin_mbr = node.MBR
        increase = (
            (max(origin_mbr['x2'], p['x']) - min(origin_mbr['x1'], p['x'])) +
            (max(origin_mbr['y2'], p['y']) - min(origin_mbr['y1'], p['y']))
        ) - node.perimeter()
        return increase

    # When a node overflows, I split it into two smaller nodes to handle the overflow
    def handle_overflow(self, u):
        u1, u2 = self.split(u)  # I split the overflowing node into two
        if u.is_root():
            # If the node is the root, I create a new root and add the two new nodes as its children
            new_root = Node()
            self.add_child(new_root, u1)
            self.add_child(new_root, u2)
            self.root = new_root  # I update the root of the tree
            self.update_mbr(new_root)
        else:
            # If it's not the root, I replace the overflowing node with its split parts in its parent
            parent = u.parent
            parent.child_nodes.remove(u)
            self.add_child(parent, u1)
            self.add_child(parent, u2)
            # I check if the parent is now overflowing, and handle it if necessary
            if parent.is_overflow():
                self.handle_overflow(parent)

    # This function splits a node into two smaller nodes when handling an overflow
    def split(self, u):
        best_s1, best_s2 = Node(), Node()  # These will hold the best split I find
        best_perimeter = sys.maxsize  # I start with a very large perimeter sum
        if u.is_leaf():
            # If the node is a leaf, I split its data points
            m = len(u.data_points)
            # I divide the data points based on x and y to find the best split
            divides = [sorted(u.data_points, key=lambda dp: dp['x']),
                       sorted(u.data_points, key=lambda dp: dp['y'])]
        else:
            # If the node is not a leaf, I split its child nodes
            m = len(u.child_nodes)
            divides = [sorted(u.child_nodes, key=lambda cn: cn.MBR['x1']),
                       sorted(u.child_nodes, key=lambda cn: cn.MBR['x2']),
                       sorted(u.child_nodes, key=lambda cn: cn.MBR['y1']),
                       sorted(u.child_nodes, key=lambda cn: cn.MBR['y2'])]

        # I try each possible split and find the one with the smallest perimeter sum
        for divide in divides:
            for i in range(math.ceil(0.4 * B), m - math.ceil(0.4 * B) + 1):
                s1 = Node()
                s2 = Node()
                if u.is_leaf():
                    s1.data_points = divide[:i]
                    s2.data_points = divide[i:]
                else:
                    s1.child_nodes = divide[:i]
                    s2.child_nodes = divide[i:]
                self.update_mbr(s1)
                self.update_mbr(s2)
                perimeter_sum = s1.perimeter() + s2.perimeter()
                if perimeter_sum < best_perimeter:
                    best_perimeter = perimeter_sum
                    best_s1, best_s2 = s1, s2

        # I set the parent references for the new child nodes
        for child in best_s1.child_nodes:
            child.parent = best_s1
        for child in best_s2.child_nodes:
            child.parent = best_s2

        return best_s1, best_s2

    # I add a child node to a given node and update its MBR
    def add_child(self, node, child):
        node.child_nodes.append(child)
        child.parent = node
        self.update_mbr(node)

    # I add a data point to a node and update its MBR
    def add_data_point(self, node, data_point):
        node.data_points.append(data_point)
        self.update_mbr(node)

    # I update the MBR of a node based on its child nodes or data points
    def update_mbr(self, node):
        x_list = []
        y_list = []
        if node.is_leaf():
            # I collect x and y coordinates from the data points
            x_list = [dp['x'] for dp in node.data_points]
            y_list = [dp['y'] for dp in node.data_points]
        else:
            # I collect x and y coordinates from the MBRs of the child nodes
            for child in node.child_nodes:
                x_list.extend([child.MBR['x1'], child.MBR['x2']])
                y_list.extend([child.MBR['y1'], child.MBR['y2']])
        # I update the MBR of the node with the min and max coordinates
        node.MBR = {
            'x1': min(x_list),
            'x2': max(x_list),
            'y1': min(y_list),
            'y2': max(y_list)
        }

# I create an R-tree from a list of points
def main(points_list):
    rtree = RTree()
    for point in points_list:
        rtree.insert(rtree.root, point)
    return rtree  # I return the constructed R-tree
