FROM mitmproxy/mitmproxy

WORKDIR /srv/banditio.inspector.backend

#install the pip libraries
RUN pip install tornado


#clone the application code.
RUN git clone https://github.com/AnalogJ/banditio.inspector.backend.git .

# Default command
CMD ["python","server.py"]
