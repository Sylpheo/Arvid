import argparse
import json
import re


class bcolors:
    ADDED = '\033[92m'
    MODIFIED = '\033[93m'
    DELETED = '\033[91m'
    ENDC = '\033[0m'



def check_objects(obj1, obj2):
    res = True
    global depth
    depth += 1
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        if len(list(obj1.keys())) >= len(list(obj2.keys())):
            left_obj = obj1
            right_obj = obj2
        else:
            left_obj = obj2
            right_obj = obj1
        for k in left_obj.keys():
            try:
                if (left_obj[k] != right_obj[k]):
                    print(indent*depth+k+':')
                    # print('key : ' + k)
                    res = False
                    check_objects(obj1[k], obj2[k])
            except KeyError:
                if left_obj == obj1:
                        color = bcolors.DELETED
                elif left_obj == obj2:
                        color = bcolors.ADDED
                print(indent*depth+color +  k + '/'+str(left_obj[k]) + bcolors.ENDC)
    elif isinstance(obj1, list) and isinstance(obj2, list):
        check_lists(obj1, obj2)
    else:
        print(indent*depth+bcolors.MODIFIED + str(obj1) +bcolors.ENDC+ " |vs| " + bcolors.MODIFIED+str(obj2)+ bcolors.ENDC)
    depth -= 1
    return res

def check_lists(list1, list2):
    for i in list1:
        for j in list2:
            if (isinstance(i, dict)) and isinstance(j,dict):
                try:
                    if i['object_name'] == j['object_name']:
                        check_objects(i,j)
                except KeyError:
                    print('\'object_name\' key not found, this is probably not a correct conf file !')
                    break






parser = argparse.ArgumentParser(description='Compare two conf files')
parser.add_argument('files', metavar='file.json', nargs=2, help='a file to compare')
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