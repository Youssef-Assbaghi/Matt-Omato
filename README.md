# Matt-Omato
 Tomato Harvester Robot to automate agricultural work 



# Table of Contents
 
 <img src="https://user-images.githubusercontent.com/65310531/119140989-0d163100-ba45-11eb-8d57-a9c2259c4ec3.jpg" align="right" width="300" alt="header"/>

   * [What is this?](#1)
   * [Description](#2)
   * [Hardware Scheme](#3)
   * [Software Architecture](#4)
      * [3D Point Cloud tomato detection](#5)
        * [HSI Threshold Color](#HSI)
        * [PassThrough Filter](#P)
        * [Clustering and RANSAC](#CR)
      * [Inverse kinematics algorithm](#6)
   * [Simulation](#7)
   * [Testing and results](#8)
   * [3D pieces](#9)
   * [Amazing contributions](#9)   
   * [Video](#10)
   * [Authors](#11)



# What is this? <a name="1"></a>
This project is related to the subject of the third-year computing mention at the UAB of "Robotics, Language and Planning" . In it, a project of the creation of a robot through simulations has been carried out .

# Description <a name="2"></a>
Matt-Omato is a robot capable of harvesting tomatoes autonomously through different growing lines and deposit them in a box attached to the base.

The main mechanical component is a anthropomorphic 5-axis robotic arm plus clamp which allows you a sufficient range to harvest tomatoes you have on the growing lines on each side.  At the end of the arm it has a special 3-finger gripper which allows us to take the tomatoes more easily and correctly.

 Matt-Omato's movement through the tomato plants is linear. Moves back and forth through rails so you don't lose straight line  and thus avoid possible shock with the tomateras. Matt-Omato has two proximity sensors which allow him to change direction if he detects any object.
 
 The other most important part of Matt-Omato is the RGB-D camera that has built-in. Thanks to it it is able to detect the tomatoes and obtain the coordinates of them.  This will also allow us to define a threshold that types of tomatoes we agree to harvest and which we do not.
 
  Generally speaking Matt-Omato is able to:
  -  Detect tomato coordinates using a 3D point cloud.
  -  Calculate the angles of rotation of the arm motors in order to move the manipulator through inverse kinematics.
  -   Move autonomously through the tomato plants thanks to the rails and proximity sensors

# Hardware Scheme <a name="3"></a>
This is the hardware scheme made for Matt-Omato. In it we can find the existence of a NEMA engine for the base of the robotic arm which allows us to move 360 degrees.  You can also see a total of 6 servo motors which 5 of them are for the arm and one for RGB-D camera support  which gives us color and depth information about the captured scene. We can also find 2 DC motors for the movement of the wheels. And finally the two proximity sensors to be able to detect the greenhouse walls for example.
<img src="https://user-images.githubusercontent.com/65310531/119172049-b4a35b80-ba65-11eb-9e4f-c1f1f7883818.png" align="center" width="700" alt="hardware_scheme"/>

# Software Architecture <a name="4"></a>
In order to develop the software part of Matt-Omato, we have divided the development into two parts. 

In the diagram below you can see Matt-Omato's internal process in relation to the software. In it, there are two differentiated parts. On the one hand we have everything related to the computer vision that is going to be able to detect the tomatoes and get the coordinates of them. And on the other hand we have the calculation of the position of the robotic arm thanks to the inverse kinematics.

<img src="https://user-images.githubusercontent.com/65310531/119173768-fb925080-ba67-11eb-863e-a49f76284118.png" align="center" width="500" alt="software_scheme"/>

## 3D Point Cloud tomato detection <a name="5"></a>
 <img src="https://user-images.githubusercontent.com/65310531/119176651-a9532e80-ba6b-11eb-9cd7-0cd376f4e653.png" align="right" width="370" alt="cloud"/>
 In order to provide Matt-Omato with computer vision, it has been necessary to integrate an RGB-D camera that provides depth and color information. Thanks to this we are able to create the 3D point cloud of the scene.
 
In order to obtain the coordinates of the tomatoes at the end of the computer vision algorithm, the following steps have been followed to facilitate our work on the 3D point cloud and tomato detection

 
 ### HSI Threshold <a name="HSI"></a>
  

 At this stage we pass the RGB values obtained by the camera to the HSI color space which is more similar to human vision and easier to parameterize. Once we have the point cloud in this color space, we have defined a threshold which will allow us to keep only those points we are interested in. In this case with tomato colors such as medium ripe green, orange about to ripen and deep red representing a ripe tomato. These are the colors that we accept that Matt-Omato harvests.
 
  ### PassThrough Filter <a name="P"></a>
  At this stage the total number of points within the 3D cloud is reduced. The idea is to define a bounding box that limits us to a range in which to keep only those points that fall inside. In this way we will only keep the tomatoes that are close to the camera and remove those background points that the camera can detect. This will make the execution time very small.
  
  ### Clustering and RANSAC <a name="CR"></a>
  
  In order to detect all the tomatoes in the scene individually, it is necessary to develop an algorithm capable of separating all the groups of points. That is why we have used a clustering algorithm which allows us to group the points by groups establishing the minimum amount of points that we want to have to form one. In this way we also avoid possible noise that may have crept in from the previous stages.

Finally, in order to obtain the coordinates of the tomatoes, we have used a RANSAC algorithm to adjust the points of each cluster to the sphere shape defined by RANSAC. Using the "pyRansac3D" library we are able to obtain the centers of these spheres and therefore the centers of the tomatoes.

Requirements: Python 3, and its libraries numpy, math, matplotlib, cv2, open3d and pyransac3d

## Inverse Kinematics <a name="6"></a>

# Simulation <a name="6"></a>
In order to test Matt-Omato it has been necessary to use the CoppeliaSim software where we have the whole robot recreated in real size with all the hardware components and all the software components (Python). We have a total of 10 scenes where the difficulty varies according to the number of tomato plants, the number of tomatoes in each tomato plant, the size of the tomatoes and the color of the tomatoes.


| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://user-images.githubusercontent.com/65310531/119180838-19b07e80-ba71-11eb-97f6-aae2400aa4f3.gif">  Simple scene |  <img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://user-images.githubusercontent.com/65310531/119180891-2f25a880-ba71-11eb-8bc7-0e4447b9d191.gif"> Intermediate scene|<img width="1604" alt="screen shot 2017-08-07 at 12 18 15 pm" src="https://user-images.githubusercontent.com/65310531/119180920-38af1080-ba71-11eb-8b8e-4548070ea1fc.gif"> Difficult scene|
 
