# Dockerfile, Image, Container
# run:
# sudo docker run -p 8080:80 python-pystrokes --host "0.0.0.0" --port "80"
# or
# sudo docker run -p 8080:80 python-pystrokes
# build:
# sudo docker build -t python-pystrokes .
FROM python:3.9

RUN git clone https://github.com/connnnor/pystrokes.git
WORKDIR "/pystrokes"
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "./app.py"]
CMD ["--host", "0.0.0.0", "--port", "80"]
HEALTHCHECK CMD curl --fail "http://127.0.0.1:80/stroke" || exit 1
EXPOSE 80
