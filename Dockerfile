# To Build: docker build --no-cache -t pbui/cse-30341-fa26-assignments . 

FROM        debian:trixie-slim
LABEL	    org.opencontainers.image.authors="Peter Bui <pbui@nd.edu>"
ENV	    DEBIAN_FRONTEND=noninteractive

RUN	    apt install --update -y \
		python3-tornado python3-requests python3-yaml python3-markdown \
		curl bc netcat-openbsd iproute2 zip unzip gawk \
		gcc g++ make valgrind cppcheck libssl-dev && \
	    apt clean && \
	    rm -fr /var/lib/apt/lists/*
