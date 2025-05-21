import cv2
from sklearn.cluster import KMeans
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


c_data_path = "1"

def get_feature(img):
    intensity = img.sum(axis=1)
    intensity = intensity.sum(axis=0) / (255 * img.shape[0] * img.shape[1])
    return intensity
def load_data(data_path=c_data_path):
        X = []
        L = []
        for file in os.listdir(data_path):
            c_x = get_feature(cv2.imread(os.path.join(data_path, file)))
            X.append(c_x)
            L.append(file)
        X = np.array(X)
        L = np.array(L)
        return X,L

X,L = load_data()
#elbow
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(X)
    distortions.append(kmeanModel.inertia_)

plt.figure(figsize=(8,5))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('Elbow Method')
plt.show()

kmeans = KMeans(n_clusters=2).fit(X)
for i in range(len(kmeans.labels_)):
    print(kmeans.labels_[i]," - ", L[i])


n_row = 3
n_col=3
for i in range(2):
    _, axs = plt.subplots(n_row, n_col)
    axs = axs.flatten()
    for img, ax in zip(L[ kmeans.labels_ == i], axs):
        ax.imshow(mpimg.imread(os.path.join(c_data_path,img)))
    plt.tight_layout()
    plt.show()