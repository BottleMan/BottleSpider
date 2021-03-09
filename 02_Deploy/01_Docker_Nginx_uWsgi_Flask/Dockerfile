FROM python:3.6
ADD . /code
WORKDIR /code

# install python library
RUN python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# update source list
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean

# install packages
RUN apt-get update \
	&& apt-get install -y nginx uwsgi uwsgi-plugin-python3

# copy nginx config file
COPY nginx_uwsgi.conf /etc/nginx/conf.d

CMD ["/bin/sh", "start_script.sh"]