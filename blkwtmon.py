#!/usr/bin/python
import os
import time
import sys
import logging
from datetime import datetime

def read_state (blkdev) :
    cols = ('read_reqs', 'read_merges', 'read_sectors', 'read_ticks', 'write_reqs', 'write_merges', 'write_sectors', 'write_ticks') 
    statFileName = os.path.join('/sys/block', blkdev, 'stat')
    f = open(statFileName, 'r')
    stat = f.read().split()
    f.close()

    return dict(zip(cols, stat))

def read_write_requests (blkdev) :
    stat = read_state (blkdev)
    return int(stat['write_sectors'])

def time_diff_day_and_minutes (tm_start, tm_end) :
    diff = tm_end - tm_start
    minutes = diff.seconds / 60.0
    if (diff.days < 1) :
        msg = ('%.3f minutes' % minutes)
    else :
        msg = ('%d days and %.3f minutes' % (diff.days, minutes))
    return msg


if __name__ == '__main__':

    if len(sys.argv) < 3 :
        print '''
=================================================================================================================
Usage:
    python blkwtmon.py BLOCK_DEVICE_NAME INTERVAL

    BLOCK_DEVICE_NAME:  the block device name monitor on
    INTERVAL:           check interval in seconds

Example:
    python blkwtmon mmcblk0 60
    will check mmcblk0's sector write counter every minute, and same the report to /var/log/blkwtmon-mmcblk0.csv
=================================================================================================================
'''
    else :
        devname = sys.argv[1]
        interval = int(sys.argv[2])

        logname = os.path.join('/var/log', 'blkwtmon-' + devname + '.log')
        logging.basicConfig( filename = logname, format = '%(asctime)s ---- %(message)s', level = logging.INFO)

        time_start = datetime.now()
        logging.info('sector write request counter logging start')
        
        wt_at_start = read_write_requests(devname)
        wt_last_log = wt_at_start

        while(1) :
            time.sleep(interval)
            wt_sects = read_write_requests(devname)

            now = datetime.now()
            since_last = wt_sects - wt_last_log 
            since_start = wt_sects - wt_at_start

            msg = '%d in last %d seconds' % (since_last, interval) 
            msg += ' ---- %d in last %s' % (since_start, time_diff_day_and_minutes(time_start, now))

            logging.info(msg)
            print msg
            wt_last_log = wt_sects;


