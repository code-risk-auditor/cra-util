#FROM python:3-slim AS builder
FROM python:3
ADD . /app
WORKDIR /app

# We need the bash
RUN apt update && apt -y install bash graphviz

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app -r requirements.txt

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
#FROM gcr.io/distroless/python3-debian10
#FROM python:3
#COPY --from=builder /app /app
#WORKDIR /app
ENV PYTHONPATH /app
CMD ["python", "/app/main.py"]