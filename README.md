# blkwtmonitor
Read and log the block device sector write requests from sys/block/DEV_NAME/stat to roughly measure a sdcard usage

See https://www.kernel.org/doc/Documentation/block/stat.txt for details.

# note
The sector is not the physical sector of the block device.

# usage
python blkwtmon.py mmcblk0 60

