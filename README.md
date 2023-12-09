# Volume Estimation through Computer Vision aided 3D reconstruction

- This pipeline performs the volume estimation in 3 steps: segmentation ⇒ 3D reconstruction ⇒ volume estimation
    - Segmentation: [YOLOv5](https://github.com/ultralytics/yolov5)
    - 3D reconstruction: [3DR2-N2 Official Version](https://github.com/chrischoy/3D-R2N2) and [3DR2-N2 PyTorch Version](https://github.com/heromanba/3D-R2N2-PyTorch)
    - Volume Calculation: [Trimesh](https://github.com/mikedh/trimesh)

## Installation
You can follow the instruction below to install the virtual environment.

- Clone this repository
```bash
git clone https://github.com/kalebmes/volume_estimation.git
```

- Create virtual environment and install required packages. Example is given below using `conda`

```bash
cd volume_estimation
conda create -n 3D-volume-estimator
conda activate 3D-volume-estimator
pip install -r requirements.txt
```
## Segmentation

### Running YOLOv5 instance segmentation
- First please download the pretrained model `obj_seg.pt` from this Link (Todo) and store it under `yolov5_det/` directory. For more information, please visit the official README.md of the [YOLOv5 Repository](https://github.com/ultralytics/yolov5)

- Navigate to the `yolov5_det/` directory

```bash
cd yolov5_det
```

- Then run the instance segmentation script using the given command. Be sure to change the `dataset_directory/` to the actual directory of the objects, and `obj_seg_directory` to the directory of the downloaded `obj_seg.pt` model

```bash
python segment/predict.py --source dataset_directory/ --weights obj_seg_directory/ --save-txt
```

- the results are stored under the `runs/` directory. Please take a note of the output path and proceed to the cropping stage.
![demo](https://github.com/kalebmes/volume_estimation/imgs/detected_demo.jpg)


### Cropping the desired objects

- Navigate back to the parent directory and run the following python file. Please make sure to specify the original directory of the objects, which was denoted as `dataset_directory/` previously, and the output of the segmented objects directory and the desired save path

```bash
python crop_image_yolov5_bb.py 
```
![cropped](https://github.com/kalebmes/volume_estimation/imgs/cropped_demo.jpg)


## 3D Reconstruction
- Please download pretrained model(ResidualGRUNet), and put ```checkpoint.pth``` under ```output/ResidualGRUNet/default_model```.
- Todo: Add the Google drive link here

- Run the following command. Please make sure to specify the folder of the cropped images, and the output directory of the saved projections

```bash
python 3D_recon_script.py
```

## Volume Calculation
- Run the following command, which generates a .csv file of predicted volumes along with their accuracies using Trimesh module

```bash
python calculate_volume.py
```

## Todo
Replicate the Code
