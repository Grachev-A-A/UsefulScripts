#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import datetime
import os
import argparse
import sys
import subprocess
from shutil import get_terminal_size
try:
    import hachoir
except ImportError:
    print("\033[31mRequired \"hachoir\" module for work. Type \"pip install hachoir\" and then rerun program.\033[0m")
    sys.exit(-1)

VERSION_NUMBER="1.1"

VERSION="{0} version {1}\n\
Original name: SubjectSeparator.py\n\
Author: Alexander Grachev".format(sys.argv[0], VERSION_NUMBER)

LICENSE="This software is distibuted under GNU GPLv3 license.\n\
Visit http://www.gnu.org/licenses/gpl-3.0.txt for more information."

def createArgParser():
    parser = argparse.ArgumentParser("Subject Separator", "separates files by creating time")
    
    parser.add_argument("-V", "--version", action="version", version=VERSION)
    parser.add_argument("-l", "--license", action="version", version=LICENSE, help='show license and exit')
    parser.add_argument("-m", "--mode", choices=('o', 'override', 'a', 'append', 'r', 'remove'), default='append', 
        help='specify model of work with already existing output directory (default - append)'
    )
    parser.add_argument('-v', '--verbose', action="store_true", default=False, 
        help="give more output."
    )
    parser.add_argument('-d', '--date', default="1970-1-1",
        help="first date to be checked. Format yyyy-m-d. Default 1970-1-1"
    )
    parser.add_argument('-t', '--time', default="00:00-23:59", 
        help="time period for search (e.g. your lesson time). Format hh:mm-hh:mm, default - all day."
    )
    parser.add_argument('-w', '--walk', action='store_true', default=False, help="search in subdirectorues")
    parser.add_argument('-T', '--timedelta', type=int, default=7, 
        help="days between lessons. Default - 7 (every week), for every day input should be 1"
    )
    parser.add_argument('-r', '--result', default='./output', 
        help='path to result directory (absolute or relative from source folder). Default ./output'
    )
    parser.add_argument('path', nargs="?", default=os.path.curdir,  
        help='path to source folder. Default - current directory'
    )

    return parser


def replaceArgs(args):
    dates = str(args.date).split('-')
    try:
        args.date = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
    except:
        print("{} is not correct date. Format: yyyy-m-d".format(args.date))
        sys.exit(1)
    
    if args.date - datetime.date.today() > datetime.timedelta(0):
        print("Date {} is in future. It will not work.".format(args.date))
        sys.exit(2)

    times = str(args.time).split('-')
    if len(times) != 2 or\
        len(times[0].split(":")) != 2 or\
        len(times[1].split(":")) != 2:
        print("{} is not correct. Format <HH:MM-HH:MM>".format(args.time))
        sys.exit(1)
    else:
        times = [t.split(":") for t in times]
        try:
            tmp = []
            for t in times:
                for s in t:
                    tmp.append(int(s))
        except:
            print("{} is not correct. Format <HH:MM-HH:MM>".format(args.time))
            sys.exit(1)
        args.time = tmp
    if args.verbose:
        print("Got args: {}".format(args))
    pass

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', autosize = True):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        autosize    - Optional  : automatically resize the length of the progress bar to the terminal window (Bool)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    if autosize:
        cols, _ = get_terminal_size(fallback = (length, 1))
        length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\033[34m\r%s\033[0m' % styling.replace(fill, bar), end = '\r')


def work_on_dir(path='.'):
    if args.verbose:
        cols, _ = get_terminal_size(fallback=(100, 1))
        l = cols - len("Starting search in {}".format(os.path.join(os.path.curdir, path)))
        print("\033[32m\033[1mStarting search in {}{}\033[0m".format(os.path.join(os.path.curdir, path), " "*l))
    count = 0
    i = 1
    lst = os.listdir(path)
    for file_or_directory in lst:
        cols, _ = get_terminal_size(fallback=(100, 1))
        printProgressBar(i, len(lst), prefix="Search in {}".format(path), suffix="Checking {}".format(file_or_directory))
        if os.path.isdir(os.path.join(path, file_or_directory)) and os.path.abspath(os.path.join(path, file_or_directory)) not in ('.', '..', os.path.abspath(args.result)):
            if args.walk:
                count += work_on_dir(os.path.join(path, file_or_directory))
                printProgressBar(i, len(lst), prefix="Search in {}".format(path), suffix="Checking {}".format(file_or_directory))
        elif os.path.isfile(os.path.join(path, file_or_directory)):
            proc = subprocess.Popen(
                ["hachoir-metadata", os.path.join(path, file_or_directory), "--level", "7"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            d = datetime.datetime.combine(wdays[0] + datetime.timedelta(days=args.timedelta + 1), datetime.datetime.min.time())
            for m in proc.stdout:
                m = str(m)
                if 'Creation date' in m:
                    d = datetime.datetime.strptime(
                        m[m.index(': ')+2:-3], 
                        "%Y-%m-%d %H:%M:%S"
                    )
                    break
            proc.kill()
            if d.date() in wdays:
                if d.hour > args.time[0] and d.hour < args.time[2] or d.hour == args.time[0] and d.minute >= args.time[1] or\
                    d.hour == args.time[2] and d.minute <= args.time[3]:
                    if not os.path.exists(os.path.join(args.result, d.strftime("%Y-%m-%d"))):
                        os.mkdir(os.path.join(args.result, d.strftime("%Y-%m-%d")))
                    if os.path.exists(os.path.join(args.result, d.strftime("%Y-%m-%d"), file_or_directory)):
                        if args.mode in ('o', 'override'):
                            os.system("mv \"{}\" \"{}\"".format(os.path.join(path, file_or_directory),
                                os.path.join(args.result, d.strftime("%Y-%m-%d"))
                            ))
                        else:
                            index = 1
                            while os.path.exists(os.path.join(args.result, d.strftime("%Y-%m-%d"), "{0} ({2}){1}.".format(*file_or_directory.split('.'), index))):
                                index+=1
                            os.system("mv \"{}\" \"{}\"".format(os.path.join(path, file_or_directory),
                                os.path.join(args.result, d.strftime("%Y-%m-%d"), "{0} ({2}){1}.".format(*file_or_directory.split('.'), index))
                            ))
                    else:
                        os.system("mv \"{}\" \"{}\"".format(os.path.join(path, file_or_directory),
                            os.path.join(args.result, d.strftime("%Y-%m-%d"))
                        ))
                    count += 1
                    if args.verbose:
                        l = cols - len("Moved: {} – {}".format(os.path.join(path, file_or_directory), d.date()))
                        print("Moved: {} – {}{}".format(os.path.join(path, file_or_directory), d.date(), " "*l))
                        printProgressBar(i, len(lst), prefix="Search in {}".format(path), suffix="Checking {}".format(file_or_directory))
        i+=1
    if args.verbose:
        l=cols-len("Finished search in {}".format(os.path.join(os.path.curdir, path)))
        print("\n\033[32m\033[1mFinished search in {}{}\033[0m".format(os.path.join(os.path.curdir, path), " "*150))
    return count


if __name__=="__main__":
    # reading args
    args = createArgParser().parse_args(sys.argv[1:])
    replaceArgs(args)

    # cd
    if not os.path.isdir(args.path):
        print('Path should be a directory!')
        sys.exit(2)
    
    os.chdir(args.path)

    # mkdir if need
    if os.path.exists(args.result) and args.mode in ('r', 'remove'):
        if args.verbose:
            print("Removing old directory {}".format(args.result))
        os.system("rm -r {}".format(args.result))
    if not os.path.exists(args.result):
        if args.verbose:
            print("Creating directory for output: {}".format(args.result))
        os.mkdir(args.result)
    
    args.result = os.path.abspath(args.result)

# finding study days
wdays = [args.date]
while wdays[len(wdays)-1] + datetime.timedelta(days=args.timedelta) < datetime.date.today():
    wdays.append(wdays[len(wdays)-1] + datetime.timedelta(days=args.timedelta))
if args.verbose:
    print("Dates to check: {}".format(wdays))

# moving files:
ans = input("All files starting from \033[32m{}\033[0m in period \033[32m{}\033[0m\
    in every \033[32m{}\033[0m days will be moved from \033[32m{}\033[0m to \033[32m{}\033[0m. Continue? (y/any)\n".format(
    args.date.strftime("%Y-%m-%d"), "{}:{} - {}:{}".format(*args.time), args.timedelta, os.path.abspath(os.path.curdir),
    args.result
))
if ans == "y":
    
    count = work_on_dir()
    print("{}Work done! Total moved: {} files".format("\n" if not args.verbose else "", count))
else:
    print("Work canceled.")
    
