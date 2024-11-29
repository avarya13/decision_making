import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task_1.task import parse_tree_to_edges


def build_relationship_matrix(json_graph):
    """
    Build a relationship matrix from a given JSON tree structure.
    
    Args:
        json_graph (dict): The JSON tree structure representing the relationships.
    
    Returns:
        pd.DataFrame: The DataFrame representing the relationship matrix.
    """

    # Convert the JSON tree to a list of edges
    edges = parse_tree_to_edges(json_graph)  # Capture the edges returned by the function
    print(f'Pairs "parent-child": {edges}')

    relationship_counts = {}

    # Initialize all nodes in the relationship_counts dictionary
    for parent, child in edges:
        if parent not in relationship_counts:
            relationship_counts[parent] = initialize_relationship_dict()
        if child not in relationship_counts:
            relationship_counts[child] = initialize_relationship_dict()

    # Count relationships
    # Immediate relationships (swap Г1 and Г2)
    for parent, child in edges:
        relationship_counts[parent]['Immediate Subordinate (Г2)'] += 1  # Mark that parent has a child
        relationship_counts[child]['Immediate Supervisor (Г1)'] += 1  # Mark that child has a parent

    # Create a map for indirect relationships
    indirect_relationship_map = {k: [] for k in relationship_counts.keys()}
    for parent, child in edges:
        indirect_relationship_map[parent].append(child)  # Build a tree structure for indirect counting

    # Count indirect relationships (swap Г3 and Г4)
    for node in relationship_counts.keys():
        relationship_counts[node]['Indirect Subordinate (Г4)'] = count_descendants(node, indirect_relationship_map)

    # To count indirect supervisors, we build the reverse mapping
    ancestor_map = {k: [] for k in relationship_counts.keys()}
    for parent, child in edges:
        ancestor_map[child].append(parent)  # Build a tree structure for ancestors

    # Count indirect supervisors
    for node in relationship_counts.keys():
        relationship_counts[node]['Indirect Supervisor (Г3)'] = count_ancestors(node, ancestor_map)

    # Count co-subordinate relationships
    for parent, child in edges:
        siblings = [sibling for sibling in indirect_relationship_map.get(parent, []) if sibling != child]
        relationship_counts[child]['Co-subordinate (Г5)'] = len(siblings)

    # Create a DataFrame for visualization
    df = pd.DataFrame(relationship_counts)
    df.index.name = 'Node'

    return df.sort_index(axis=1)


def initialize_relationship_dict():
    """
    Initialize the relationship dictionary for each node.
    
    Returns:
        dict: A dictionary with keys for each type of relationship.
    """
    return {
        'Immediate Supervisor (Г1)': 0,
        'Immediate Subordinate (Г2)': 0,
        'Indirect Supervisor (Г3)': 0,
        'Indirect Subordinate (Г4)': 0,
        'Co-subordinate (Г5)': 0
    }


# Function to recursively count ancestors
def count_ancestors(node, ancestor_map):
    """
    Recursively count the ancestors of a node.

    Args:
        node (str): The node whose ancestors are being counted.
        ancestor_map (dict): A mapping of each node to its ancestors.
    
    Returns:
        int: The number of ancestors for the given node.
    """
    count = 0
    if node in ancestor_map:
        for parent in ancestor_map[node]:
            count += 1 + count_ancestors(parent, ancestor_map)
    return count


# Function to recursively count descendants
def count_descendants(node, indirect_relationship_map):
    """
    Recursively count the descendants of a node.

    Args:
        node (str): The node whose descendants are being counted.
        indirect_relationship_map (dict): A mapping of each node to its descendants.
    
    Returns:
        int: The number of descendants for the given node.
    """
    count = 0
    if node in indirect_relationship_map:
        for child in indirect_relationship_map[node]:
            count += 1 + count_descendants(child, indirect_relationship_map)
    return count


def main():
    # Example usage with a predefined JSON tree
    json_graph = {
        "1": {
            "2": {
                "3": {},
                "4": {
                    "5": {},
                    "6": {}
                }
            }
        }
    }

    # Build the relationship matrix
    df = build_relationship_matrix(json_graph)
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv('relationship_matrix.csv')


if __name__ == "__main__":
    main()
