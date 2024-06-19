# Frontend/Dockerfile

FROM python:3.10.8

RUN mkdir -p app/frontend

WORKDIR /app/frontend

COPY Streamlit_Frontend .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]

CMD ["1_😁_Home.py"]
