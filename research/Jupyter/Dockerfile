FROM openkbs/jre-mvn-py3:latest


COPY ./requirements.txt .

RUN pip install  --default-timeout=1000 --upgrade pip \
    && pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
