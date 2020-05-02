####
####   k-means  
####

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import seaborn as sns
import matplotlib.pyplot as plt
# tv = TfidfVectorizer(max_df = 0.4)
# tv_fit = tv.fit_transform(documents)
# for nu in range(len(tv_fit.A)):
#     plt.scatter(np.arange(len(tv_fit.A[nu])), tv_fit.A[nu])
import os

filelists = os.walk("Data/websites/textonly/")  
documents = []
for path,dir_list,file_list in filelists:  
    for file_name in file_list:
        print(file_name)
        with open(os.path.join(path, file_name), "r") as outf:
            documents.append(outf.read())

n_clusters = 6
pipeline = Pipeline([('feature_extraction', TfidfVectorizer(max_df=0.4)),   # ignore the rate of words appear more than 40%
                    ('clusterer', KMeans(n_clusters=n_clusters))
                    ])

pipeline.fit(documents)
labels = pipeline.predict(documents)   # labels have no meaning itself.

from collections import Counter
c = Counter(labels)
for cluster_number in range(n_clusters):
    print("Cluster {} contains {} samples------------".format(cluster_number,
                                                 c[cluster_number]))

terms = pipeline.named_steps['feature_extraction'].get_feature_names()
c = Counter(labels)
for cluster_number in range(n_clusters):
    print("*****Cluster {} contains {} samples".format(cluster_number,
                                                 c[cluster_number]))
    print("     Most Important terms")
    centroid = pipeline.named_steps['clusterer'].cluster_centers_[cluster_number]
    most_important = centroid.argsort()
    for i in range(5):
        term_index = most_important[-(i+1)]
        print("           {0} )  {1}  (score:   {2:.4f})".format(i+1, terms[term_index], centroid[term_index]))

#####
####   draw the heat map dor the data
#####


# from scipy.sparse import csr_matrix
# import numpy as np

# def create_coassociation_matrix(labels):
#     rows = []
#     cols = []
#     unique_labels = set(labels)
#     for label in unique_labels:
#         indices = np.where(labels == label)[0]
#         for index1 in indices:
#             for index2 in indices:
#                 rows.append(index1)
#                 cols.append(index2)
#     data = np.ones((len(rows), ))
#     return csr_matrix((data, (rows, cols)),   dtype='float')

# C = create_coassociation_matrix(labels)


# from scipy.sparse.csgraph import minimum_spanning_tree

# mst = minimum_spanning_tree(-C)
# pipeline.fit(documents)

# labels2 = pipeline.predict(documents)
# C2 = create_coassociation_matrix(labels2)
# C_sum = (C+C2)  / 2

# mst  = minimum_spanning_tree(-C_sum)
# mst.data[mst.data > -1] = 0



# from scipy.sparse.csgraph import connected_components
# number_of_clusters, labels = connected_components(mst)

# from sklearn.base import BaseEstimator, ClusterMixin

# class EAC(BaseEstimator, ClusterMixin):
#     def __init__(self, n_clusterings = 10, cut_threshold = 0.5, n_clusters_range = (3, 10)):
#         self.n_clusterings = n_clusterings
#         self.cut_threshold = cut_threshold
#         self.n_clusters_range = n_clusters_range
    
#     def fit(self, X, y=None):  ## 共斜矩阵  MST 最小生成树， 消除一些 低于thershold的 value
#         C = sum( ( create_coassociation_matrix(self._single_clustering(X))
#                  for i in range(self.n_clusterings)))
#         mst = minimum_spanning_tree(-C)
#         mst.data[mst.data > -self.cut_threshold] = 0
#         self.n_components, self.labels_ = connected_components(mst)
#         return self
    
#     def _single_clustering(self, X):
#         import numpy as np
#         n_clusters = np.randomom.randint(*self.n_clusters_range)
#         km = KMeans(n_clusters=n_clusters)
#         return km.fit_predict(X)
    
# pipeline = Pipeline( [ ('feature_extraction', TfidfVectorizer(max_df=0.4)), 
#                      ('clusterer', EAC())
#                      ])
