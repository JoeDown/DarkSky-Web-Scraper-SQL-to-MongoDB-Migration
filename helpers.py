from sys import exit
from datetime import datetime
import time

# panic will print out the error and return with a status of 1
def panic(err, status=1):
    print(err)
    exit(status)

# walk_dict will explore a the elements of a dictionary as well as the lists
# it containts.  It is designed with jsons in mind
def walk_dict(_dict, depth=0):
    for k in _dict:
        print("%s%s : %s" % ("\t"*depth, k, type(_dict[k])))
        if type(_dict[k]) is dict:
            walk_dict(_dict[k], depth + 1)
        if type(_dict[k]) is list:
            if type(_dict[k][0]) is dict:
                walk_dict(_dict[k][0], depth + 1)
            else:
                for item in _dict[k]:
                    print("%s%s : %s" % ("\t"*(depth+1), item, type(item)))

# to_posix will take a date and a formate and return a posix time
def to_posix(date, _format):
    dt = datetime.strptime(date, _format)
    posix_dt = time.mktime(dt.timetuple())
    return int(posix_dt)
