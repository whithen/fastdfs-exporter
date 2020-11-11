# fastdfs-exporter
fastdfs监控

![image](https://github.com/whithen/fastdfs-exporter/blob/master/FastDFSMonitor.jpg)

### docker运行

sudo docker run -it --rm \
-p 9018:9018 \
-e TRACKER_SERVER="192.168.10.81:22122;192.168.10.82:22122" \
docekrimage

### curl localhost:9018/metrics

\# HELP fastdfs_tracker_server_info fastdfs_tracker_server_info
\# TYPE fastdfs_tracker_server_info gauge
fastdfs_tracker_server_info{tracker="192.168.10.81:22122"} 1.0
fastdfs_tracker_server_info{tracker="192.168.10.82:22122"} 1.0
\# HELP fastdfs_group_info fastdfs_group_info
\# TYPE fastdfs_group_info gauge
fastdfs_group_info{group="group1"} 1.0
fastdfs_group_info{group="group2"} 2.0
\# HELP fastdfs_storage_server_count fastdfs_storage_server_count
\# TYPE fastdfs_storage_server_count gauge
fastdfs_storage_server_count{group="group1"} 2.0
fastdfs_storage_server_count{group="group2"} 1.0
\# HELP fastdfs_active_server_count fastdfs_active_server_count
\# TYPE fastdfs_active_server_count gauge
fastdfs_active_server_count{group="group1"} 1.0
fastdfs_active_server_count{group="group2"} 1.0
\# HELP fastdfs_disk_total_space fastdfs_disk_total_space
\# TYPE fastdfs_disk_total_space gauge
fastdfs_disk_total_space{group="group1"} 6.9463965696e+011
fastdfs_disk_total_space{group="group2"} 1.67011418112e+012
\# HELP fastdfs_disk_free_space fastdfs_disk_free_space
\# TYPE fastdfs_disk_free_space gauge
fastdfs_disk_free_space{group="group1"} 5.34387884032e+011
fastdfs_disk_free_space{group="group2"} 1.670043926528e+012
\# HELP fastdfs_storage_server_info fastdfs_storage_server_info
\# TYPE fastdfs_storage_server_info gauge
fastdfs_storage_server_info{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 1.0
fastdfs_storage_server_info{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 6.0
fastdfs_storage_server_info{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 6.0
\# HELP fastdfs_storage_version fastdfs_storage_version
\# TYPE fastdfs_storage_version gauge
fastdfs_storage_version{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 6.06
fastdfs_storage_version{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 6.06
fastdfs_storage_version{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 6.06
\# HELP fastdfs_join_time fastdfs_join_time
\# TYPE fastdfs_join_time gauge
fastdfs_join_time{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 1.604990102e+09
fastdfs_join_time{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 1.60119119e+09
fastdfs_join_time{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 1.601191172e+09
\# HELP fastdfs_up_time fastdfs_up_time
\# TYPE fastdfs_up_time gauge
fastdfs_up_time{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_up_time{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 1.604990241e+09
fastdfs_up_time{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 1.604989837e+09
\# HELP fastdfs_total_storage fastdfs_total_storage
\# TYPE fastdfs_total_storage gauge
fastdfs_total_storage{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_total_storage{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 1.67011418112e+012
fastdfs_total_storage{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 1.67011418112e+012
\# HELP fastdfs_free_storage fastdfs_free_storage
\# TYPE fastdfs_free_storage gauge
fastdfs_free_storage{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_free_storage{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 1.670042877952e+012
fastdfs_free_storage{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 1.670043926528e+012
\# HELP fastdfs_total_upload_count fastdfs_total_upload_count
\# TYPE fastdfs_total_upload_count gauge
fastdfs_total_upload_count{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_total_upload_count{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 56.0
fastdfs_total_upload_count{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 9.0
\# HELP fastdfs_success_upload_count fastdfs_success_upload_count
\# TYPE fastdfs_success_upload_count gauge
fastdfs_success_upload_count{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_success_upload_count{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 56.0
fastdfs_success_upload_count{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 9.0
\# HELP fastdfs_total_delete_count fastdfs_total_delete_count
\# TYPE fastdfs_total_delete_count gauge
fastdfs_total_delete_count{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_total_delete_count{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 0.0
fastdfs_total_delete_count{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 0.0
\# HELP fastdfs_success_delete_count fastdfs_success_delete_count
\# TYPE fastdfs_success_delete_count gauge
fastdfs_success_delete_count{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_success_delete_count{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 0.0
fastdfs_success_delete_count{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 0.0
\# HELP fastdfs_total_download_count fastdfs_total_download_count
\# TYPE fastdfs_total_download_count gauge
fastdfs_total_download_count{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_total_download_count{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 2.0
fastdfs_total_download_count{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 1.0
\# HELP fastdfs_success_download_count fastdfs_success_download_count
\# TYPE fastdfs_success_download_count gauge
fastdfs_success_download_count{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_success_download_count{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 2.0
fastdfs_success_download_count{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 1.0
\# HELP fastdfs_total_upload_bytes fastdfs_total_upload_bytes
\# TYPE fastdfs_total_upload_bytes gauge
fastdfs_total_upload_bytes{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_total_upload_bytes{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 421073.0
fastdfs_total_upload_bytes{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 16704.0
\# HELP fastdfs_success_upload_bytes fastdfs_success_upload_bytes
\# TYPE fastdfs_success_upload_bytes gauge
fastdfs_success_upload_bytes{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_success_upload_bytes{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 421073.0
fastdfs_success_upload_bytes{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 16704.0
\# HELP fastdfs_total_download_bytes fastdfs_total_download_bytes
\# TYPE fastdfs_total_download_bytes gauge
fastdfs_total_download_bytes{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_total_download_bytes{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 15398.0
fastdfs_total_download_bytes{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 1856.0
\# HELP fastdfs_success_download_bytes fastdfs_success_download_bytes
\# TYPE fastdfs_success_download_bytes gauge
fastdfs_success_download_bytes{group="group1",ip="192.168.10.73",storage="storage1",version="6.06"} 0.0
fastdfs_success_download_bytes{group="group1",ip="192.168.10.81",storage="storage2",version="6.06"} 15398.0
fastdfs_success_download_bytes{group="group2",ip="192.168.10.82",storage="storage1",version="6.06"} 1856.0
