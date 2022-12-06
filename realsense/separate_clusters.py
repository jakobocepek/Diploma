import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

pcd = o3d.io.read_point_cloud("realsense\oblaki_blizu\PC_6.ply")

#pcd, ind = pcd.remove_radius_outlier(nb_points=1000, radius=0.05)

#labels = np.array(pcd.cluster_dbscan(eps=0.02, min_points=10))
#print(pcd, len(labels), max(labels)+1)

for i in range(50):
    pcd.points.append([0,0,-i/30])

o3d.visualization.draw_geometries([pcd])