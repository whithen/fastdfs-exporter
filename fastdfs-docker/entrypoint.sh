#!/bin/bash
SERVICE=${SERVICE}

STORAGE_BASE_PATH="/data/storage"
STORAGE_LOG_FILE="${STORAGE_BASE_PATH}/logs/storaged.log"
STORAGE_CONF_FILE="/etc/fdfs/storage.conf"

TRACKER_BASE_PATH="/data/tracker"
TRACKER_LOG_FILE="${TRACKER_BASE_PATH}/logs/trackerd.log"
TRACKER_CONF_FILE="/etc/fdfs/tracker.conf"

tracker()
{
    if [ ! -d ${TRACKER_BASE_PATH} ]
    then
        mkdir -p ${TRACKER_BASE_PATH}
    fi
    if [ ! -z ${connect_timeout} ];then
        sed -i "s:^connect_timeout.*=.*:connect_timeout=${connect_timeout}:g" /etc/fdfs/tracker.conf
    else
        sed -i "s:^connect_timeout.*=.*:connect_timeout=30:g" /etc/fdfs/tracker.conf
    fi
    if [ ! -z ${network_timeout} ];then
        sed -i "s:^network_timeout.*=.*:network_timeout=${network_timeout}:g" /etc/fdfs/tracker.conf
    else
        sed -i "s:^network_timeout.*=.*:network_timeout=60:g" /etc/fdfs/tracker.conf
    fi
    if [ ! -z ${max_connections} ];then
        sed -i "s:^max_connections.*=.*:max_connections=${max_connections}:g" /etc/fdfs/tracker.conf
    else
        sed -i "s:^max_connections.*=.*:max_connections=10240:g" /etc/fdfs/tracker.conf
    fi
    if [ ! -z ${store_lookup} ];then
        sed -i "s:^store_lookup.*=.*:store_lookup=${store_lookup}:g" /etc/fdfs/tracker.conf
    else
        sed -i "s:^store_lookup.*=.*:store_lookup=2:g" /etc/fdfs/tracker.conf
    fi
    if [ ! -z ${reserved_storage_space} ];then
        sed -i "s:^reserved_storage_space.*=.*:reserved_storage_space=${reserved_storage_space}%:g" /etc/fdfs/tracker.conf
    else
        sed -i "s:^reserved_storage_space.*=.*:reserved_storage_space=10%:g" /etc/fdfs/tracker.conf
    fi
    if [ ! -z ${log_file_keep_days} ];then
        sed -i "s:^log_file_keep_days.*=.*:log_file_keep_days=${log_file_keep_days}:g" /etc/fdfs/tracker.conf
    else
        sed -i "s:^log_file_keep_days.*=.*:log_file_keep_days=7:g" /etc/fdfs/tracker.conf
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
    echo TRACKER_LIST=${TRACKER_LIST}
    echo GROUP_LIST=${GROUP_LIST}
    echo GROUP_NAME=${GROUP_NAME}
    if [ ! -z ${TRACKER_LIST} ]
    then
        sed -i "s/^.*tracker_server.*=.*$/#tracker_server/" /etc/fdfs/storage.conf
        storage_line=$(sed -n '/^#tracker_server/=' /etc/fdfs/storage.conf |sed -n 1p)
        sed -i "s/^.*tracker_server.*=.*$/#tracker_server/" /etc/fdfs/mod_fastdfs.conf
        mod_fastdfs_line=$(sed -n '/^#tracker_server/=' /etc/fdfs/mod_fastdfs.conf |sed -n 1p)
        TRACKER_LIST=($(echo ${TRACKER_LIST} | tr ';' ' '))
        for tracker in ${TRACKER_LIST[@]}
        do
            echo ${tracker}
            ping ${tracker} -c 2
            sed -i "${storage_line}a\tracker_server=${tracker}:22122" /etc/fdfs/storage.conf
            sed -i "${mod_fastdfs_line}a\tracker_server=${tracker}:22122" /etc/fdfs/mod_fastdfs.conf
            # sed -i "/#tracker_server/a\tracker_server=${tracker}:22122" /etc/fdfs/storage.conf
            # sed -i "/#tracker_server/a\tracker_server=${tracker}:22122" /etc/fdfs/mod_fastdfs.conf
        done
        sed -i "s:^group_name.*=.*:group_name=${GROUP_NAME}:g" /etc/fdfs/storage.conf
        if [ ! -z ${connect_timeout} ];then
            sed -i "s:^connect_timeout.*=.*:connect_timeout=${connect_timeout}:g" /etc/fdfs/mod_fastdfs.conf
        else
            sed -i "s:^connect_timeout.*=.*:connect_timeout=30:g" /etc/fdfs/mod_fastdfs.conf
        fi
        if [ ! -z ${network_timeout} ];then
            sed -i "s:^network_timeout.*=.*:network_timeout=${network_timeout}:g" /etc/fdfs/mod_fastdfs.conf
        else
            sed -i "s:^network_timeout.*=.*:network_timeout=60:g" /etc/fdfs/mod_fastdfs.conf
        fi
        sed -i "s:^group_name.*=.*:group_name=${GROUP_NAME}:g" /etc/fdfs/mod_fastdfs.conf
        GROUP_LIST=($(echo ${GROUP_LIST} | tr ';' ' '))
        sed -i "s:^group_count.*:group_count=${#GROUP_LIST[@]}:g" /etc/fdfs/mod_fastdfs.conf
        for gname in ${GROUP_LIST[@]}
        do
            echo ${gname}
            echo "[${gname}]
group_name=${gname}
storage_server_port=23000
store_path_count=1
store_path0=/data/storage
" >> /etc/fdfs/mod_fastdfs.conf
        done
        if [ ! -z ${connect_timeout} ];then
            sed -i "s:^connect_timeout.*=.*:connect_timeout=${connect_timeout}:g" /etc/fdfs/storage.conf
        else
            sed -i "s:^connect_timeout.*=.*:connect_timeout=30:g" /etc/fdfs/storage.conf
        fi
        if [ ! -z ${network_timeout} ];then
            sed -i "s:^network_timeout.*=.*:network_timeout=${network_timeout}:g" /etc/fdfs/storage.conf
        else
            sed -i "s:^network_timeout.*=.*:network_timeout=60:g" /etc/fdfs/storage.conf
        fi
        if [ ! -z ${max_connections} ];then
            sed -i "s:^max_connections.*=.*:max_connections=${max_connections}:g" /etc/fdfs/storage.conf
        else
            sed -i "s:^max_connections.*=.*:max_connections=10240:g" /etc/fdfs/storage.conf
        fi
        if [ ! -z ${log_file_keep_days} ];then
            sed -i "s:^log_file_keep_days.*=.*:log_file_keep_days=${log_file_keep_days}:g" /etc/fdfs/storage.conf
        else
            sed -i "s:^log_file_keep_days.*=.*:log_file_keep_days=7:g" /etc/fdfs/storage.conf
        fi
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