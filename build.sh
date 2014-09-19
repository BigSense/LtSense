#!/bin/sh

if [[ "$1" == "" || "$2" == "" ]]; then
  echo "Usage: build_wrt.sh [openwrt|debian] <Build Version>"
  exit 1
fi

openwrt_files() {
    mkdir -p $TARGET/etc/init.d &&
    cp package/openwrt/ltsense.openwrt.init $TARGET/etc/init.d/ltsense &&
    chmod 755 $TARGET/etc/init.d/ltsense $TARGET/usr/bin/ltsense
}

debian_files() {
    mkdir -p $TARGET/etc/{init,default} &&
    cp package/debian-ubuntu/upstart $TARGET/etc/init/ltsense.conf &&
    cp package/debian-ubuntu/etc-default $TARGET/etc/default/ltsense
}

case "$1" in
  openwrt)
    PKDIR=CONTROL
  ;;
  debian)
    PKDIR=DEBIAN
  ;;
  *)
    echo Invalid Package Type: $1
    exit 1
  ;;
esac

WORK="./build"
TARGET="$WORK/target"
LIB="$TARGET/usr/lib/ltsense"

rm -rf $WORK &&
mkdir -p $LIB &&

cp -r ltsense $LIB &&
mkdir -p $TARGET/{etc/ltsense,etc/ltsense/examples,usr/lib/ltsense,usr/bin} &&
cp ltsense.py $LIB &&
cp package/ltsense.wrapper $TARGET/usr/bin/ltsense &&
cp etc/*.config $TARGET/etc/ltsense/examples &&
mkdir -p $TARGET/$PKDIR &&
cat >$TARGET/$PKDIR/control <<EOF &&
Package: ltsense 
Version: $2
Architecture: all
Maintainer: Sumit Khanna <sumit@penguindreams.org>
Section: bigsense
Priority: optional
Description: LtSense
Source: http://bigsens.io
Depends: python-configobj
EOF

case "$1" in
  openwrt)
    openwrt_files
    ipkg-build -o root -g root $TARGET
    ;;
  debian)
    debian_files
    dpkg -b $TARGET ltsense-"$2"_all.deb
    ;;
esac
