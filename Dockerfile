FROM debian:bookworm-slim


RUN apt-get update && \
    apt-get install -y fortune-mod cowsay netcat-openbsd bash ca-certificates && \
    rm -rf /var/lib/apt/lists/*



ENV PATH="/usr/games:${PATH}"


WORKDIR /app


COPY wisecow.sh .


RUN chmod +x wisecow.sh


EXPOSE 4499


CMD ["./wisecow.sh"]
