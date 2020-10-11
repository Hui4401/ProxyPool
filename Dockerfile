FROM python:3.8

LABEL maintainer="Assassin"

WORKDIR /root/ProxyPool

COPY . .

RUN pip install -i https://pypi.douban.com/simple -r requirements.txt

VOLUME /root/ProxyPool/logs

EXPOSE 5555

CMD python run.py
