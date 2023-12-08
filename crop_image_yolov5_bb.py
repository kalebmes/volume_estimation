from PIL import Image, ImageDraw
import numpy as np
import os
import shutil

def crop_segmented_region(txt_file_path, image_path, save_path, expansion_factor=1.5):
    # Load the YOLOv5 data from the text file
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()

    image_name = image_path.split('/')[-1].split('.jpg')[0]
    # Load the image
    img = Image.open(image_path)
    img_width, img_height = img.size

    for i, line in enumerate(lines):
        # Parse the line into class label and points
        parts = line.strip().split()
        class_label = int(parts[0])
        points = np.array([(float(parts[i]) * img_width, float(parts[i + 1]) * img_height) for i in range(1, len(parts), 2)])

        # Calculate the bounding box dimensions
        min_x = np.min(points[:,0])
        max_x = np.max(points[:,0])
        min_y = np.min(points[:,1])
        max_y = np.max(points[:,1])
        
        # Calculate the center of the bounding box
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        # Apply the expansion factor to the bounding box dimensions
        width = (max_x - min_x) * expansion_factor
        height = (max_y - min_y) * expansion_factor
        
        # Calculate the new bounding box with the expansion factor
        new_min_x = max(center_x - width / 2, 0)
        new_max_x = min(center_x + width / 2, img_width)
        new_min_y = max(center_y - height / 2, 0)
        new_max_y = min(center_y + height / 2, img_height)
        
        # Crop the image to the new bounding box
        cropped_img = img.crop((int(new_min_x), int(new_min_y), int(new_max_x), int(new_max_y)))

        # Create a mask for the object within the new bounding box
        mask = Image.new('L', cropped_img.size, 0)
        bbox_points = [(x - new_min_x, y - new_min_y) for x, y in points]
        ImageDraw.Draw(mask).polygon(bbox_points, outline=1, fill=1)

        # Convert the mask and cropped image to numpy arrays
        mask_np = np.array(mask)
        cropped_img_np = np.array(cropped_img)

        # Apply the mask to the cropped image
        cropped_img_np[mask_np == 0] = (255, 255, 255)  # Setting the outside of the object to white

        # Convert the masked image back to a PIL Image and save it
        masked_img = Image.fromarray(cropped_img_np)
        masked_img.save(os.path.join(save_path, f'segmented_{image_name}_{i}.jpg'))
        print('Saved the cropped image under the path:', os.path.join(save_path, f'segmented_{image_name}_{i}.jpg'))
        

folder_path = '/root/yolov5/runs/predict-seg/exp3'
original_folder = '/root/Wegnal/Segmentation/55_dummies_labeled'
# save_path = '/root/Wegnal/Segmentation/폐기물더미이미지zip_cropped'
save_path = '/root/Wegnal/Segmentation/55_dummies_labeled_cropped_bb'
# video_name = 'KakaoTalk_20230308_174212496'
# save_path = f'/root/Wegnal/Segmentation/{video_name}_cropped'

if not os.path.exists(save_path):
    os.mkdir(save_path)
    print('created directory:', save_path)

for file in os.listdir(folder_path):
    # if file.endswith('.txt'):
    if file.endswith('.jpg'):# and file.startswith(video_name):
        txt_file_path = os.path.join(folder_path, 'labels', file.replace('.jpg', '.txt'))
        if os.path.exists(txt_file_path):
            image_path = os.path.join(original_folder, file)
            crop_segmented_region(txt_file_path, image_path, save_path, expansion_factor=1.25)
            # print(txt_file_path, image_path, save_path)
        else:
            print('txt file does not exist:', txt_file_path)
print('*'*50)
print('cropped all images')
print('*'*50)

print()
print('grouping pics of similar objects into one folder')
# group pics of similar objects into one folder


# cropped_pics_path = save_path

for image in os.listdir(save_path):
    
    folder_name = image.split()[0]
    folder_path = os.path.join(cropped_pics_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    shutil.move(os.path.join(cropped_pics_path, image), os.path.join(folder_path, image))
    # and then rename the moved images to 0.jpg, 1.jpg, 2.jpg, ...
    for i, image in enumerate(os.listdir(folder_path)):
        os.rename(os.path.join(folder_path, image), os.path.join(folder_path, f'{i}.jpg'))
    print('moved', image, 'to', folder_path)