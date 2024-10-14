from btdht import DHT
import binascii

def main():
    dht = DHT()
    dht.start()
    print(dht.get_peers(binascii.a2b_hex("0403fb4728bd788fbcb67e87d6feb241ef38c75a")))
    # dht.get_peers(binascii.a2b_hex("8e2e2c13bf3460835c50ede96293205fec7cda7f"))
