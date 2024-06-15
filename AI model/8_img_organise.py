import dicom2nifti
import nibabel as nib
import nilearn as nil
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil

import gc


f = "0.0"

folder = 'E:/Faheem/oasis-scripts-master/data/organised_mr/'+f

destination = "C:/Users/mohdf/OneDrive/Desktop/oasis/data/organised_mr/"+f
# destination = "M:/Faheem/oasis-scripts-master/data/images_mr/"+f




for foldername in os.listdir(folder):
    # print(foldername)
    for inner_folder in os.listdir(folder+"/"+foldername):
        path = folder+"/"+foldername+"/"+inner_folder
        filename = os.listdir(folder+"/"+foldername+"/"+inner_folder)[1]

        dicom2nifti.convert_directory(path+"/DICOM", 'data', compression=True, reorient=True)
        brain_vol = nib.load(path+"/"+filename)
        brain_vol_data = brain_vol.get_fdata()

        # for storing images
        n_slice = brain_vol_data.shape[2]
        
        print(foldername+"_"+inner_folder+" ==> "+str(n_slice))
        # for 2.0 and 3.0 step_size = 1
        # for 1.0 step_size = n_slice // 130
        # for 0.5 step_size = n_slice // 60
        # for 0.0 step_size = n_slice // 30
        if f == "2.0" or f == "3.0":
            step_size = 1
        elif f == "1.0":
            step_size = n_slice // 130
        elif f == "0.5":
            step_size = n_slice // 60
        else:
            step_size = n_slice // 30
        
        if step_size < 1:
            step_size = 1
        plot_range = n_slice
        start_stop = 0
        
        
        for idx, img in enumerate(range(start_stop, plot_range, step_size)):
            plt.figure(figsize=[1, 1],dpi=900)
            plt.imshow(ndi.rotate(brain_vol_data[:, :, img], 90), cmap='gray')
            plt.axis('off')
            
            img_filename = os.path.join(destination, f'{foldername}_{inner_folder}_{idx + 1}.jpg')
            plt.savefig(img_filename, bbox_inches='tight', pad_inches=0)
            plt.close()  # Close the individual subplot figure
        del brain_vol_data, brain_vol  # Free memory
        gc.collect()  # Force garbage collection
    print()



"""
for foldername in os.listdir(folder):
    f = foldername.split("_")[0][3:]
    # print(f)
    if int(f) < 30649:
        continue
    else:
        # print(foldername)
        # print(f)
        for inner_folder in os.listdir(folder+"/"+foldername):
            path = folder+"/"+foldername+"/"+inner_folder
            filename = os.listdir(folder+"/"+foldername+"/"+inner_folder)[1]

            dicom2nifti.convert_directory(path+"/DICOM", 'data', compression=True, reorient=True)
            brain_vol = nib.load(path+"/"+filename)
            brain_vol_data = brain_vol.get_fdata()

            # for storing images
            n_slice = brain_vol_data.shape[2]
            
            print(foldername+"_"+inner_folder+" ==> "+str(n_slice))
            # for 2.0 and 3.0 step_size = 1
            # for 1.0 step_size = n_slice // 130
            # for 0.5 step_size = n_slice // 60
            # for 0.0 step_size = n_slice // 30
            if f == "2.0" or f == "3.0":
                step_size = 1
            elif f == "1.0":
                step_size = n_slice // 130
            elif f == "0.5":
                step_size = n_slice // 60
            else:
                step_size = n_slice // 30
            
            if step_size < 1:
                step_size = 1
            plot_range = n_slice
            start_stop = 0
            
            
            for idx, img in enumerate(range(start_stop, plot_range, step_size)):
                plt.figure(figsize=[1, 1],dpi=900)
                plt.imshow(ndi.rotate(brain_vol_data[:, :, img], 90), cmap='gray')
                plt.axis('off')
                
                img_filename = os.path.join(destination, f'{foldername}_{inner_folder}_{idx + 1}.jpg')
                plt.savefig(img_filename, bbox_inches='tight', pad_inches=0)
                plt.close()  # Close the individual subplot figure
            del brain_vol_data, brain_vol  # Free memory
            gc.collect()  # Force garbage collection
        print()

"""
print("complete")