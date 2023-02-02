FROM python:3.9.16

# Install app dependencies
COPY ./feedback-suggestion/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -qr /tmp/requirements.txt

# Create app directory
WORKDIR /usr/src/app

COPY ./feedback-suggestion/src/ src/

# Run the image as a non-root user
RUN groupadd -r textemb && useradd --no-log-init -r -g textemb textemb
RUN chown -R textemb:textemb /home/textemb
RUN chmod -R 755 /home/textemb
RUN mkdir -p /usr/src/app/logs/ && chown -R textemb:textemb /usr/src/app/
VOLUME ["/usr/src/app/logs"]
USER textemb

EXPOSE 8000
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "src:app"]