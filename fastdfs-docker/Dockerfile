FROM alpine as git

RUN apk add git \
  && cd /srv && git clone https://github.com/happyfish100/libfastcommon.git \
  && cd libfastcommon; git checkout V1.0.43 \
  && cd /srv &&  git clone https://github.com/happyfish100/fastdfs.git \
  && cd fastdfs; git checkout V6.06 \
  && cd /srv && git clone https://github.com/happyfish100/fastdfs-nginx-module \
  && cd fastdfs-nginx-module; git checkout V1.22 \
  && cd /srv && wget https://nginx.org/download/nginx-1.16.1.tar.gz \
  && tar -zxf nginx-1.16.1.tar.gz \
  && rm nginx-1.16.1.tar.gz

FROM ubuntu

COPY --from=git /srv /srv
COPY nginx.conf /
COPY entrypoint.sh /

RUN apt-get update -y \
  && apt-get install gcc make libpcre3 libpcre3-dev openssl libssl-dev zlib1g-dev iputils-ping -y \
  && cd /srv/libfastcommon \
  && ./make.sh clean && ./make.sh && ./make.sh install \
  && cd /srv/fastdfs \
  && ./make.sh clean && ./make.sh && ./make.sh install \
  && ./setup.sh /etc/fdfs \
  && cd /srv/nginx-1.16.1 \
  && ./configure --add-module=/srv/fastdfs-nginx-module/src \
  && make && make install \
  && mv /nginx.conf /usr/local/nginx/conf/ \
  && cp /srv/fastdfs/conf/http.conf /etc/fdfs/ \
  && cp /srv/fastdfs/conf/mime.types /etc/fdfs/ \
  && cp /srv/fastdfs-nginx-module/src/mod_fastdfs.conf /etc/fdfs/ \
  && sed -i 's:base_path.*=.*:base_path=/data/storage:g' /etc/fdfs/storage.conf \
  && sed -i 's:store_path0.*=.*:store_path0=/data/storage:g' /etc/fdfs/storage.conf \
  && sed -i 's:base_path.*=.*:base_path=/data/storage:g' /etc/fdfs/mod_fastdfs.conf \
  && sed -i 's:store_path0.*=.*:store_path0=/data/storage:g' /etc/fdfs/mod_fastdfs.conf \
  && sed -i 's:url_have_group_name.*:url_have_group_name=true:g' /etc/fdfs/mod_fastdfs.conf \
  && sed -i 's:base_path.*=.*:base_path=/data/tracker:g' /etc/fdfs/tracker.conf \
  && sed -i 's:store_lookup.*=.*:store_lookup=0:g' /etc/fdfs/tracker.conf \
  && apt-get clean \
  && rm -rf /srv

VOLUME ["/data/storage"]
VOLUME ["/data/tracker"]
EXPOSE 22122 23000 8888
CMD ["/entrypoint.sh"]
