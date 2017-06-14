# create_and_display_pointclouds
Use python to read JSON file to create pointclouds with xyz and rgb, and use rviz based on ROS to display the pointcloud.
The method to use is input the following command after cloning the code.

'python json2pcl.py ./reconstruction.json'

Then input 'rosrun rviz rviz' in another terminal and add pointcloud2 of the topic called 'CreatePointCloud', you will see the pointcloud with color in rviz.
Enjoy!

Considering the structure of the ROS file system, clone the code and put these in ROS workspace, for example, put all the files in /catkin_ws/src/display_pointcloud/.
Then input 'catkin_make' in terminal. Of course, you can ignore that.
