import pandas as pd
from pathlib import Path
import SimpleITK as sitk
from tqdm import tqdm

dir_path = "/mnt/data/Abdomen"
seg_name = "segmentation_resampled.nii.gz"
save_path = "dataframe.csv"

class_label_list = ["background", "spleen", "rightKidney", "leftKidney", "gallbladder", "esophagus", "liver", "stomach", "aorta", "inferiorVenaCava", "portalVeinAndSplenicVein", "pancreas", "rightAdrenalFland", "leftAdrenalGland"]

df = {}
df["id"] = []
df["slice"] = []
df["all"] = []
for class_label in class_label_list:
    df[class_label] = []

for x in range(30):
    path = Path(dir_path) / ("case_" + str(x).zfill(2)) / seg_name
    seg = sitk.ReadImage(str(path))
    seg_array = sitk.GetArrayFromImage(seg)

    length = seg_array.shape[0]

    with tqdm(total=length * len(class_label_list), desc="case_" + str(x).zfill(2), ncols=60) as pbar:
        for s in range(length):
            slice_array = seg_array[s, ...]
            cnt = (slice_array > -1).sum()
            df["all"].append(cnt)

            for i, class_label in enumerate(class_label_list):
                cnt = (slice_array == i).sum()
                df[class_label].append(cnt)

                pbar.update(1)

            df["id"].append(x)
            df["slice"].append(s)


df = pd.DataFrame(df)
df.to_csv(save_path)

print(df)
        

