FROM fedora:34 

RUN dnf install -y python3-pip which \
&& dnf clean all \
&& pip3 install pipenv

COPY . /sonos-doorbell

WORKDIR /sonos-doorbell

RUN pipenv install 

CMD ["/sonos-doorbell/run.sh"]

