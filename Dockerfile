FROM iofog/python3
RUN pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install iofog && \
    python3 -m pip install ws4py && \
    python3 -m pip install json_logging
COPY . /sensors
WORKDIR  /sensors
CMD ["python3", "index.py"]