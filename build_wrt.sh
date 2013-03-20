#!/bin/sh

if [[ "$1" == "" || "$2" == "" ]]; then
  echo "Usage: build_wrt.sh <OpenWRT Toolchain Root> <Build Version>"
  exit 1
fi

WORK="./build"
TARGET="$WORK/target"
LIB="$TARGET/usr/lib/ltsense"

rm -rf $WORK &&
mkdir -p $LIB &&

cp -r ltsense $LIB &&
mkdir -p $TARGET/{etc/ltsense,etc/ltsense/examples,etc/init.d,usr/lib/ltsense,usr/bin} &&
cp ltsense.py $LIB &&
cp contrib/ltsense.openwrt.init $TARGET/etc/init.d/ltsense &&
cp contrib/ltsense.wrapper $TARGET/usr/bin/ltsense
cp etc/*.config $TARGET/etc/ltsense/examples &&
chmod 755 $TARGET/etc/init.d/ltsense $TARGET/usr/bin/ltsense &&
mkdir -p $TARGET/CONTROL &&
cat >$TARGET/CONTROL/control <<EOF &&
Package: LtSense 
Version: $2
Architecture: all
Maintainer: Sumit Khanna <sumit@penguindreams.org>
Section: bigsense
Priority: optional
Description: LtSense
Source: http://bigsens.org
EOF

$1/host/bin/ipkg-build -o root -g root $TARGET
