import json

# List of edges (parent-child pairs)
edges = []

# Function to convert a JSON tree into a list of edges
def parse_tree_to_edges(tree, parent=None):
    for node, children in tree.items():
        if parent:
            edges.append((parent, node))
        parse_tree_to_edges(children, node)

# Function to find the children of a given node
def find_children(node, edges):
    children = [child for parent, child in edges if parent == node]
    return children

# Function to find the siblings of a given node
def find_siblings(node, edges):
    parent = find_parent(node, edges)
    if parent is None:
        return []  # No siblings if there is no parent
    siblings = []
    for p, child in edges:
        if p == parent and child != node:
            siblings.append(child)
    return siblings

# Function to find the parent of a given node
def find_parent(node, edges):
    for parent, child in edges:
        if child == node:
            return parent
    return None

# Main function
def main():
    # Example JSON tree
    json_graph = {
        "1": {
            "2": {
                "3": {
                    "5": {},
                    "6": {}
                },
                "4": {
                    "7": {},
                    "8": {}
                }
            }
        }
    }

    # Convert the JSON tree to a list of edges
    parse_tree_to_edges(json_graph)

    # Demonstrating usage of each function

    # Example 1: Find children of node "2"
    node = "2"
    children_of_node = find_children(node, edges)
    print(f"Children of node {node}: {children_of_node}")

    # Example 2: Find siblings of node "3"
    node = "3"
    siblings_of_node = find_siblings(node, edges)
    print(f"Siblings of node {node}: {siblings_of_node}")

    # Example 3: Find parent of node "6"
    node = "6"
    parent_of_node = find_parent(node, edges)
    print(f"Parent of node {node}: {parent_of_node}")

# Execute the main function
if __name__ == "__main__":
    main()
