From python:3.7
WORKDIR /opt/python
RUN apt update && apt install -y cmake gcc vim wget curl 
RUN pip3 install -i https://pypi.douban.com/simple/ requests
RUN pip3 install -i https://pypi.douban.com/simple/ PyMySQL
RUN apt autoclean && apt clean
RUN rm -rf /tmp/*
CMD ["python3", "apply.py"]
