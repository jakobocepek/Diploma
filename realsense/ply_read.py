import open3d as o3d
import numpy as np

pts = []
i = 1
while i<4:
    pcd_i = o3d.io.read_point_cloud("realsense\oblaki\PC_" + str(i) + ".ply")
    i += 1

    if not pcd_i.has_points():
        break
    pts.append(np.asarray(pcd_i.points))

pts_join = np.concatenate(pts, axis=0)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pts_join)

o3d.visualization.draw_geometries([pcd])
