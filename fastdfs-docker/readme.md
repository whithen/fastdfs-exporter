### 创建fdfs网络，启动2个tracker;2个group,2个storage容器

docker-compose up

### 测试

> docker exec -it fdfs_exporter_1 bash

> root@964e69f7deb0:/opt# fdfs_monitor /etc/fdfs/client.conf

> root@964e69f7deb0:/opt# fdfs_upload_file /etc/fdfs/client.conf requirements.txt

> group1/M00/00/00/wKgKUV-rkpqANxQYAAAAINOM8v4042.txt

> root@964e69f7deb0:/opt# fdfs_download_file /etc/fdfs/client.conf group1/M00/00/00/wKgKUV-rkpqANxQYAAAAINOM8v4042.txt

> root@964e69f7deb0:/opt# diff requirements.txt  wKgKUV-rkpqANxQYAAAAINOM8v4042.txt

> root@964e69f7deb0:/opt# curl localhost:9018/metrics

多网卡主机建议使用hostnetwork

### 参数说明

- SERVICE: [必选] tracker | storage（服务模式）
- TRACKER_LIST: [storage模式必选] 192.168.10.100;192.168.10.101（tracker列表）
- GROUP_LIST: [storage模式必选] group1,group2,group3（集群group列表）
- GROUP_NAME: [storage模式必选] group1（当前group name）
- connect_timeout: [可选] 链接超时（默认30s）
- network_timeout: [可选] 网络超时（默认60s）
- max_connections: [可选] 最大连接（默认10240）
- store_lookup: [可选] 存储轮询（默认2:优先最大可用空间storage）
- reserved_storage_space: [可选] 存储限制（默认10%:磁盘空间<10%不可用）
- log_file_keep_days: [可选] 日志保留（默认7天）