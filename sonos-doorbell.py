import time
import soco
from flask import Flask
from soco.snapshot import Snapshot


def play_alert(zones, alert_uri, alert_volume=20, alert_duration=0, fade_back=False):
    # Use soco.snapshot to capture current state of each zone to allow restore
    for zone in zones:
        zone.snap = Snapshot(zone)
        zone.snap.snapshot()
        print("snapshot of zone: {}".format(zone.player_name))

    # prepare all zones for playing the alert
    for zone in zones:
        # Each Sonos group has one coordinator only these can play, pause, etc.
        if zone.is_coordinator:
            if not zone.is_playing_tv:  # can't pause TV - so don't try!
                # pause music for each coordinators if playing
                trans_state = zone.get_current_transport_info()
                if trans_state["current_transport_state"] == "PLAYING":
                    zone.pause()

        # For every Sonos player set volume and mute for every zone
        zone.volume = alert_volume
        zone.mute = False

    # play the sound (uri) on each sonos coordinator
    print("will play: {} on all coordinators".format(alert_uri))
    for zone in zones:
        if zone.is_coordinator:
            zone.play_uri(uri=alert_uri, title="Sonos Alert")

    # wait for alert_duration
    time.sleep(alert_duration)

    # restore each zone to previous state
    for zone in zones:
        print("restoring {}".format(zone.player_name))
        zone.snap.restore(fade=fade_back)


def ring_doorbell():
    all_zones = soco.discover(allow_network_scan=True)
    if all_zones == None:
        return False

    # alert uri to send to sonos - this uri must be available to Sonos
    alert_sound = "https://archive.org/download/generic-Doorbell-ringtone/Doorbell-ringtone-Doorbell-ringtone.mp3"

    play_alert(
        all_zones,
        alert_sound,
        alert_volume=30,
        alert_duration=3,
        fade_back=False,
    )

    return "Ringaling..."


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "sonos-doorbell running"


@app.route("/ring")
def ring_route():
    return ring_doorbell()
