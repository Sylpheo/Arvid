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
            for k in obj1.keys():
                try:
                    if (obj1[k] != obj2[k]):
                        print(indent*depth + k + ':')
                        # print('key : ' + k)
                        res = False
                        check_objects(obj1[k], obj2[k])
                except KeyError:
                    print(indent*depth + bcolors.DELETED + k + ':' + str(obj1[k]) + bcolors.ENDC)

            for k in obj2.keys():
                try:
                    obj1[k]
                except KeyError:
                    print(indent*depth + bcolors.ADDED + k + ':' + str(obj2[k]) + bcolors.ENDC)
        else:
            print(indent*depth + bcolors.SAME + "identical"+ bcolors.ENDC)
    elif isinstance(obj1, list) and isinstance(obj2, list):
        check_lists(obj1, obj2)
    else:
        print(indent*depth + bcolors.MODIFIED + str(obj1) + bcolors.ENDC + " |vs| " + bcolors.MODIFIED + str(obj2) + bcolors.ENDC)
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
                                    print(bcolors.NAME + depth*indent + i['object_name'] + ' : ' + bcolors.ENDC)
                                    check_objects(i,j)
                        except KeyError:
                            print('\'object_name\' key not found, fist file is probably not a correct conf file !')
                            break
                # si on trouve pas l'objet de l'autre côté
                if flag == False:
                    if first_time == True:
                        color = bcolors.DELETED
                    else:
                        color = bcolors.ADDED
                    print(color + depth*indent + i['object_name'] + bcolors.ENDC)



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