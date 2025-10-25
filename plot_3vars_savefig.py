"""

E. Wes Bethel, Copyright (C) 2022

October 2022

Description: This code loads a .csv file and creates a 3-variable plot, and saves it to a file named "myplot.png"

Inputs: the named file "data_3vars.csv"

Outputs: displays a chart with matplotlib

Dependencies: matplotlib, pandas modules

Assumptions: developed and tested using Python version 3.8.8 on macOS 11.6

"""

import pandas as pd
import matplotlib.pyplot as plt

plot_fname = "myplot.png"

fname = "data_3vars.csv"
df = pd.read_csv(fname, comment="#")
print(df)

var_names = list(df.columns)

print("var names =", var_names)

# split the df into individual vars
# assumption: column order - 0=problem size, 1=blas time, 2=basic time

problem_sizes = df[var_names[0]].values.tolist()
code1_time = df[var_names[1]].values.tolist()
code2_time = df[var_names[2]].values.tolist()
code3_time = df[var_names[3]].values.tolist()

plt.figure()

plt.title("Comparison of 3 Codes")

xlocs = [i for i in range(len(problem_sizes))]

plt.xticks(xlocs, problem_sizes)

plt.plot(code1_time, "r-o")
plt.plot(code2_time, "b-x")
plt.plot(code3_time, "g-^")

#plt.xscale("log")
#plt.yscale("log")

plt.xlabel("Problem Sizes")
plt.ylabel("runtime")

varNames = [var_names[1], var_names[2], var_names[3]]
plt.legend(varNames, loc="best")

plt.grid(axis='both')

# save the figure before trying to show the plot
plt.savefig(plot_fname, dpi=300)


plt.show()

df["direct_mflops"] = df["Problem Size"] / (df["direct"] * 1e6)
df["vector_mflops"] = df["Problem Size"] / (df["vector"] * 1e6)
df["indirect_mflops"] = df["Problem Size"] / (df["indirect"] * 1e6)

plt.figure()
plt.title("MFLOP/s Comparison of 3 Codes")
plt.xlabel("Problem Size")
plt.ylabel("MFLOP/s")
plt.xticks(range(len(problem_sizes)), problem_sizes, rotation=45)

plt.plot(df["direct_mflops"].tolist(), "r-o", label="direct")
plt.plot(df["vector_mflops"].tolist(), "b-x", label="vector")
plt.plot(df["indirect_mflops"].tolist(), "g-^", label="indirect")

plt.legend(loc="best")
plt.grid(True)
plt.tight_layout()
plt.savefig("MFLOP.png", dpi=300)
plt.show()


PEAK_BW = 100  # GB/s, change to your system's peak
# Convert problem size to bytes (int64 = 8 bytes per element)
df["direct_bw"] = (df["Problem Size"] * 8) / df["direct"] / (PEAK_BW * 1e9) * 100
df["vector_bw"] = (df["Problem Size"] * 8) / df["vector"] / (PEAK_BW * 1e9) * 100
df["indirect_bw"] = (df["Problem Size"] * 8) / df["indirect"] / (PEAK_BW * 1e9) * 100

plt.figure()
plt.title("Memory Bandwidth Utilization of 3 Codes")
plt.xlabel("Problem Size")
plt.ylabel("% Peak Memory Bandwidth")
plt.xticks(range(len(problem_sizes)), problem_sizes, rotation=45)

plt.plot(df["direct_bw"].tolist(), "r-o", label="direct")
plt.plot(df["vector_bw"].tolist(), "b-x", label="vector")
plt.plot(df["indirect_bw"].tolist(), "g-^", label="indirect")

plt.legend(loc="best")
plt.grid(True)
plt.tight_layout()
plt.savefig("bandwidth_plot.png", dpi=300)
plt.show()
# EOF
