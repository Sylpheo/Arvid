import argparse
import json
import re


class bcolors:
    ADDED = '\033[92m'
    MODIFIED = '\033[93m'
    DELETED = '\033[91m'
    NAME = '\033[94m'
    ENDC = '\033[0m'
    SAME = '\033[96m'



def check_objects(obj1, obj2):
    res = True
    global depth
    depth += 1
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        if obj1 != obj2:
            res = False
            for k in obj1.keys():
                try:
                    if (obj1[k] != obj2[k]):
                        print(indent*depth + k + ':')
                        # print('key : ' + k)
                        check_objects(obj1[k], obj2[k])
                except KeyError:
                    if args.o == False:
                        color = bcolors.DELETED
                        color_end = bcolors.ENDC
                    else:
                        color = 'DELETED : '
                        color_end = ''
                    print(indent*depth + color + k + ':' + str(obj1[k]) + color_end)

            for k in obj2.keys():
                try:
                    obj1[k]
                except KeyError:
                    if args.o == False:
                        color = bcolors.ADDED
                        color_end = bcolors.ENDC
                    else:
                        color = 'ADDED : '
                        color_end = ''
                    print(indent*depth + color + k + ':' + str(obj2[k]) + color_end)
        elif depth > 1: #pourrrriiiiiiiiiiiiiiiiii
            if args.o == False:
                color = bcolors.SAME
                color_end = bcolors.ENDC
            else:
                color = ''
                color_end = ''
            print(indent*depth + color + "identical"+ color_end)
    elif isinstance(obj1, list) and isinstance(obj2, list):
        check_lists(obj1, obj2)
    else:
        if args.o == False:
            color = bcolors.MODIFIED
            color_end = bcolors.ENDC
        else:
            color = ''
            color_end = ''
        print(indent*depth + color + str(obj1) + color_end + " |vs| " + color + str(obj2) + color_end)
    depth -= 1
    return res

def check_lists(list1, list2):

    iterate(list1, list2, True)
    iterate(list2, list1, False)

def iterate(list1, list2, first_time):
        for i in list1:
            flag = False
            if isinstance(i,dict):
                for j in list2:
                    if isinstance(j,dict):
                        try:
                            if i['object_name'] == j['object_name']:
                                flag = True
                                if first_time == True:
                                    if args.o == False:
                                        color = bcolors.NAME
                                        color_end = bcolors.ENDC
                                    else:
                                        color = ''
                                        color_end = ''
                                    print(color + depth*indent + i['object_name'] + ' : ' + color_end)
                                    check_objects(i,j)
                        except KeyError:
                            print('\'object_name\' key not found, fist file is probably not a correct conf file !')
                            break
                # si on trouve pas l'objet de l'autre côté
                if flag == False:
                    if args.o == False:
                        if first_time == True:
                            color = bcolors.DELETED
                        else:
                            color = bcolors.ADDED
                        color_end = bcolors.ENDC
                    else:
                        color = 'ADDED : '
                        color_end = ''
                    print(color + depth*indent + i['object_name'] + color_end)



parser = argparse.ArgumentParser(description='Compare two conf files')
parser.add_argument('files', metavar='file.json', nargs=2, help='a file to compare')
parser.add_argument('-o', nargs='?', const=True, default=False, help='use it if you redirect the output to a file')
args = parser.parse_args()
file1_name = args.files[0]
file2_name = args.files[1]
with open(file1_name) as f:
 file1 = json.load(f)
with open(file2_name) as f:
 file2 = json.load(f)

depth = -1
indent = ' '
is_identical = check_objects(file1,file2)
if is_identical:
    print('The files are identical !')