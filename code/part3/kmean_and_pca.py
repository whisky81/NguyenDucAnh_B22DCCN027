# %%
import pandas as pd  # type: ignore
import numpy as np  # type: ignore

df = pd.read_csv('../part1/results.csv') 
data = df[df.columns[4:]].copy()
data.dropna(axis='columns', inplace=True)

# %% [markdown]
# 1. scale the data to standardize values

# %%
data = ((data - data.min()) / (data.max() - data.min())) * 9 + 1

# %% [markdown]
# 2. initialize random centroids

# %%
def random_centroids(data, k): 
    centroids = [] 

    for _ in range(k): 
        centroid = data.apply(lambda x: float(x.sample().iloc[0])) 
        centroids.append(centroid)  

    return pd.concat(centroids, axis=1)  


# centroids = random_centroids(data, k=3) 

# %% [markdown]
# 3. get labels for each data point

# %%
def get_labels(data, centroids): 
    distances = centroids.apply(lambda x: np.sqrt(((data - x) ** 2).sum(axis=1)))  
    return distances.idxmin(axis=1)

# labels = get_labels(data, centroids)

# labels
# type(labels)

# %% [markdown]
# 4. create new centroids based on mean values of each cluster

# %%
def new_centroids(data, labels, k):
    centroids = data.groupby(labels).apply(lambda x: np.exp(np.log(x).mean())).T

    
    return centroids  

# %% [markdown]
# 5. plot centroids 
# 6. repeat 3-5 untill the centroids stop changing

# %%

from sklearn.decomposition import PCA # type: ignore
import matplotlib.pyplot as plt # type: ignore
from IPython.display import clear_output # type: ignore
import time 



# %%
# i dont understand
def plot_clusters(data, labels, centroids, iteration):
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(data)
    centroids_2d = pca.transform(centroids.T)
    time.sleep(1)
    clear_output(wait=True)
    plt.title(f'Iteration {iteration}')
    plt.scatter(x=data_2d[:,0], y=data_2d[:,1], c=labels)
    plt.scatter(x=centroids_2d[:,0], y=centroids_2d[:,1])
    plt.savefig("../../images/kmeans pca.png")
    plt.show()

# %%
# i dont understand
max_iterations = 100
k = 3

centroids = random_centroids(data, k)
old_centroids = pd.DataFrame()
iteration = 1

while iteration < max_iterations and not centroids.equals(old_centroids):
    old_centroids = centroids
    
    labels = get_labels(data, centroids)
    centroids = new_centroids(data, labels, k)
    if centroids.equals(old_centroids):
        plot_clusters(data, labels, centroids, iteration)
    iteration += 1

