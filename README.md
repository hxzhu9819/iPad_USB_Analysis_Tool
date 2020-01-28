## Apple Test Log Visulation Tool

Author: Haoxuan Zhu (hxzhu@umich)

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

```shell
$ datapreprocess sample_logs -v
```

`-v, --verbose` (optional:) Allows you to see the intermediate step info.

* The program will scan the `INPUT_DIR`, find all `*.txt`, extract `COLUMN`,`ROW` data, and generate heatmaps under `INPUT_DIR/result`
* By default, the program prevents the users from overwriting the existing files, that being said, the program can not run when the `INPUT_DIR/result` exists.
* By default for all heatmaps, the x-axis is `ROW`, y-axis is `COLUMN`

### Assumptions

* This program only extract data without preprocessing, including outlier filer, upper/lowerbound filtering
* For better resolutions, consider modifying `dpi` in `plt.savefig`
* Each `.txt` file has its own heatmap
* All input logs have no format and syntax errors (Even though the program has a **naive** error handling section)

