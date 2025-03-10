"""
Utility functions for the entity tagging project
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import json
import argparse


def plot_metrics(data, title=None, save_path=None):
    """
    Plot model evaluation metrics
    
    Args:
        data (dict): Model evaluation metrics dictionary
        title (str, optional): Title for the plot
        save_path (str, optional): Path to save the plot image
        
    Returns:
        None
    """
    # Extract the overall metrics
    overall_metrics = {
        'p': data['ents_p'],
        'r': data['ents_r'],
        'f': data['ents_f']
    }

    # Extract the entity-specific metrics
    entity_metrics = data['ents_per_type']

    # Convert the data to a DataFrame for easier plotting
    entity_categories = list(entity_metrics.keys())
    entity_p = [entity_metrics[ent]['p'] for ent in entity_categories]
    entity_r = [entity_metrics[ent]['r'] for ent in entity_categories]
    entity_f = [entity_metrics[ent]['f'] for ent in entity_categories]

    # Create a DataFrame for entity-specific metrics in long format
    df_entity = pd.DataFrame({
        'Entity Category': entity_categories * 3,  # Repeating the entity categories for each metric (p, r, f)
        'Metric': ['p'] * len(entity_categories) + ['r'] * len(entity_categories) + ['f'] * len(entity_categories),
        'Value': entity_p + entity_r + entity_f
    })

    # Create a DataFrame for overall metrics (one row for each metric)
    df_overall = pd.DataFrame({
        'Entity Category': ['Overall'] * 3,
        'Metric': ['p', 'r', 'f'],
        'Value': [overall_metrics['p'], overall_metrics['r'], overall_metrics['f']]
    })

    # Concatenate the entity-specific and overall metrics
    df_combined = pd.concat([df_entity, df_overall], ignore_index=True)

    # Set up the plot
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid")

    # Plot the bars
    sns.barplot(x="Entity Category", y="Value", hue="Metric", data=df_combined, palette="Set2")

    # Customize the plot
    plot_title = title or "Overall vs Entity-Specific Metrics (p=precision, r=recall, f=f1 score) by Entity Category"
    plt.title(plot_title, fontsize=14)
    plt.xlabel("Entity Category", fontsize=12)
    plt.ylabel("Metric Value", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Metric", loc="upper right")
    plt.tight_layout()
    
    # Save the plot if a path is provided
    if save_path:
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    
    # Show the plot
    plt.show()


def compare_metrics(train_data, test_data, title=None, save_path=None):
    """
    Compare and plot training and test metrics
    
    Args:
        train_data (dict): Training evaluation metrics dictionary
        test_data (dict): Test evaluation metrics dictionary
        title (str, optional): Title for the plot
        save_path (str, optional): Path to save the plot image
        
    Returns:
        None
    """
    # Extract metrics
    metrics = {
        'Train Precision': train_data['ents_p'],
        'Train Recall': train_data['ents_r'],
        'Train F-score': train_data['ents_f'],
        'Test Precision': test_data['ents_p'],
        'Test Recall': test_data['ents_r'],
        'Test F-score': test_data['ents_f']
    }
    
    # Create DataFrame
    df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
    
    # Set up the plot
    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    
    # Plot the bars
    ax = sns.barplot(x="Metric", y="Value", data=df, palette="Set2")
    
    # Add value labels on top of bars
    for i, v in enumerate(df['Value']):
        ax.text(i, v + 0.01, f"{v:.4f}", ha='center')
    
    # Customize the plot
    plot_title = title or "Comparison of Training and Test Metrics"
    plt.title(plot_title, fontsize=14)
    plt.xlabel("", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot if a path is provided
    if save_path:
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
        plt.savefig(save_path)
        print(f"Comparison plot saved to {save_path}")
    
    # Show the plot
    plt.show()


def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description="Visualize model evaluation metrics")
    parser.add_argument("--input", required=True, 
                        help="Path to the JSON file containing evaluation metrics")
    parser.add_argument("--compare", 
                        help="Path to another JSON file to compare metrics with")
    parser.add_argument("--output", 
                        help="Path to save the plot image")
    parser.add_argument("--title", 
                        help="Title for the plot")
    
    args = parser.parse_args()
    
    # Load the evaluation metrics
    with open(args.input, 'r') as f:
        data = json.load(f)
    
    if args.compare:
        # If comparing two sets of metrics
        with open(args.compare, 'r') as f:
            compare_data = json.load(f)
        
        # Determine which is train and which is test
        if 'train' in data and 'test' in data:
            # If the file contains both train and test metrics
            compare_metrics(data['train'], data['test'], args.title, args.output)
        elif 'train' in compare_data and 'test' in compare_data:
            # If the comparison file contains both train and test metrics
            compare_metrics(compare_data['train'], compare_data['test'], args.title, args.output)
        else:
            # Assume the first file is train and the second is test
            compare_metrics(data, compare_data, args.title, args.output)
    else:
        # If only visualizing one set of metrics
        if 'train' in data and 'test' in data:
            # If the file contains both train and test metrics
            print("File contains both train and test metrics. Visualizing test metrics.")
            plot_metrics(data['test'], args.title, args.output)
        else:
            # Visualize the provided metrics
            plot_metrics(data, args.title, args.output)


if __name__ == "__main__":
    main()
