FROM iofog/python
COPY index.py /src/
WORKDIR  /src
CMD ["python", "index.py"]