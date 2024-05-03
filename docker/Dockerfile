FROM ubuntu:jammy-20230126

RUN apt-get update
RUN \
    apt install -y \
    python3 \
    python3-pip \
    python3-venv
RUN cd /opt

COPY ./ /opt
RUN \
    cd /opt/epsilon; \
    pip3 install -r requirements.txt;

WORKDIR /opt/epsilon

EXPOSE 8511

HEALTHCHECK CMD curl --fail http://localhost:8511/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8511", "--server.address=0.0.0.0"]