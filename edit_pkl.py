#!/usr/bin/env python3
import numpy as np
import pickle
import glob
import os
from scipy.interpolate import interp1d

num_sims = 100
days = np.linspace(0, 250, 251)

#root_dirs = ["low", "high", "highrand", "lowrand"]
top_dirs = ["highnorm","lownorm"]

for top in top_dirs:
    print(f'beginning directory {top}',flush=True)
    for dirpath, dirnames, filenames in os.walk(top):
        pkl_files = [f for f in filenames if f.endswith(".pkl")]
        if not pkl_files:
            continue

        for file in pkl_files:
            file_path = os.path.join(dirpath, file)
            npy_name = "I_" + file.replace(".pkl", ".npy")
            npy_path = os.path.join(dirpath, npy_name)
            Is = np.zeros((num_sims, len(days)))
            with open(file_path, "rb") as pkl:
                dic = pickle.load(pkl)
                for j in range(num_sims):
                    t = np.array(dic[j]["t"])
                    i = np.array(dic[j]["i"])
                    f_interp = interp1d(t, i, kind="previous", fill_value="extrapolate")
                    Is[j, :] = f_interp(days)

            np.save(npy_path, Is)
