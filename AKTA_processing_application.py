import os
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def get_file():
    for pname, dname, fname in os.walk(os.getcwd()):
        return fname

def get_csvfile(fname):
    CSV_List = []
    for file in fname:
        if file.endswith(".csv"):
            CSV_List.append(file)
    return CSV_List

def open_csvfile(csvfile):
    table = pd.read_csv(csvfile, encoding="utf-16",sep='\t',header = [0,1,2])
    n_columns = []
    for cols in table.columns:
        col_values = []
        for idx, col in enumerate(cols):
            if re.search("Unnamed", col):
                col_values.append(n_columns[-1][idx])
            else:
                col_values.append(col)
        n_columns.append(col_values)
    table.columns = pd.MultiIndex.from_tuples(n_columns)
    return table

def matplot_show_single(table):
    columns = table.columns
    for idx in range(0,len(columns),2):
        if columns[idx][2] == "ml" and columns[idx+1][2] =="mAU":
            x = table.iloc[:,idx]
            y = table.iloc[:,idx+1]
            plt.plot(x,y)
            plt.title(columns[idx][1])
            plt.xlabel('Retention volume (ml)')
            plt.ylabel(f'Absorbance {columns[idx][1].split("_")[1]} nm')
            plt.show()

def matplot_show_sub(table):
    sub_index = 1
    fig = plt.figure()
    columns = table.columns
    for idx in range(0,len(columns),2):
        if columns[idx][2] == "ml" and columns[idx+1][2] == "mAU":
            x = table.iloc[:,idx]
            y = table.iloc[:,idx+1]
            peak, _ = find_peaks(y,np.mean(y))
            ax = fig.add_subplot(2,2,sub_index)
            ax.plot(x,y)
            length = len(peak)
            for i in range(length):
                if  np.array(x)[peak[i]] > 0 and np.array(y)[peak[i]] > 0.05*max(np.array(y)):
                    ax.plot(np.array(x)[peak[i]],np.array(y)[peak[i]],"o",c = "b",label = np.array(x)[peak[i]])
                    ax.text(np.array(x)[peak[i]],np.array(y)[peak[i]], s=np.array(x)[peak[i]]) #retention plot
            ax.set_title(columns[idx][1])
            ax.set_xlabel('Retention volume (ml)')
            ax.set_ylabel(f'Absorbance {columns[idx][1].split("_")[1]} nm')
            sub_index += 1
    fig.tight_layout()
    fig.show()
      


def matplot_s(CSV_name,table):
    X = []
    Y = []
    peaks = []
    leg = []
    columns = table.columns
    for idx in range(0, len(columns), 2):
        if columns[idx][2] == "ml" and columns[idx+1][2] == "mAU":
            x = table.iloc[:,idx]
            y = table.iloc[:,idx+1]
            X.append(x)
            Y.append(y)
            peak, _ = find_peaks(y,0)
            peaks.append(peak)
            leg.append(idx)
    print(peaks)

    colors = ["r", "g", "b", "c", "m", "y", "k", "w"]
    for i in range(len(X)):
        plt.plot(X[i],Y[i],label = columns[leg[i]],c = colors[i]) #name
        plt.scatter(np.array(X[i])[peaks[i]],np.array(Y[i])[peaks[i]],marker = "o" ,c = colors[i]) #marking
    
    
    plt.title(CSV_name)
    plt.legend()
    plt.show()
    

