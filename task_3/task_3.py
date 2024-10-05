import sys
import os
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task_2.task_2 import build_relationship_matrix

def calculate_entropy(probabilities):
    """
    Calculate entropy for a given list of probabilities using the formula:
    H = -sum(p * log2(p)) for p > 0.
    
    Args:
        probabilities (list or array): The probabilities for which entropy is to be calculated.
        
    Returns:
        float: The entropy value.
    """
    probabilities = np.array(probabilities)
    probabilities = probabilities[probabilities > 0]  # Avoid log(0)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

def calculate_overall_entropy(df):
    """
    Calculate the overall entropy across all nodes and all relationship types.
    
    Args:
        df (pd.DataFrame): The relationship matrix where each row corresponds to a relationship type
                           and each column corresponds to a node.
    
    Returns:
        float: The overall (global) entropy value.
    """
    num_nodes = len(df.columns)
    
    if num_nodes <= 1:
        print("Entropy calculation is not possible with one or fewer nodes.")
        return 0.0  

    # Normalize values across all nodes for each relationship type
    probabilities = df / (num_nodes - 1)
    
    # Calculate the overall entropy
    overall_entropy = calculate_entropy(probabilities.values.flatten())
    
    return overall_entropy


def main():
    # Example usage with a predefined JSON tree
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

    # Build the relationship matrix
    df = build_relationship_matrix(json_graph)
    print(df)

    # Calculate the overall (global) entropy
    overall_entropy = calculate_overall_entropy(df)
    print(f"\nOverall Entropy: {overall_entropy:.4f}")


if __name__ == "__main__":
    main()
