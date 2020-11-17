# fastdfs-exporter
### Dashboard

![image](https://github.com/whithen/fastdfs-exporter/blob/master/FastDFSMonitor.png)

### docker运行

> sudo docker run -it --rm \\\
> -p 9018:9018 \\\
> -e TRACKER_SERVER="192.168.10.81:22122;192.168.10.82:22122" \\\
> whithen/fastdfs-exporter:v6.06

### curl localhost:9018/metrics
