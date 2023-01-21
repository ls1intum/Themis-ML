FROM python:3.9.16

# Install app dependencies
COPY ./inject-test-data/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -qr /tmp/requirements.txt

# Create app directory
WORKDIR /usr/src/app

COPY ./inject-test-data/src/ src/

# Run the image as a non-root user
RUN groupadd -r textemb && useradd --no-log-init -r -g textemb textemb
RUN mkdir -p /usr/src/app/logs/ && chown -R textemb:textemb /usr/src/app/
VOLUME ["/usr/src/app/logs"]
USER textemb

ENV THEMIS_URL=http://localhost:8000
ENV TEST_SERVER_URL=http://localhost:8001

EXPOSE 8001
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8001", "src:app"]