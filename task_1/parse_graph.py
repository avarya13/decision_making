import json

# List of edges (parent-child pairs)
edges = []

# Function to convert a JSON tree into a list of edges
def parse_tree_to_edges(tree, parent=None):
    for node, children in tree.items():
        if parent:
            edges.append((parent, node))
        parse_tree_to_edges(children, node)

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

    # Show graph as a list of tuples 'parent-node'

    print(edges)

# Execute the main function
if __name__ == "__main__":
    main()
