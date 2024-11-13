#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 18:03:39 2024

@author: jonah
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Path to data folder
directory = '../GATSol/dataset/'

# Load the DataFrame with embeddings
df = pd.read_pickle(directory + 'eSol_Test.pkl')

# Reshape embeddings
embeddings = np.stack(df['embedding'].values)
embeddings = np.squeeze(embeddings)
print("Shape of embeddings:", embeddings.shape)  # Should be (num_sequences, embedding_dim)

# Apply PCA without specifying n_components to analyze full explained variance
pca = PCA()
pca.fit(embeddings)

# Calculate cumulative explained variance
cumsum = np.cumsum(pca.explained_variance_ratio_)
d = np.argmax(cumsum >= 0.95) + 1  # +1 because index 0 is the first component

print(f"Number of components needed for 95% variance: {d}")

# Plot cumulative explained variance
plt.figure(figsize=(10, 6))
plt.plot(cumsum, marker='o', linestyle='-', color='b', linewidth=2)
plt.axhline(y=0.95, color='r', linestyle='--', label='95% Explained Variance')
plt.axvline(x=d - 1, color='g', linestyle='--', label=f'{d} Components')
plt.xlabel('Number of Principal Components', fontsize=14, fontweight='bold')
plt.ylabel('Cumulative Explained Variance', fontsize=14, fontweight='bold')
plt.title('PCA: Cumulative Explained Variance', fontsize=16, fontweight='bold')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Perform PCA with the selected number of components
pca = PCA(n_components=d)
pca_embeddings = pca.fit_transform(embeddings)
print("Shape of reduced embeddings:", pca_embeddings.shape)

# Create a new DataFrame for the PCA components and concatenate
pca_columns = [f'PCA_{i+1}' for i in range(d)]
pca_df = pd.DataFrame(pca_embeddings, columns=pca_columns)
df = pd.concat([df, pca_df], axis=1)

# Save updated DataFrame
df.to_pickle(directory + 'eSol_Test_PCA.pkl')