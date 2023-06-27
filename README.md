## What is MST file?

This is specific file type with the .mst extension.
This file has text type data contents and the data is of the following syntax:

```text
BEGIN BlockName
    PropertyName = PropertyValue
    PropertyName = PropertyValue
    ...
END
```

## What is the purpose of this project?

As per the syntax described above, it can be sometimes difficult for human being to compare 2 MST files, 
where the data contents are huge.

Since, the blocks in MST file can be in any order, it is difficult to compare the files using any text comparison tool.
Thus, the purpose of this project is to compare 2 MST files and generate a report which will show the differences in the files.

## How to use this project?

There are 2 ways to use this project:
    
1. Using the [batch comparison tool](./batch_compare_mst.py).
2. Using the [single pair of MST file comparison tool](./single_compare_mst.py).

### Using the batch comparison tool

This tool can be used to compare multiple pairs of MST files.
\
But, before using this tool, you have to ensure that the input directories are in the following structure:

```text
Dir/
    File1__desktop.mst
    File1__MOW.mst
    File2__desktop.mst
    File2__MOW.mst
```
You just have to provide the path of the directory containing the MST files and the tool will generate the report in the same directory.

_**Note:**_ The `__desktop` and `__MOW` suffix after each file name is important and by that it groups the mst files.

### Using the single pair of MST file comparison tool

This tool can be used to compare a single pair of MST files.
\
You just have to provide the path of the 2 MST files and the tool will generate the report in the same directory.

```commandline
python single_compare_mst.py <path_to_file1> <path_to_file2>
```

_Optionally,_
You can also provide the path of the config json file, which may contain some config that you want to use temporarily.

```commandline
python single_compare_mst.py <path_to_file1> <path_to_file2> <path_to_config_json>
```

## _Upcoming_

- Valid configuration parameters in the config json file.
- Customization of the output file generation in user choice folder.
- GUI for the tool.
