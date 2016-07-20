FROM mitmproxy/mitmproxy

WORKDIR /srv/banditio.engine

#install the pip libraries
RUN pip install tornado

#clone the application code.
RUN git clone https://github.com/AnalogJ/banditio.engine.git .

# Default command
CMD ["python","engine.py"]
