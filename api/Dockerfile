FROM python:3.10.2 


EXPOSE 8000

ENV TZ=Asia/Almaty

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /home/api_app/

COPY ./api_app/requirements.txt /home/api_app/requirements.txt
RUN pip install -r requirements.txt

COPY ./api_app /home/api_app/

ENTRYPOINT [ "./run_app.sh" ]
