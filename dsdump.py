#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import getopt
import subprocess

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('dsdump.py \n -i <inputfile> \n -o <outputfile>')
        sys.exit(2)
    
    for (opt, arg) in opts:
        if opt == '-h':
            print('dsdump.py \n -i <inputfile> \n -o <outputfile>')
            sys.exit(1)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if os.path.isfile(inputfile) and outputfile != '':
        if outputfile.endswith('/'):
            outputfile[:-1]
        if not os.path.exists(outputfile):
            os.mkdir(outputfile)
        dumpObjectiveC(inputfile, outputfile)
        dumpSwift(inputfile, outputfile)
    else:
        print('dsdump.py \n -i <inputfile> \n -o <outputfile>')
        sys.exit(2)


def dumpObjectiveC(inputfile, outputfile):
    strline = './dsdump --objc --verbose=5 "' + inputfile + '"'
    p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0].decode('utf-8', 'ignore')
    arr = out.split('\n\n\n')
    # 分割输出内容
    protocols = arr[0].split('\n')
    classes = arr[1:len(arr) - 1]
    categares = arr[-1].split('\n')
    # 输出protocols
    start = -1
    end = -1
    className = ''
    for i in range(0, len(protocols)):
        line = protocols[i]
        if '@protocol' in line:
            start = i
            className = str(line).split(' ')[1]
        if '@end' in line:
            end = i
        if start != -1 and end != -1:
            fileName = outputfile + '/' + className + '.h'
            print(fileName)
            with open(fileName, mode='w') as f:
                f.write('\n'.join(protocols[start:(end + 1)]))
                start = -1
                end = -1
    # 输出classes
    last = '\n'.join(protocols).split('@end')[-1]
    classes.append(last)
    for line in classes:
        className = line.split(' ')[1]
        fileName = outputfile + '/' + className + '.h'
        print(fileName)
        with open(fileName, mode='w') as f:
            f.write(line)
    # 输出categares
    count = len(categares)
    for i in range(0, count):
        line = categares[i]
        if line.startswith('0x00000000000'):
            continue
        else:
            if line.startswith('0x'):
                className = str(line).split(' ')[1]
                fileName = outputfile + '/' + className + '.h'
                result = line + '\n'
                for j in range(i + 1, count):
                    ll = categares[j]
                    if ll.startswith('0x'):
                        break
                    else:
                        result += ll + '\n'
                print(fileName)
                with open(fileName, mode='w') as f:
                    f.write(result)


def dumpSwift(inputfile, outputfile):
    strline = './dsdump --swift --verbose=5 "' + inputfile + '"'
    p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0].decode('utf-8', 'ignore')
    arr = out.split('\n')
    className = ''
    start = -1
    end = -1
    count = len(arr)
    for i in range(0, count):
        line = arr[i].strip()
        if line.startswith('class') or line.startswith('enum') or line.startswith('struct'):
            className = line.split(' ')[1].strip()
            fileName = outputfile + '/' + className + '.swift'
            start = i
            if line.endswith('}'):
                end = i
        elif line.endswith('}'):
            end = i
        if start != -1 and end != -1:
            print(fileName)
            with open(fileName, mode='w') as f:
                f.write('\n'.join(arr[start:end+1]))
            start = -1
            end = -1


if __name__ == "__main__":
   main(sys.argv[1:])
