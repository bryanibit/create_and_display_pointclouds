import json
import numpy as np
import os
import os.path
import argparse
import rospy
import logging; logger = logging.getLogger("morse." + __name__)
import roslib; roslib.load_manifest('sensor_msgs')
import struct
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import String

def publish_cloud_point(colorlist, xyzlist, count):
    pub = rospy.Publisher('CreatePointCloud', PointCloud2, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1)  # 10hz

    rgb_points = PointCloud2()
    rgb_points.header.stamp = rospy.get_rostime()
    rgb_points.header.frame_id = 'map'
    rgb_points.height = 1
    rgb_points.width = int(count)
    rgb_points.is_dense = False
    rgb_points.is_bigendian = False
    rgb_points.fields.append(PointField(
        name="x", offset=0, datatype=PointField.FLOAT32, count=1))
    rgb_points.fields.append(PointField(
        name="y", offset=4, datatype=PointField.FLOAT32, count=1))
    rgb_points.fields.append(PointField(
        name="z", offset=8, datatype=PointField.FLOAT32, count=1))
    rgb_points.fields.append(PointField(
        name="rgb", offset=16, datatype=PointField.FLOAT32, count=1))
    rgb_points.point_step = 32
    rgb_points.row_step = rgb_points.point_step * rgb_points.width
    buffer = []
    for (color,xyz) in zip(colorlist, xyzlist):
        buffer.append(struct.pack('ffffBBBBIII', xyz[0], xyz[1],
                                  xyz[2], 1.0, color[2], color[1], color[0], 0,0,0,0))
    rgb_points.data="".join(buffer)

    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        # rospy.loginfo(hello_str)
        pub.publish(rgb_points)
        rate.sleep()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot matches between images')
    parser.add_argument('dataset',
                        help='path should include reconstruction.meshed.json')
    args = parser.parse_args()
    path = args.dataset
    with open(path, 'r') as fout:
        datas = json.load(fout)
    # Because reconstruction.json is big list, there must be [0]
    print 'There are {} points in all'.format(len(datas[0]['points']))
    colorlist=[]
    xyzlist=[]
    for track_id, data in datas[0]['points'].items():
        # fin.write('%g,%g,%g,%d,%d,%d\n' % (data['coordinates'][0], data['coordinates'][1], data['coordinates'][2], data['color'][0], data['color'][1], data['color'][2]))
        colorlist.append(data['color'])
        xyzlist.append(data['coordinates'])
    # print colorlist
    print 'Add json to python list'
    try:
        publish_cloud_point(colorlist, xyzlist, len(datas[0]['points']))
    except rospy.ROSInterruptException:
        print 'Do not publish'




    

