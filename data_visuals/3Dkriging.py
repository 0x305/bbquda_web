#%%
import numpy as np 
import pandas as pd
from pykrige.ok3d import OrdinaryKriging3D
from matplotlib import pyplot as plt
from matplotlib import cm
# %%
# Lat, Long, Depth, Val
data = np.array(
[
    [0.1, 0.1, 0.3, 0.9],
    [0.2, 0.1, 0.4, 0.8],
    [0.1, 0.3, 0.1, 0.9],
    [0.5, 0.4, 0.4, 0.5],
    [0.3, 0.3, 0.2, 0.7],
]
)
gridx = np.arange(0.0, 0.6, 0.05)
gridy = np.arange(0.0, 0.6, 0.01)
gridz = np.arange(0.0, 0.6, 0.1)
# %%
ok3d = OrdinaryKriging3D(
data[:, 0], data[:, 1], data[:, 2], data[:, 3], variogram_model="gaussian", enable_plotting=True, verbose=True)
k3d1, ss3d = ok3d.execute("grid", gridx, gridy, gridz)
# %%
zg, yg, xg = np.meshgrid(gridz, gridy, gridx, indexing='ij')
# %%
fig3d = plt.figure(figsize=(5,5))
plot3d = fig3d.add_subplot(111, projection='3d')
plot3d.scatter(xg, yg, zg, c=k3d1)

# %%
print(k3d1.shape)
# %%
