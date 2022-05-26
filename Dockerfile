FROM continuumio/miniconda3

WORKDIR /corn_backend

SHELL ["/bin/bash", "--login", "-c"]

RUN conda create -n corn_env python=3.10

RUN conda init bash
RUN conda activate corn_env
COPY . .

EXPOSE 8000

#ENTRYPOINT ["python", "manage.py", "runserver"]