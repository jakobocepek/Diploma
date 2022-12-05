## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image

# Configure depth and color streams
pipe = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# Start streaming
pipe.start(config)

colorizer = rs.colorizer()

def savePointCloud(i, pipe, colorizer):
    # Wait for the next set of frames from the camera
    frames = pipe.wait_for_frames()
    colorized = colorizer.process(frames)

    # Create save_to_ply object
    ply = rs.save_to_ply("realsense\oblaki_blizu\PC_" + str(i) + ".ply")

    # Set options to the desired values
    # In this example we'll generate a textual PLY with normals (mesh is already created by default)
    ply.set_option(rs.save_to_ply.option_ply_binary, True)
    ply.set_option(rs.save_to_ply.option_ply_normals, True)

    # Apply the processing block to the frameset which contains the depth frame and the texture
    ply.process(colorized)

    color_image = np.asanyarray(frames.get_color_frame().get_data())
    
    im = Image.fromarray(color_image)
    
    im.save("realsense\slike_blizu\pic_" + str(i) + ".jpeg")

try:
    i = 1
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipe.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        resized_depth_image = cv2.resize(depth_colormap, dsize=(640,360), interpolation=cv2.INTER_AREA)

        depth_colormap_dim = resized_depth_image.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, resized_depth_image))
        else:
            images = np.hstack((color_image, resized_depth_image))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)

        if cv2.waitKey(1) == 13:
            savePointCloud(i, pipe, colorizer)
            i += 1

        if cv2.getWindowProperty('RealSense',cv2.WND_PROP_VISIBLE) < 1:
            break
    
    cv2.destroyAllWindows()

except:
    # Stop streaming
    pipe.stop()



