FROM python:3.12-alpine
# Usuario no-root para OCP "restricted"
RUN adduser -D -u 10001 app
WORKDIR /app
COPY app.py /app/
# Este servicio no usa PyMongo (solo proxy a DATA)
USER 10001
EXPOSE 8080
CMD ["python", "app.py"]