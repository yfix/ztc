#!/bin/sh
#
# Script for making Linux_disk_xxx templates from Linux_disk_sda
#
# Copyright (c) 2011 Wrike, Inc.

set -e

TEMPLATE_FLDR=~/workspace/ztc/templates/
NEW_DISK=$1

[ "x$NEW_DISK" == "x" ] && ( echo "new device name not specified" && exit 1 )

cp $TEMPLATE_FLDR/Template_Linux_disk_sda.xml $TEMPLATE_FLDR/Template_Linux_disk_$NEW_DISK.xml
sed -ie s/sda/$NEW_DISK/ $TEMPLATE_FLDR/Template_Linux_disk_$NEW_DISK.xml
sed -ie s/sda/$NEW_DISK/ $TEMPLATE_FLDR/Template_Linux_disk_$NEW_DISK.xml
sed -ie s/sda/$NEW_DISK/ $TEMPLATE_FLDR/Template_Linux_disk_$NEW_DISK.xml
sed -ie s/sda/$NEW_DISK/ $TEMPLATE_FLDR/Template_Linux_disk_$NEW_DISK.xml

rm $TEMPLATE_FLDR/Template_Linux_disk_$NEW_DISK.xmle

echo "done"
exit 0
