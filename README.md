# fastdfs-exporter
fastdfs监控

![image](https://github.com/whithen/fastdfs-exporter/blob/master/FastDFS Monitor.jpg)

docker运行
sudo docker run -it --rm \
-p 9018:9018 \
-e TRACKER_SERVER="192.168.10.81:22122;192.168.10.82:22122" \
docekrimage

curl localhost:9018/metrics
