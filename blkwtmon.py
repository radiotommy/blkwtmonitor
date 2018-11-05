#!/usr/bin/python
import os
import time
import sys
from datetime import datetime

def read_state (blkdev) :
    cols = ('read_reqs', 'read_merges', 'read_sectors', 'read_ticks', 'write_reqs', 'write_merges', 'write_sectors', 'write_ticks') 
    statFileName = os.path.join('/sys/block', blkdev, 'stat')
    f = open(statFileName, 'r')
    stat = f.read().split()
    f.close()

    return dict(zip(cols, stat))

def log_sector_writes (blkdev, logname, last_reading):
    stat = read_state(devname)
    wt_sects = int(stat['write_sectors'])
    delt = wt_sects - last_reading
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rec = '%s,%d,%d' % (date, wt_sects, delt)
    f = open(logname, 'a')
    f.write(rec + '\n')
    f.close()
    return rec, wt_sects

if __name__ == '__main__':

    if len(sys.argv) < 4 :
        print '''
===============================================================================================
Usage:
    python blkwtmon.py BLOCK_DEVICE_NAME INTERVAL LOG_NAME

    BLOCK_DEVICE_NAME:  the block device name monitor on
    INTERVAL:           check interval in seconds
    LOG_NAME:           where to save the log

Example:
    python blkwtmon mmcblk0 60 /var/log/mmc0.csv
    will record mmcblk0's sector writes per minute to /var/log/mmc0.csv
===============================================================================================
'''
    else :
        devname = sys.argv[1]
        interval = int(sys.argv[2])
        logname = sys.argv[3]

        print 'Monitor block device %s sector writing every %d seconds' % (devname, interval)
        stat = read_state(devname)
        last_reading = int(stat['write_sectors'])

        while(1) :
            time.sleep(interval)
            stat = read_state(devname)
            rec, wt_sects = log_sector_writes(devname, logname, last_reading)

            print rec
            last_reading = wt_sects

