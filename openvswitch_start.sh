#!/bin/bash

CURDIR=$(pwd)
open_vswitch_dir=${CURDIR}/datapath/linux
open_vswitch_ko=openvswitch.ko

modules_dir=/lib/modules/$(uname -r)/build
nf_nat_ipv6_ko_dir=${modules_dir}/net/ipv6/netfilter
nf_nat_ipv6_ko=nf_nat_ipv6.ko
crc32_ko_dir=${modules_dir}/lib
crc32_ko=libcrc32c.ko

modprobe gre

if [ -z "$(lsmod | grep "nf_nat_ipv6")" ]
then
	pushd ${nf_nat_ipv6_ko_dir} >/dev/null
		insmod ${nf_nat_ipv6_ko}
	popd
fi

if [ -z "$(lsmod | grep "libcrc32c")" ]
then
	pushd ${crc32_ko_dir} >/dev/null
		insmod ${crc32_ko}
	popd
fi

if [ -z "$(lsmod | grep "openvswitch")" ]
then
	pushd ${open_vswitch_dir} >/dev/null
		insmod ${open_vswitch_ko}
	popd
fi

/sbin/modprobe openvswitch

if [ -z "$(ps aux | grep ovsdb-server | grep -v grep )" ]
then
	ovsdb-server /usr/local/etc/openvswitch/conf.db --remote=punix:/usr/local/var/run/openvswitch/db.sock --pidfile --detach
fi

#ovs-vsctl --no-wait init
if [ -z "$(ps aux | grep ovs-vswitchd | grep -v grep )" ]
then
	ovs-vswitchd --pidfile --detach
fi
