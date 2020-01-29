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
from matplotlib.patches import Rectangle


# Hyper-parameter
confidence_coefficient = 1.96 # 1.96-> 95%; 3 -> 99.75%

def mkdir(path):
    """Create a directory if not exist."""
    is_exist = os.path.exists(path)

    if not is_exist:
        os.makedirs(path)
    else:
        pass


def get_eye_size(N):
    M = N.copy()
    M[M != 0] = 1
    height = M.shape[0] - np.min(np.sum(M, axis=0, keepdims=True))
    width = M.shape[1] - np.min(np.sum(M, axis=1, keepdims=True))
    return width, height, np.argmin(np.sum(M, axis=1, keepdims=True)), np.argmin(np.sum(M, axis=0, keepdims=True))


def analyze_distribution(data, name, log_name_for_wh, path):
    mean = np.mean(data)
    std = np.std(data)
    lowerbound = mean - confidence_coefficient * std
    upperbound = mean + confidence_coefficient * std
    print("{} Confidence Interval: [{}, {}]".format(name, lowerbound, upperbound))

    # Find outliers based on the confidence interval
    outlier_log_index = [i for i in range(len(data)) if (data[i] < lowerbound or data[i] > upperbound)]
    for i in outlier_log_index:
        print(log_name_for_wh[i] + " contains " + name + " outlier")
    generate_histogram(data, os.path.join(path,"histogram"), name, False)

    # Filter outliers
    filtered_data = [data[i] for i in range(len(data)) if (data[i] >= lowerbound and data[i] <= upperbound)]
    generate_histogram(filtered_data, os.path.join(path,"histogram"), name, True)


def generate_histogram(w, out_path, xlabel, filtered=False):
    plt.cla()
    plt.clf()

    plt.title('Distribution of eye ' + xlabel, fontsize=20)
    plt.ylabel('Count', fontsize=15)
    plt.xlabel(xlabel, fontsize=15)
    plt.hist(w, bins='auto')

    if filtered:
        filename = xlabel + "_filtered_raw_data.png"
    else:
        filename = xlabel + "_raw_Data.png"
    plt.savefig(os.path.join(out_path,filename))

    # Colours for different percentiles
    perc_25_colour = 'gold'
    perc_50_colour = 'mediumaquamarine'
    perc_75_colour = 'deepskyblue'
    perc_95_colour = 'peachpuff'

    fig, ax = plt.subplots(figsize=(8,8))
    counts, bins, patches = ax.hist(w, facecolor=perc_50_colour, edgecolor='gray', bins='auto')
    ax.set_xticks(bins.round(3))
    plt.xticks(rotation=70)
    plt.title('Distribution of eye ' + xlabel, fontsize=20)
    plt.ylabel('Count', fontsize=15)
    plt.xlabel(xlabel, fontsize=15)
    twentyfifth, seventyfifth, ninetyfifth = np.percentile(w, [25, 75, 95])
    for patch, leftside, rightside in zip(patches, bins[:-1], bins[1:]):
        if rightside < twentyfifth:
            patch.set_facecolor(perc_25_colour)
        elif leftside > ninetyfifth:
            patch.set_facecolor(perc_95_colour)
        elif leftside > seventyfifth:
            patch.set_facecolor(perc_75_colour)
    bin_x_centers = 0.5 * np.diff(bins) + bins[:-1]
    bin_y_centers = ax.get_yticks()[1] * 0.25
    for i in range(len(bins)-1):
        bin_label = "{0:,}".format(counts[i]) + "  ({0:,.2f}%)".format((counts[i]/counts.sum())*100)
        plt.text(bin_x_centers[i], bin_y_centers, bin_label, rotation=90, rotation_mode='anchor')

    # Annotation for bar values
    ax.annotate('Each bar shows count and percentage of total',
            xy=(.85,.30), xycoords='figure fraction',
            horizontalalignment='center', verticalalignment='bottom',
            fontsize=10, bbox=dict(boxstyle="round", fc="white"),
            rotation=-90)

    #create legend
    handles = [Rectangle((0,0),1,1,color=c,ec="k") for c in [perc_25_colour, perc_50_colour, perc_75_colour, perc_95_colour]]
    labels= ["0-25 Percentile","25-50 Percentile", "50-75 Percentile", ">95 Percentile"]
    plt.legend(handles, labels, bbox_to_anchor=(0.5, 0., 0.6, 0.99))

    if filtered:
        filename = xlabel + "_filtered_analyzed_data.png"
    else:
        filename = xlabel + "_analyzed_Data.png"
    plt.savefig(os.path.join(out_path,filename))


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='Print detailed info.')
@click.argument('INPUT_DIR')
def main(verbose, input_dir):
    path = input_dir
    logs = os.listdir(path)

    # This try-except block prevents the users from overwriting the existing files.
    # If you want to disable this feature, please comment the try-except blocks
    # and uncomment the following line:
    mkdir(os.path.join(path,"result"))
    mkdir(os.path.join(path,"histogram"))
    # try:
    #     os.makedirs(os.path.join(path,"result"))
    #     os.makedirs(os.path.join(path,"histogram"))
    # except OSError:
    #     print("There exists folder. Hint: Please check whether you've removed the previous results\nTry: rm -rf " + path + "/result\nrm -rf " + path + "/histogram")
    #     sys.exit(1)

    incomplete_lists = []
    cnt_good = 0
    cnt_txt = 0
    widths = []
    heights = []
    log_name_for_wh = []

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
                    print(log,end=" ")
                print("FAIL: Missing COLUMN")
                continue
            if(res.shape[1] != 81):
                if not verbose: 
                    print(log,end=" ")
                print("FAIL: Missing ROW")
                continue
            
            # Remove the Row index from res
            res = res[:,1:]
            
            for i in range(0,res.shape[0],64):

                w, h, w_line, h_line = get_eye_size(res[i:i+64, :])
                widths.append(w)
                heights.append(h)
                log_name_for_wh.append(log)


                # plot heatmaps
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


    # result report
    print("**************************************")
    print("Scanned",cnt_txt, "files.\nSuccess:", cnt_good, "Pending:", len(incomplete_lists))
    print("**************************************")
    print("Incomplete scans:")
    for err_file in incomplete_lists:
        print(err_file)
    print("**************************************")

    # histogram and confidence interval analysis
    analyze_distribution(widths, "Width", log_name_for_wh, path)
    analyze_distribution(heights, "Height", log_name_for_wh, path)


if __name__ == "__main__":
    main()
