from utime import sleep_ms, ticks_ms
from lora import *
import secrets

class LoraSender():
    messages = []
    lastcheck = None
    connecting = False

    def __init__(self, interval=120000, queue_limit=None, confirm_messages=True):
        # NOTE: independent of this setting the modem won't allow to send more than one
        # unconfimed message every 2 minutes, this is enforced by firmware and can not be changed.
        self.interval = interval
        self.lora = Lora(band=BAND_EU868, poll_ms=60000, debug=False)
        self.confirm_messages = confirm_messages
        self.queue_limit = queue_limit
        print("Firmware:", self.lora.get_fw_version())
        print("Device EUI:", self.lora.get_device_eui())
        self.appEui = secrets.appEui
        self.appKey = secrets.appKey

    def clear_messages(self):
        del self.messages[:]

    def add_message(self, message, port = 1):
        if self.queue_limit and len(self.messages) >= self.queue_limit:
            return
        self.messages.append({'message' : message, 'port' : port})

    def check(self):
        now = ticks_ms()
        should_send = self.lastcheck == None or (now - self.lastcheck) > self.interval
        if (not self.lastcheck or should_send):
            self.send_next_message()
            self.lastcheck = now

    def connect(self):
        self.connecting = True
        try:
            self.lora.join_OTAA(self.appEui, self.appKey, timeout=20000)
        except LoraErrorTimeout as e:
            print("Something went wrong; are you indoor? Move near a window and retry")
            print("ErrorTimeout:", e)
        except LoraErrorParam as e:
            print("ErrorParam:", e)

        self.connecting = False
        print("LoRa connected.")

    def replace_messages(self, message, port = 1):
        self.clear_messages()
        self.add_message(message, port)

    def send_next_message(self):
        if len(self.messages) == 0:
            return
        if self.lora.get_join_status() == False and not self.connecting:
            self.connect()

        if self.lora.get_join_status() == True:
            try:
                message = self.messages.pop(0)
                self.lora.set_port(message["port"])
                self.lora.send_data(message["message"], confirmed=self.confirm_messages)
                print("Message '%s' sent." % message["message"])
            except LoraErrorTimeout as e:
                print("ErrorTimeout:", e)
        else:
            print("Not connected")