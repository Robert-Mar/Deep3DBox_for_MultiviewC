# Deep3DBox_for_MultiviewC
 Pytorch implementation for Deep3DBox on [MultiviewC dataset](https://github.com/Robert-Mar/MultiviewC).
 
## Visualization 
![alt text](https://github.com/Robert-Mar/Deep3DBox_for_MultiviewC/blob/main/results/C0.png "Visualization of Camera1")
![alt text](https://github.com/Robert-Mar/Deep3DBox_for_MultiviewC/blob/main/results/C6.png "Visualization of Camera6")

## Model Checkpoint
2D detection part: [FasterRCNN](https://drive.google.com/file/d/1JQPuuKuZxyvEqjgujSS1m3FvfuoWokDM/view?usp=sharing).
3D detection part: [Deep3DBox](https://drive.google.com/file/d/1S6ttmu_V6Hle0U4frHEopY79ltyQL90Z/view?usp=sharing).
Download the checkpoint and copy them in weights folder, which can help you complete prediction.

## Angle Adjustment
Different from [Kitti](http://www.cvlibs.net/datasets/kitti/) dataset, MultiviewC contains seven cameras located at four corners of field.There are several angle information thate need to be explained.
```

theta_w_global [Orient_w]: cattle's global orientation in world coordinate
    
theta_ref_global: cattle's global orientation in reference camera coordinate
    
theta_c_global [Orient_c]: cattle's global orientation in specific camera coordinate  
    
theta_local [Alpha]: cattle's local orientation in specific camera coordinate 
    
theta_ray: the angle between the ray from cammera center to objects' center 
                 and the y axis of camera.  (angle of camera coordinate)
    
Rz: the rotation angle of camera on Z-axis of the world coordinate

[FORMULA]
theta_ref_global = theta_w_global + 90

theta_c_global = theta_ref_global - R_z

theta_c_global = theta_local + theta_ray
```
More details about rotatin angle refer to this [note](https://github.com/Robert-Mar/Deep3DBox_for_MultiviewC/tree/main/notes).

## Reference
* 3D Bounding Box Estimation Using Deep Learning and Geometry. [Paper](https://arxiv.org/abs/1612.00496).
* PyTorch implementation for this paper. [Link](https://github.com/skhadem/3D-BoundingBox).
