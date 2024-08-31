FROM python:3.11.6-alpine

WORKDIR /app

COPY SztuSrunLogin SztuSrunLogin

COPY main.py main.py

RUN pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV TZ=Asia/Shanghai

CMD ["python", "-u", "main.py"]