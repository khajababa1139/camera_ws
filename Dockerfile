FROM ultralytics/ultralytics:latest-jetson-jetpack4

RUN apt-get update && \
    apt-get install -y nano git && \
    pip3 install --no-cache-dir websockets

RUN git clone https://github.com/your/repository.git /workspace/repository

WORKDIR /workspace/repository

CMD ["/bin/bash"]