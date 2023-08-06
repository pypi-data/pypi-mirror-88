import pyrealsense2 as rs
import numpy as np
import cv2

class RealSenseL515:
    def __init__(self, enable_BGR = True, enable_depth = True, \
        bgr_width = 1280, bgr_height = 720, depth_width = 640, \
                        depth_height = 480, show_image = False):
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.BGR_width = bgr_width
        self.BGR_height = bgr_height
        self.depth_width = depth_width
        self.depth_height = depth_height

        self.enable_BGR = enable_BGR
        self.enable_depth = enable_depth
        self.show_image = show_image

        if self.enable_BGR:
            self.config.enable_stream(rs.stream.color, self.BGR_width , self.BGR_height, rs.format.bgr8, 30)
        if self.enable_depth:
            self.config.enable_stream(rs.stream.depth, self.depth_width, self.depth_height, rs.format.z16, 30)
        self.pipeline.start(self.config)

    def get_Image(self):
        frames = self.pipeline.wait_for_frames()
        got_BGR = True
        got_depth = True
        if self.enable_BGR:
            color_frame = frames.get_color_frame()
            if not color_frame:
                got_BGR = False
            color_image = np.asanyarray(color_frame.get_data())
            color_image = cv2.resize(color_image,(self.BGR_width,self.BGR_height))
        else:
            color_image = None
        if not got_BGR:
            color_image = None

        if self.enable_depth:
            depth_frame = frames.get_depth_frame()
            if not color_frame:
                got_depth = False
            depth_image = np.asanyarray(depth_frame.get_data())
            depth_image = cv2.resize(depth_image,(self.depth_width,self.depth_height))
            if self.show_image:
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        else:
            depth_image = None
        if not got_depth:
            depth_image = None

        if self.show_image:
            if got_BGR and got_depth:
                return True,color_image,depth_image,depth_colormap
            else:
                return False,color_image,depth_image,depth_colormap
        else:
            if got_BGR and got_depth:
                return True,color_image,depth_image
            else:
                return False,color_image,depth_image

if __name__ == '__main__':
    l515 = RealSenseL515()
    while True:
        success, color, depth = l515.get_Image()
        cv2.imshow("color",color)
        cv2.imshow("depth",depth)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break