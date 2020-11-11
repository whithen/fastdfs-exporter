#!/bin/bash
SERVICE=$SERVICE

STORAGE_BASE_PATH="/data/storage"
STORAGE_LOG_FILE="$STORAGE_BASE_PATH/logs/storaged.log"
STORAGE_CONF_FILE="/etc/fdfs/storage.conf"

TRACKER_BASE_PATH="/data/tracker"
TRACKER_LOG_FILE="$TRACKER_BASE_PATH/logs/trackerd.log"
TRACKER_CONF_FILE="/etc/fdfs/tracker.conf"

tracker()
{
    if [ ! -d ${TRACKER_BASE_PATH} ]
    then
        mkdir -p ${TRACKER_BASE_PATH}
    fi
    echo "start fdfs_trackerd..."
    fdfs_trackerd ${TRACKER_CONF_FILE}
    tail -f "$TRACKER_LOG_FILE"
}

storage()
{
    if [ ! -d ${STORAGE_BASE_PATH} ]
    then
        mkdir -p ${STORAGE_BASE_PATH}
    fi
    echo "start fdfs_storgaed..."
    echo TRACKER_SERVER=$TRACKER
    echo GROUP_LIST=${GROUP_LIST}
    echo GROUP_NAME=${GROUP_NAME}
    if [ ! "$TRACKER" = "" ]
    then
        sed -i "s/^.*tracker_server.*=.*$/#tracker_server/" /etc/fdfs/storage.conf
        sed -i "s/^.*tracker_server.*=.*$/#tracker_server/" /etc/fdfs/mod_fastdfs.conf
        tnum=`echo ${TRACKER} |grep ';' |wc -l`
        echo TRACKER num = `expr $tnum + 1`
        for((i=1;i<=$tnum+1;i++))
        do
            tip=`echo ${TRACKER} |cut -d ';' -f $i`
            echo TRACKER $i = $tip
            ping $tip -c 3
            sed -i "/#tracker_server/a\tracker_server=$tip:22122" /etc/fdfs/storage.conf
            sed -i "/#tracker_server/a\tracker_server=$tip:22122" /etc/fdfs/mod_fastdfs.conf
        done
        sed -i "s:^group_name.*=.*:group_name=$GROUP_NAME:g" /etc/fdfs/storage.conf
        sed -i "s:^group_name.*=.*:group_name=$GROUP_NAME:g" /etc/fdfs/mod_fastdfs.conf
        gnum=`echo ${GROUP_LIST} |grep ';' |wc -l`
        echo GROUP_LIST num = `expr $gnum + 1`
        sed -i "s:^group_count.*:group_count=`expr $gnum + 1`:g" /etc/fdfs/mod_fastdfs.conf
        for((i=1;i<=$gnum+1;i++))
        do
            gname=`echo ${GROUP_LIST} |cut -d ';' -f $i`
            echo GROUP_LIST $i = $gname
            echo "[$gname]
group_name=$gname
storage_server_port=23000
store_path_count=1
store_path0=/data/storage
" >> /etc/fdfs/mod_fastdfs.conf
        done
    fi
    fdfs_storaged "$STORAGE_CONF_FILE"
    /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
    sleep 5
    tail -f "$STORAGE_LOG_FILE"
}

case $SERVICE in
    "tracker")
        tracker
    ;;
    "storage")
        storage
    ;;
esac
