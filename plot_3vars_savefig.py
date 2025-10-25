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

runtime_fname = "runtime.png"
MFLOP_fname = "MFLOP.png"
bandwidth_fname = "bandwidth.png"
latency_fname = "latency.png"

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

varNames = [var_names[1], var_names[2], var_names[3]]

plt.figure()

plt.title("Runtime Comparison of 3 Codes")

xlocs = [i for i in range(len(problem_sizes))]

plt.xticks(xlocs, problem_sizes)

plt.plot(code1_time, "r-o")
plt.plot(code2_time, "b-x")
plt.plot(code3_time, "g-^")

#plt.xscale("log")
#plt.yscale("log")

plt.xlabel("Problem Sizes")
plt.ylabel("runtime (seconds)")

plt.legend(varNames, loc="best")

plt.grid(axis='both')

# save the figure before trying to show the plot
plt.savefig(runtime_fname, dpi=300)

plt.show()

# MFLOPS = (problem size / 10^6) / time
code1_mflops = [((problem_sizes[i] / code1_time[i]) / 1e6) for i in range(len(problem_sizes))]
code2_mflops = [((problem_sizes[i] / code2_time[i]) / 1e6) for i in range(len(problem_sizes))]
code3_mflops = [((problem_sizes[i] / code3_time[i]) / 1e6) for i in range(len(problem_sizes))]

plt.figure()

plt.title("MFLOP/s Comparison of 3 Codes")

xlocs = [i for i in range(len(problem_sizes))]

plt.xticks(xlocs, problem_sizes)

plt.plot(code1_mflops, "r-o")
plt.plot(code2_mflops, "b-x")
plt.plot(code3_mflops, "g-^")

plt.xlabel("Problem Sizes")
plt.ylabel("MFLOP/s")

plt.legend(varNames, loc="best")  # same ordering: direct, vector, indirect

plt.grid(axis='both')

plt.savefig(MFLOP_fname, dpi=300)

peak = 448 * 1000 # converts GPU-GPU memory in TBs to GBs
# bandwidth is (8 bytes/time) / (capacity * 10^9 to convert capacity to bytes)
code1_bw = [(((problem_sizes[i] * 8) / code1_time[i]) / (1e9 / peak)) * 100 for i in range(len(problem_sizes))]
code2_bw = [(((problem_sizes[i] * 8) / code2_time[i]) / (1e9 / peak)) * 100 for i in range(len(problem_sizes))]
code3_bw = [(((problem_sizes[i] * 8) / code3_time[i]) / (1e9 / peak)) * 100 for i in range(len(problem_sizes))]

plt.figure()

plt.title("Peak Memory Bandwidth Utilization of 3 Codes")

xlocs = [i for i in range(len(problem_sizes))]

plt.xticks(xlocs, problem_sizes)

plt.plot(code1_bw, "r-o")
plt.plot(code2_bw, "b-x")
plt.plot(code3_bw, "g-^")

plt.xlabel("Problem Sizes")
plt.ylabel("% of memory bandwidth utilized")

plt.legend(varNames, loc="best")

plt.grid(axis='both')

plt.savefig(bandwidth_fname, dpi=300)

# latency = (t/N) * 10^9 convert from seconds to nano seconds for readability
code1_latency = [(code1_time[i] / problem_sizes[i]) * 1e9 for i in range(len(problem_sizes))]
code2_latency = [(code2_time[i] / problem_sizes[i]) * 1e9 for i in range(len(problem_sizes))]
code3_latency = [(code3_time[i] / problem_sizes[i]) * 1e9 for i in range(len(problem_sizes))]

plt.figure()

plt.title("Memory Latency of 3 Codes")

xlocs = [i for i in range(len(problem_sizes))]

plt.xticks(xlocs, problem_sizes)

plt.plot(code1_latency, "r-o")
plt.plot(code2_latency, "b-x")
plt.plot(code3_latency, "g-^")

plt.xlabel("Problem Sizes")
plt.ylabel("Latency (nano seconds)")

plt.legend(varNames, loc="best")

plt.grid(axis='both')

plt.savefig(latency_fname, dpi=300)

# EOF
