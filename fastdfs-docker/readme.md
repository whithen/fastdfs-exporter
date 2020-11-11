### 创建fdfs网络，启动2个tracker;2个group,2个storage容器

docker-compose up

### 测试

docker exec -it fdfs_exporter_1 bash

root@964e69f7deb0:/opt# fdfs_monitor /etc/fdfs/client.conf

root@964e69f7deb0:/opt# fdfs_upload_file /etc/fdfs/client.conf requirements.txt 

group1/M00/00/00/wKgKUV-rkpqANxQYAAAAINOM8v4042.txt

root@964e69f7deb0:/opt# fdfs_download_file /etc/fdfs/client.conf group1/M00/00/00/wKgKUV-rkpqANxQYAAAAINOM8v4042.txt

root@964e69f7deb0:/opt# diff requirements.txt  wKgKUV-rkpqANxQYAAAAINOM8v4042.txt 

root@964e69f7deb0:/opt# curl localhost:9018/metrics
