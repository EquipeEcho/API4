FROM ubuntu:22.04

RUN apt-get update && apt-get install -y fuse

COPY ODAFileConverter_QT6_lnxX64_8.3dll_27.1.AppImage /app/oda

RUN chmod +x /app/oda

ENTRYPOINT ["/app/oda", "--appimage-extract-and-run"]