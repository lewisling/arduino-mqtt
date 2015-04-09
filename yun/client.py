import sys
import paho.mqtt.client as mqtt

class Client:
    # Constructor
    def __init__(self):
        self.client = None

    # Client Callbacks
    def on_connect(self, _, __, ___, rc):
        if rc == 0:
            self.send_command("ca")
        else:
            self.send_command("cd")
    def on_message(self, _, __, msg):
        self.send_command("m:" + msg.topic + ":" + str(msg.payload))

    # Command Helpers
    def parse_command(self, line):
        segments = line.split(":")
        cmd = segments[0]
        remaining = segments[1:]
        if cmd == 'c':
            self.do_connect(remaining)
        elif cmd == 's':
            self.do_subscribe(remaining)
        elif cmd == 'u':
            self.do_unsubscribe(remaining)
        elif cmd == 'p':
            self.do_publish(remaining)
        elif cmd == 'd':
            self.do_disconnect()
    def send_command(self, line):
        sys.stdout.write(line + "\n")

    # Command Handlers
    def do_connect(self, args):
        if len(args) >= 3:
            self.client = mqtt.Client(args[2])
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            if len(args) >= 5:
                self.client.username_pw_set(args[3], args[4])
            self.client.connect(args[0], int(args[1]))
            self.client.loop_start()
    def do_subscribe(self, args):
        if len(args) >= 1:
            self.client.subscribe(args[0])
    def do_unsubscribe(self, args):
        if len(args) >= 1:
            self.client.unsubscribe(args[0])
    def do_publish(self, args):
        if len(args) >= 2:
            self.client.publish(args[0], args[1])
    def do_disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Main
    def run(self):
        c.send_command("ok")
        while True:
            self.parse_command(sys.stdin.readline()[0:-1])

# Main Loop

c = Client()
c.run()

# TODO: better error handling
