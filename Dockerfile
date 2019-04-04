FROM alpine:latest

RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.8/main/" > /etc/apk/repositories

WORKDIR /code/

COPY . /code/

ENV TIME_ZONE Asia/Shanghai

RUN apk add --no-cache -U tzdata \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && echo "${TIME_ZONE}" > /etc/timezone

RUN apk add --no-cache --virtual=build-dependencies \
    mariadb-dev \
    g++ supervisor \
    build-base libffi-dev \
    libffi openssl ca-certificates \
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    linux-headers pcre-dev

RUN apk add --no-cache python3 \
    && apk add --no-cache python3-dev \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --no-cache-dir --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
    && pip3 install -r /code/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
    && rm -rf /var/cache/apk/* \
    && rm -rf ~/.cache/pip

RUN mkdir -p /var/log/supervisor /var/log/tornado

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 8000
CMD ["/usr/bin/supervisord","-n"]
