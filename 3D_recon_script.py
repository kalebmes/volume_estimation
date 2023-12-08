import os

folders_path = '/root/Wegnal/Segmentation/55_dummies_labeled_cropped_bb'
parent_folder_name = folders_path.split('/')[-1].replace('_cropped_bb', '')
for folder in os.listdir(folders_path):
    folder_path = os.path.join(folders_path, folder)
    volume_number = folder.split('segmented_')[-1]
    print('executed', f'python demo.py projections_{parent_folder_name}/projection_{volume_number}.obj {folder_path}')
    os.system(f'python demo.py projections_{parent_folder_name}/projection_{volume_number}.obj {folder_path}')