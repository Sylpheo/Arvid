# -*- coding: utf-8 -*-

"""
    Implementation of the comparison between two conf files.

    Usage:

    arvid file1.json file2.json
"""

import argparse
import json
import re
import sys

__all__ = ['main']
class bcolors:
    """
        Class for the different color used in this program
    """
    ADDED = '\033[92m'
    MODIFIED = '\033[93m'
    DELETED = '\033[91m'
    NAME = '\033[94m'
    ENDC = '\033[0m'
    SAME = '\033[96m'



def check_objects(obj1, obj2):
    """
        Main fonction, check the differences between two objects. Return True if the objects are identical
    """
    res = True
    global depth
    depth += 1
    if args.o == False:
        color_end = bcolors.ENDC
    else:
        color_end = ''
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        if obj1 != obj2:
            res = False
            for k in obj1.keys(): # we check all the keys in obj1
                try:
                    if (obj1[k] != obj2[k]):
                        print(indent*depth + k + ':') # writing the level of the object where things are different
                        check_objects(obj1[k], obj2[k])
                except KeyError: # if we don't find the key in obj2, we print it as deleted
                    if args.o == False:
                        color = bcolors.DELETED
                    else:
                        color = 'DELETED : '
                    print(indent*depth + color + k + ': ' + str(obj1[k]) + color_end) # we print with the indentation !

            for k in obj2.keys(): # then we check all the keys in obj2
                try:
                    obj1[k]
                except KeyError: # if we don't find the key in obj1, we print it as added
                    if args.o == False:
                        color = bcolors.ADDED
                    else:
                        color = 'ADDED : '
                    print(indent*depth + color + k + ': ' + str(obj2[k]) + color_end)

        elif depth > 1:
            if args.o == False:
                color = bcolors.SAME
            else:
                color = ''
            print(indent*depth + color + "identical"+ color_end)

    elif isinstance(obj1, list) and isinstance(obj2, list):
        check_lists(obj1, obj2)
    else: # if the items are different but are neither objects nor lists, we print them as modified
        if args.o == False:
            color = bcolors.MODIFIED
        else:
            color = ''
        print(indent*depth + color + str(obj1) + color_end + " |vs| " + color + str(obj2) + color_end)
    depth -= 1
    return res

def check_lists(list1, list2):
    """
        A fonction to compare two lists, using two iteration
    """

    iterate(list1, list2, True)
    iterate(list2, list1, False)

def iterate(list1, list2, first_time):
    """
        A fonction to iterate through a list and comparing it with the other
    """

    if args.o == False:
        color_end = bcolors.ENDC
    else:
        color_end = ''

    for i in list1:
        flag = False
        if isinstance(i,dict):
            for j in list2:
                if isinstance(j,dict):
                    try:
                        # if we find the key in the two lists, we check the item they contain
                        if i['object_name'] == j['object_name']:
                            flag = True
                            # we only print the name of the object if we check it for the first time
                            if first_time == True:
                                if args.o == False:
                                    color = bcolors.NAME
                                else:
                                    color = ''
                                print(color + depth*indent + i['object_name'] + ' : ' + color_end)
                                check_objects(i,j)
                    except KeyError:
                        print('\'object_name\' key not found, fist file is probably not a correct conf file !')
                        break

            # if we don't find the object on the other side, we print it as deleted or added depending on which way we are comparing
            if flag == False:
                if args.o == False:
                    if first_time == True:
                        color = bcolors.DELETED
                    else:
                        color = bcolors.ADDED
                else:
                    color = 'ADDED : '
                print(color + depth*indent + i['object_name'] + color_end)


def main():
    """
        Entry point of the programme. Check the arguments
    """

    # using argparse to parse the arguments
    parser = argparse.ArgumentParser(description='Compare two conf files')
    parser.add_argument('files', metavar='file.json', nargs=2, help='a file to compare')

    # argument needed to write properly in a text file
    parser.add_argument('-o', nargs='?', const=True, default=False, help='use it if you redirect the output to a file')
    global args
    args = parser.parse_args()
    file1_name = args.files[0]
    file2_name = args.files[1]
    with open(file1_name) as f:
        try:
            file1 = json.load(f)
        except json.decoder.JSONDecodeError:
            print('First file is not a proper json file')
            sys.exit(0)

    with open(file2_name) as f:
        try:
            file2 = json.load(f)
        except json.decoder.JSONDecodeError:
            print('Second file is not a proper json file')
            sys.exit(0)



    global depth
    depth = -1 # used to count the indentation depth
    global indent
    indent = ' ' # identation symbol

    print("\n** ARVID ** \n")
    print("Everything is relative to the first file !\n")
    if args.o == False:
        print("In "+bcolors.ADDED+"green"+bcolors.ENDC+" : what is added")
        print("In "+bcolors.DELETED+"red"+bcolors.ENDC+" : what is removed")
        print("In "+bcolors.MODIFIED+"yellow"+bcolors.ENDC+" : what is modified")
        print("In "+bcolors.NAME+"blue"+bcolors.ENDC+" : name of the objects\n")

    is_identical = check_objects(file1,file2)
    if is_identical:
        print('The files are identical !')

if __name__ == '__main__':
    main()