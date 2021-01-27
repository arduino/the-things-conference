from utime import sleep_ms
from lora_sender import LoraSender

sender = LoraSender(interval=10000)
sender.add_message("Test message", 1)
sender.add_message("LoRa is awesome!", 2)
#sender.replace_messages("Final message.", 3)

while True:
    sender.check()
    sleep_ms(1000)
