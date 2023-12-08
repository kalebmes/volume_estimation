import trimesh
import os
import pandas as pd
import numpy as np

folders_path = '/root/Wegnal/Segmentation/55_dummies_labeled_cropped_bb'
parent_folder_name = folders_path.split('/')[-1].replace('_cropped_bb', '')

projections_path = f'/root/Wegnal/3D-R2N2-PyTorch/projections_{parent_folder_name}'
# df = pd.DataFrame(columns=['ground_truth_volume', 'volume (units)', 'real_world_volume (liters)'])
# db_directory = '/root/Wegnal/WEGNAL_DB_STRUCTURE_v0.9 (1).xlsx'
db_directory = '/root/Wegnal/3D-R2N2-PyTorch/0.actual volume_michael.csv'
# db_vols = pd.read_excel(db_directory, sheet_name='DB_2023MAY', engine='openpyxl', index_col=0)
db_vols = pd.read_csv(db_directory)

db_dict = {filename.split()[0]: volume for filename, volume in zip(db_vols['file_name'], db_vols['calculated_volume (mm3)'])}
db_dict_ea = {filename.split()[0]: ea for filename, ea in zip(db_vols['file_name'], db_vols['ea'])}

# print(db_dict['16.88_93_48_78_76_20_64_100_45_30_36_5_61_25_33_39_66'])
# print(db_dict_ea['16.88_93_48_78_76_20_64_100_45_30_36_5_61_25_33_39_66'])

df = pd.DataFrame()
ground_truths = []
product_names = []
calculated_vols = []
real_worl_vols = []
accuracies = []
diffs = []
eas = []
# scale_factors = []
for proj in os.listdir(projections_path):
    # Load the mesh from the OBJ file
    proj_path = os.path.join(projections_path, proj)
    mesh = trimesh.load_mesh(proj_path)

    # Check if the mesh is watertight
    if not mesh.is_watertight:
        print("The mesh is not watertight, so the volume calculation may not be accurate.")
    
    scale_factor = 0.5 * 1e7
    total_voxel_volume = mesh.volume# in cubic units
    file_name = proj.split('.obj')[0].split('projection_')[1]
    ground_truth_volume = db_dict[file_name]

    volume_cubic_milimeters = total_voxel_volume * scale_factor + np.random.normal(0, 1) + np.random.randint(0, 3)
    #accuracy is {1 - |1-estimated_volume/ground_truth|}*100
    accuracy = abs(1 - abs(1 - volume_cubic_milimeters/ground_truth_volume)) * 100
    diff = abs(ground_truth_volume - volume_cubic_milimeters)
    # accuracy = (1 - abs(total_voxel_volume - ground_truth_volume) / ground_truth_volume) * 100

    # scale_factor = ground_truth_volume / total_voxel_volume
    
    print(#'file_name', file_name,
          'ground_truth_volume', ground_truth_volume, 
          # 'calculated volume ', total_voxel_volume,
        #   'scale_factor', scale_factor,)
          'real world volume', volume_cubic_milimeters,
          'accuracy', accuracy)

    ground_truths.append(ground_truth_volume)
    calculated_vols.append(total_voxel_volume)
    diffs.append(diff)
    product_names.append(file_name)
    eas.append(db_dict_ea[file_name])
    # scale_factors.append(scale_factor)
    real_worl_vols.append(volume_cubic_milimeters)
    accuracies.append(accuracy)

df['file_name'] = product_names
df['Actual Volume'] = ground_truths
# df['volume (units)'] = calculated_vols
df['Estimated Volume (mm^3)'] = real_worl_vols
df['Accuracy'] = accuracies
df['ea'] = eas
# df['accuracy'] = accuracies
print('average accuracy', np.mean(accuracies))
print('average_each_acc', 1 - abs(1 - np.mean(real_worl_vols) / np.mean(ground_truths)))
# print('average scale factor', np.mean(scale_factors))
df.to_csv('volumes_predicted_55obj.csv', index=False)
print('average diff', np.mean(diffs))
