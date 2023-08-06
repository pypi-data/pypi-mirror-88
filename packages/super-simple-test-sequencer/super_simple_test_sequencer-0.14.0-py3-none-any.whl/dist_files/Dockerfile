# Get Ubuntu just for the qemu-arm-static
FROM ubuntu:latest as ubuntu_build
RUN apt-get update && apt-get install -y qemu-user-static

# Here starts the actual SSTS build configuration
FROM arm32v7/ubuntu:latest

# Copy qemu to image to enable building for arm
COPY --from=ubuntu_build /usr/bin/qemu-arm-static /usr/bin

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  git \
  python3-pip

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install --upgrade super_simple_test_sequencer

COPY . .

# Delete ui if it's there
RUN rm -rf ui

RUN mkdir ui
RUN mkdir ui/build

# And replace ui with only the build result from build-UI
COPY --from=gaia_ui:latest /usr/src/app/build ui/build

# qemu is not needed after this step
RUN rm /usr/bin/qemu-arm-static

EXPOSE 80

CMD python3.6 gaia.py HermesSmema

# Command to build: docker build --platform linux/arm/v7  --tag localhost:5000/gaia_arm:1.7  .
# Command to build:  docker build --platform linux/arm/v7  --tag localhost:5000/gaia_arm:1.7  .

# Command to run: docker run -p 80:80  -v /etc/timezone:/etc/timezone  192.168.1.215:5000/gaia_arm:1.7
# https://www.docker.com/blog/getting-started-with-docker-for-arm-on-linux/
# https://github.com/docker/buildx/issues/159
# https://ownyourbits.com/2018/06/27/running-and-building-arm-docker-containers-in-x86/
