#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import getopt
import os
import subprocess
import sys

print('''
    .         .                   
    |         |                    {Version: 2.0}
 .-.| .--. .-.| .  . .--.--. .,-. 
(   | `--.(   | |  | |  |  | |   )
 `-'`-`--' `-'`-`--`-'  '  `-|`-' 
                             |    
                             '   
''')

howToUse = 'python3 dsdump.py \n -i <inputfile> \n -o <outputfile> \n -a [ arm64 | armv7 ] \n -d'


def main(argv):
    inputfile = ''
    outputfile = ''
    arches = 'arm64'
    demangle = False
    try:
        opts, args = getopt.getopt(argv, "hi:o:a:d", ["ifile=", "ofile=", "arches=", "demangle"])
    except getopt.GetoptError:
        print('')
        sys.exit(0)

    for (opt, arg) in opts:
        if opt == '-h':
            print(howToUse)
            sys.exit(1)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-a", "--arches"):
            arches = arg
            if arches not in ['arm64', 'armv7']:
                print(howToUse)
                sys.exit(1)
        elif opt in ("-d", "--demangle"):
            demangle = True

    if os.path.isfile(inputfile) and outputfile != '':
        if outputfile.endswith('/'):
            outputfile[:-1]
        if not os.path.exists(outputfile):
            os.mkdir(outputfile)
        dumpObjectiveC(inputfile, outputfile, arches, demangle)
        dumpSwift(inputfile, outputfile, arches, demangle)
    else:
        print(howToUse)
        sys.exit(2)


def dumpObjectiveC(inputfile, outputfile, arches, demangle):
    strline = f'./dsdump -a {arches} --objc --verbose=5 "{inputfile}"'
    p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0].decode('utf-8', 'ignore')
    arr = out.split('\n\n\n')
    # 分割输出内容
    protocols = arr[0].split('\n')
    classes = arr[1:-1]
    categares = arr[-1].split('\n')
    # 输出protocols
    start = -1
    end = -1
    className = ''
    for i in range(len(protocols)):
        line = protocols[i]
        if '@protocol' in line:
            start = i
            className = str(line).split(' ')[1]
        if '@end' in line:
            end = i
        if start != -1 and end != -1:
            if demangle:
                out = swiftDemangle(className)
                if out != className:
                    className = out
            fileName = f'{outputfile}/{className}.h'
            print(fileName)
            with open(fileName, mode='a') as f:
                f.write('\n'.join(protocols[start:(end + 1)]) + '\n')
                start = -1
                end = -1
    # 输出classes
    last = '\n'.join(protocols).split('@end')[-1]
    classes.append(last)
    for line in classes:
        className = line.split(' ')[1]
        if demangle:
            out = swiftDemangle(className)
            if out != className:
                className = out
        fileName = f'{outputfile}/{className}.h'
        print(fileName)
        with open(fileName, mode='w') as f:
            f.write(line)
    # 输出categares
    count = len(categares)
    for i in range(count):
        line = categares[i]
        if line.startswith('0x00000000000'):
            continue
        if line.startswith('0x'):
            className = str(line).split(' ')[1]
            if demangle:
                out = swiftDemangle(className)
                if out != className:
                    className = out
            fileName = f'{outputfile}/{className}.h'
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


def dumpSwift(inputfile, outputfile, arches, demangle):
    strline = f'./dsdump -a {arches} --swift --verbose=5 "{inputfile}"'
    p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0].decode('utf-8', 'ignore')
    arr = out.split('\n')
    className = ''
    start = -1
    end = -1
    count = len(arr)
    for i in range(count):
        line = arr[i].strip()
        if line.startswith('class') or line.startswith('enum') or line.startswith('struct'):
            className = line.split(' ')[1].strip()
            fileName = f'{outputfile}/{className}.swift'
            start = i
            if line.endswith('}'):
                end = i
        elif line.endswith('}'):
            end = i
        if start != -1 and end != -1:
            print(fileName)
            with open(fileName, mode='a') as f:
                f.write('\n'.join(arr[start:end + 1]) + '\n')
            start = -1
            end = -1


def swiftDemangle(className):
    if className.startswith('_'):
        if '(' in className and ')' in className:
            className = className.split('(')[0]
        p = subprocess.Popen(
            f'xcrun swift-demangle --simplified --compact {className}',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out = p.communicate()[0].decode('utf-8', 'ignore').strip()
        if len(out) > 2:
            return out
    return className


if __name__ == "__main__":
    main(sys.argv[1:])
