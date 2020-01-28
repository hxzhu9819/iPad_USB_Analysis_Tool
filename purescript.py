import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import re
import numpy as np


def mkdir(path):
    """Create a directory if not exist."""
    is_exist = os.path.exists(path)

    if not is_exist:
        os.makedirs(path)
    else:
        pass

path = "sample_logs"
logs = os.listdir(path)

try:
    mkdir(os.path.join(path,"result"))
except IsADirectoryError:
    print("There exists folder. Hint: Please check whether you've removed the previous results\nTry: rm -rf " + path + "/result.")
    sys.exit(1)

incomplete_lists = []
for log in logs:
    res = []
    if os.path.splitext(log)[1] != '.txt': 
        continue
    with open(os.path.join(path, log),"r") as f: 
        print("Eyescanning", log, end=" ")
        for line in f.readlines():
            r = re.findall('FINAL_([\S\s]*?)\n', line)
            if r :
                res.append([int(s) for s in re.findall(r'\b\d+\b', r[0])])
        res = np.array(res)

        # Error Categorization
        if(len(res) == 0):
            print("FAIL: Eyescan {} incomplete!".format(log))
            incomplete_lists.append(log)
            continue
        if(res.shape[0] % 64 != 0):
            print("FAIL: Missing COLUMN")
            continue
        if(res.shape[1] != 81):
            print("FAIL: Missing ROW")
            continue

        for i in range(0,res.shape[0],64):
            plt.xlabel("Width (step)")
            plt.ylabel("Height (step)")
            plt.subplot(121+ (i / 64))
            plt.title("CIO Lane{} Eye (74 units)".format(int(i / 64)))
            plt.imshow(res[i:i+64, :], cmap=plt.cm.hot_r)
            plt.colorbar(orientation='horizontal')
       
        plt.suptitle("Eyescan Result")
        plt.savefig(os.path.join(path,"result",log.rstrip(".txt")+".png"))
        # plt.show()
        plt.cla()
        plt.clf()
        #print("Eyescan {} complete!".format(log))
        print("COMPLETE!")

print("Incomplete scans:")
for err_file in incomplete_lists:
    print(err_file)
