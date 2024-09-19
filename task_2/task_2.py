import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task_1.task_1 import parse_tree_to_edges

def main():
    # Example JSON tree
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
    # Immediate relationships
    for parent, child in edges:
        relationship_counts[parent]['Immediate Supervisor (Г1)'] += 1  # Count children
        relationship_counts[child]['Immediate Subordinate (Г2)'] += 1  # Mark parent exists
    
    # Create a map for indirect relationships
    indirect_relationship_map = {k: [] for k in relationship_counts.keys()}
    for parent, child in edges:
        indirect_relationship_map[parent].append(child)  # Build a tree structure for indirect counting

    # Function to recursively count descendants
    def count_descendants(node):
        count = 0
        if node in indirect_relationship_map:
            for child in indirect_relationship_map[node]:
                count += 1 + count_descendants(child)
        return count

    # Count indirect relationships
    for node in relationship_counts.keys():
        relationship_counts[node]['Indirect Supervisor (Г3)'] = count_descendants(node)
    
    # To count indirect subordinates, we build the reverse mapping
    ancestor_map = {k: [] for k in relationship_counts.keys()}
    for parent, child in edges:
        ancestor_map[child].append(parent)  # Build a tree structure for ancestors

    # Function to recursively count ancestors
    def count_ancestors(node):
        count = 0
        if node in ancestor_map:
            for parent in ancestor_map[node]:
                count += 1 + count_ancestors(parent)
        return count

    # Count indirect subordinates
    for node in relationship_counts.keys():
        relationship_counts[node]['Indirect Subordinate (Г4)'] = count_ancestors(node)

    # Count co-subordinate relationships
    for parent, child in edges:
        siblings = [sibling for sibling in indirect_relationship_map.get(parent, []) if sibling != child]
        relationship_counts[child]['Co-subordinate (Г5)'] = len(siblings) 
        """ for sibling in siblings:
            relationship_counts[sibling]['Co-subordinate (Г5)'] += 1  # Ensure sibling counts are mutual """

    # Create a DataFrame for visualization
    df = pd.DataFrame(relationship_counts)
    df.index.name = 'Node'
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv('relationship_matrix.csv')

def initialize_relationship_dict():
    return {
        'Immediate Supervisor (Г1)': 0,
        'Immediate Subordinate (Г2)': 0,
        'Indirect Supervisor (Г3)': 0,
        'Indirect Subordinate (Г4)': 0,
        'Co-subordinate (Г5)': 0
    }

# Execute the main function
if __name__ == "__main__":
    main()

# Usage:
# python .\task_2\task_2.py 