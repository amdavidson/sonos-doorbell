#Setup Sonos Doorbell Service

1. clone repository
2. `podman built -t sonos-doorbell .`
3. `podman run --net=host --restart=always --name=sonos-doorbell sonos-doorbell`
3. enable lingering for your user if you have not already
4. copy podman service to ~/.config/systemd/user/
5. `systemctl --user enable podman-sonos-doorbell.service`
5. configure `ngrok.yml`
4. copy ngrok service to ~/.config/systemd/user/
5. `systemctl --user enable ngrok-sonos-doorbell.service`
6. `systemctl --user start ngrok-sonos-doorbell.service`
7. configure IFTTT to connect an alexa command to the ngrok endpoint
8. configure an alexa routine to call the alexa command when the doorbell button is pressed
