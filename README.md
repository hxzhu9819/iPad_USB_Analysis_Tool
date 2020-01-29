## Apple Test Log Visulation Tool

Author: Haoxuan Zhu (hxzhu@umich.edu)

Date: Jan 27, 2019

***This program is written by Haoxuan Zhu for Apple iPad System Hardware Engineering***



### Install

This section helps get your tool set up.

My program is called `datapreprocess` Configurating a new virtual environment with **Anaconda** is recommended. First, be sure that you have python, and the virtual environment is active

```shell
$ echo $VIRTUAL_ENV
```

Then, use `pip` to install `datapreprocess`

```shell
$ pip install -e .
```

Now, there's an executable that calls the `datapreprocess` package's `main()` function

```shell
$ datapreprocess
Usage: datapreprocess [OPTIONS] INPUT_DIR
Try "datapreprocess --help" for help.
```

### Use

The program currently serves two purposes: heatmap generation, and eye height & width analysis. To run the program, type

```shell
$ datapreprocess sample_logs
```

It will give

* Terminal:

  * The number of scanned files
  * The number of well-formatted files and the number of incomplete logs
  * The name of incomplete logs
  * Confidence Interval of width and height (By default the value is 95%)
  * The name of logs that contain outliers

  ```shell
  **************************************
  Scanned 61 files.
  Success: 59 Pending: 2
  **************************************
  Incomplete scans:
  fixturelog_0x18788c2240013a.txt
  fixturelog_0x1c28600a40013a.txt
  **************************************
  Width Confidence Interval: [18.51439288916334, 51.875437619311235]
  fixturelog_0x1159600a40013a.txt contains Width outlier
  fixturelog_0x1159600a40013a.txt contains Width outlier
  fixturelog_0xc188c2240013a.txt contains Width outlier
  fixturelog_0xc188c2240013a.txt contains Width outlier
  Height Confidence Interval: [7.599233939467744, 40.28212199273565]
  fixturelog_0x1159600a40013a.txt contains Height outlier
  fixturelog_0x1159600a40013a.txt contains Height outlier
  fixturelog_0xc188c2240013a.txt contains Height outlier
  fixturelog_0xc188c2240013a.txt contains Height outlier
  ```

* File:

  * `INPUT_DIR/result`
    * `[FILENAME].png`: Eyescan result heatmap view
  * `INPUT_DIR/histogram`
    * `[Height / Width]_filtered_annotated_data.png`: An annotated histogram for the filtered data (outliers are excluded) that contains percentile analysis
    * `[Height / Width]_raw_annotated_data.png`: An annotated histogram for the unprocessed data (outliers are included) that contains percentile analysis
    * `[Height / Width]_raw_data.png`: A histogram for the unprocessed data (outliers are included)
    * `[Height / Width]_filtered_data.png`: A histogram for the filtered data (outliers are excluded)

#### Heatmap Generation

```shell
$ datapreprocess sample_logs -v
```

`-v, --verbose` (optional:) Allows you to see the intermediate step info.

* The program will scan the `INPUT_DIR`, find all `*.txt`, extract `COLUMN`,`ROW` data, and generate heatmaps under `INPUT_DIR/result`
* By default, the program prevents the users from overwriting the existing files, that being said, the program can not run when the `INPUT_DIR/result` exists.
* By default for all heatmaps, the x-axis is `ROW`, y-axis is `COLUMN`

#### Histogram and Filtering Outliers

*A more user-friendly interface will be updated until the correctness of the program is examined by Apple*

```shell
$ datapreprocess sample_logs -v
```

* By default, the model assumes normal distribution
* By default, the program assumes that there are no error count inside the eye area.
* By default, the program uses 95% confidence interval. (Later, user can set the confidence percentage through terminal commands)

* Users can determine how tight the interval is by tuning the `confidence_coefficient`. By default, `confidence_coefficient=1.96`, which yields `95%`  confidence  
  * Check `http://onlinestatbook.com/2/calculators/normal_dist.html`
* There are other method's to decide the lowerbound and upperbound of the inliers
  * eg: Cook's Distance

### Assumptions

* This program only extract data without preprocessing, including outlier filer, upper/lowerbound filtering
* For better resolutions, consider modifying `dpi` in `plt.savefig`
* Each `.txt` file has its own heatmap
* All input logs have no format and syntax errors (Even though the program has a **naive** error handling section)



### Update Log

* Jan 28, 2020
  * Can plot histogram for eye widths and heights
  * Determine outliers with confidence interval

