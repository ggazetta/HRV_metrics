import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import signal
import os
import pandas as pd


def hrv_metrics_calc2(file_name):
    with open(file_name) as file:
            data = np.asarray(list(csv.reader(file, delimiter = ";")), dtype=np.float64)
            df = pd.DataFrame(data[:,0].T, columns=['RR'])
            print(len(df))
            change = df.pct_change()
            dfnew =  pd.concat([df, change], axis=1)
            dfnew.columns = ['RR', 'pct_change']
            df2=dfnew.loc[lambda dfnew:abs(dfnew.loc[:,"pct_change"])<=.25]
            new_rr = df2.loc[:,'RR'].to_numpy
            new_rr = list(filter(lambda x: x < 2000, new_rr())) 
            print(len(new_rr))
            peaks = nk.intervals_to_peaks(new_rr)
            hrv = nk.hrv_time(peaks, sampling_rate=1000)
            rmssd = list(hrv.HRV_RMSSD)[0]
            hrv_welch = nk.hrv_frequency(peaks, sampling_rate=1000, show=True, psd_method="welch")
            lf = list(hrv_welch.HRV_LF)[0]
            hf = list(hrv_welch.HRV_HF)[0]
            lfhf = list(hrv_welch.HRV_LFHF)[0]
    return rmssd, lf, hf, lfhf


with open("rmssd.csv", 'w+') as out:
        for filenames in os.listdir("HR/"):
            if ".txt" in filenames:
                print(filenames)
                rmssd, lf, hf, ratio = hrv_metrics_calc2("HR/"+filenames)
                out.write(f'{filenames}, {str(rmssd)}, {str(lf)}, {str(hf)}, {str(ratio)}\n')