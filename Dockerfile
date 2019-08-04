FROM python:3
WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV PORT 80
EXPOSE 80
CMD ["python", "-m", "tor_py_server"]
