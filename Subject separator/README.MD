# SUBJECT SEPARATOR
_Terminal_ script for separating media files by their creation date and time.
## Motivation
This script may be useful in different cases. For example, I use it to separate photos made on lectures by their subjects and dates.

## Usage

Requierments:
- [Python 3](https://www.python.org)\
Interpreter for program launching.  
Any 3.x version. 
- [hachoir](https://hachoir.readthedocs.io/en/latest/)\
Used for geting files' metadata.\
Any Python 3 - compatible version.  
Installation:  
```
pip install hachoir
```

### Arguments
- `-h, --help`: shows help page end exit.
- `-V, --version`: shovs version ang exit.
- `-v, --verbose`: give more output.
- `-w, --walk`: search in subdirectorues.
- `-m, --mode`: chose mode for processing with an existing result folder.
    - `o, override`: delete existing folder (recursively), then create new;
    - `a, append`: add files to existing folder.
- `-d, --date`: specify the first date for search. Format ISO-8601 (yyyy-mm-dd). Default - 1970-01-01.
- `-t, --time`: time period for search (e.g. your lesson time). Format hh:mm-hh:mm, default - all day.
- `-T, --timedelta`: search every X days. Default - 7 (every week).
- `-r, --result`: path to result directory (absolute or relative from source folder). Default ./output
- positional argument – path to source folder. Default current work directory.

### Examples
```bash
./SubjectSeparator.py
```
Result would be: every file in directory with script, which a media file and was created at every 7 day starting from 1970-01-01 wil be moved to ./output.

```bash
python3 SubjectSeparator.py -w -d 2019-09-04 -t 13:10-14:40 -T 14 -r philosophy <Path/To/Source/Directory>
```
Result would be: all files from directory <Path/To/Source/Directory> and its subdirectories, which are mediafiles and was created at any philosophy lecture (them started 2019-09-04 and run every two weeks) will be moved to a _philosophy_ folder.