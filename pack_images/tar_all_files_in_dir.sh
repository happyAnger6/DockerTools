CURDIR=$(pwd)
PACKDIR=${CURDIR}/package
COPY_FLAGS="-dp --parents"
TAR_FILE="pack.tar"

source ${CURDIR}/log.sh

debug_flag=6

base_file=$1
pack_file=$2

if [ $# -ne 2 ]
then
	echo "usage:$0 <pack_base_filename> <tar_filename>!!!"
	exit 1
fi

if [ -z "$(echo $pack_file | sed -n '/\.tar$/p')" ]
then
	echo "tar_filename must be like: xxx.tar"
	exit 1
fi

TAR_FILE=$pack_file

if [ -d ${PACKDIR} ]
then
	rm -rf ${PACKDIR}
fi

if [ ! -d ${PACKDIR} ]
then
	mkdir -p ${PACKDIR}
fi

function copy_file()
{
	file=$1
	if [ -z "$file" ]
	then
		warn_log "copy a empty file!"
		return 1
	fi
	
	if [ -f ${PACKDIR}$file ]
	then
		info_log "$file already exist!"
		return 1
	fi

	if [ ! -f $file ]
	then
		err_log "source file $file not exist!"
	fi

	if [ -d $file ]
	then
		if [ ! -d ${PACKDIR}/$file ]
		then
			mkdir -p ${PACKDIR}/$file
		fi
		cp -rf $file/* ${PACKDIR}/$file
		return 0
	fi

	info_log "copy file $file"
	cp -dp --parents $file ${PACKDIR}

	link_file=`readlink $file`
	if [ -n "$link_file" ]
	then
		file_path=${file%/*}
		is_abs=`echo $link_file | grep '^/'`
		if [ -z "$is_abs" ]
		then
			link_file=${file_path}/${link_file}
			info_log "make_abs $link_file"
		fi
		copy_file $link_file
		return
	fi

	all_deps=`ldd $file`
	for dep in $all_deps
	do
		dep=${dep##*=>}
		dep=`echo $dep | sed -n 's/(.*)//p' | tr -d ' \t' `
		if [ -n "$dep" ]
		then
			copy_file $dep
		fi
	done
		
}

IFS_OLD=$IFS
IFS=$'\n'
for file in `cat $base_file`
do
	info_log "copy $file"
	copy_file $file	
done

IFS=$IFS_OLD

pushd ${PACKDIR} > /dev/null
	tar czvf ${TAR_FILE} *
	cp ${TAR_FILE} ${CURDIR}
popd

rm -rf ${PACKDIR}
