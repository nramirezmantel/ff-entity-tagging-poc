import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

## below should be functionised to produce a visual of train and test metrics
data = test_performance_dict

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
plt.title("Overall vs Entity-Specific Metrics (p=precision, r=recall, f=f1 score) by Entity Category", fontsize=14)
plt.xlabel("Entity Category", fontsize=12)
plt.ylabel("Metric Value", fontsize=12)
plt.xticks(rotation=45)
plt.legend(title="Metric", loc="upper right")

# Show the plot
plt.tight_layout()
plt.show()