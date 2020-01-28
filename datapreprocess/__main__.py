"""Extract data from log file, and generate Heatmap."""
"""Written by Haoxuan Zhu (hxzhu@umich.edu). All rights reserved"""
import os
import os
import sys
import re
import click
import matplotlib
import numpy as np
import matplotlib.pyplot as plt


def mkdir(path):
    """Create a directory if not exist."""
    is_exist = os.path.exists(path)

    if not is_exist:
        os.makedirs(path)
    else:
        pass



@click.command()
@click.option('-v', '--verbose', is_flag=True, help='Print detailed info.')
@click.argument('INPUT_DIR')
def main(verbose, input_dir):
    path = input_dir
    logs = os.listdir(path)

    # This try-except block prevents the users from overwriting the existing files.
    # If you want to disable this feature, please comment the try-except blocks
    # and uncomment the following line:
    # makedirs(os.path.join(path,"result"))
    try:
        os.makedirs(os.path.join(path,"result"))
    except OSError:
        print("There exists folder. Hint: Please check whether you've removed the previous results\nTry: rm -rf " + path + "/result.")
        sys.exit(1)

    incomplete_lists = []
    cnt_good = 0
    cnt_txt = 0
    for log in logs:
        res = []
        if os.path.splitext(log)[1] != '.txt': 
            continue
        with open(os.path.join(path, log),"r") as f: 
            cnt_txt += 1
            if verbose:
                print("Eyescanning", log, end=" ")
            for line in f.readlines():
                r = re.findall('FINAL_([\S\s]*?)\n', line)
                if r :
                    res.append([int(s) for s in re.findall(r'\b\d+\b', r[0])])
            res = np.array(res)

            # Error Categorization
            if(len(res) == 0):
                if verbose:
                    print("FAIL: Eyescan {} incomplete!".format(log))
                incomplete_lists.append(log)
                continue
            if(res.shape[0] % 64 != 0):
                if not verbose: 
                    print(log,end="")
                print("FAIL: Missing COLUMN")
                continue
            if(res.shape[1] != 81):
                if not verbose: 
                    print(log,end="")
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
            if verbose:
                print("COMPLETE!")
            cnt_good += 1
    print("**************************************")
    print("Scanned",cnt_txt, "files.\nSuccess:", cnt_good, "Pending:", len(incomplete_lists))
    print("**************************************")
    print("Incomplete scans:")
    for err_file in incomplete_lists:
        print(err_file)
    print("**************************************")


if __name__ == "__main__":
    main()
