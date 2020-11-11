#fastdfs-exporter
FROM alpine as git

RUN apk add git \
  && cd /srv && git clone https://github.com/happyfish100/libfastcommon.git \
  && cd libfastcommon; git checkout V1.0.43 \
  && cd /srv &&  git clone https://github.com/happyfish100/fastdfs.git \
  && cd fastdfs; git checkout V6.06

FROM ubuntu
LABEL maintainer="1045002003@qq.com"

COPY --from=git /srv /srv
COPY requirements.txt /tmp/requirements.txt
COPY . /opt/

RUN apt-get update -y \
  && apt-get install gcc make -y \
  && cd /srv/libfastcommon \
  && ./make.sh clean && ./make.sh && ./make.sh install \
  && cd /srv/fastdfs \
  && ./make.sh clean && ./make.sh && ./make.sh install \
  && ./setup.sh /etc/fdfs \
  && sed -i 's#base_path.*=.*#base_path=/tmp#g' /etc/fdfs/client.conf \
  && apt install python3 python3-pip -y \
  && pip3 install -r /tmp/requirements.txt \
  && apt-get clean \
  && rm -rf /srv

WORKDIR /opt
EXPOSE 9018
CMD ["gunicorn", "--workers=4", "src.wsgi:app", "-b 0.0.0.0:9018"]
