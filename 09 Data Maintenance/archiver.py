#!/usr/bin/env python

import sys
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer,KafkaError, OFFSET_BEGINNING
from google.cloud import storage
import zlib
import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

bucket_name = "trimet_data"
source_file_name = "/home/kajal/test-cons.json"
destination_blob_name = "trimet_data_obj"
def upload_blob(bucket_name, contents, destination_blob_name):
    service_key_path='/home/kajal/trimet-project-key.json'
    storage_client = storage.Client.from_service_account_json(service_key_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    json_contents = '\n'.join(contents)
    compressed_data = zlib.compress(json_contents.encode(), -1)
    (publicKey, privateKey) = rsa.newkeys(2048)
    symmetric_key = get_random_bytes(32)
    encrypted_symmetric_key = rsa.encrypt(symmetric_key, publicKey)
    cipher = AES.new(symmetric_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(compressed_data)
    blob.upload_from_string(ciphertext)
    
if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    count=0
    contents=[]
    topic = "archivetest"
    consumer.subscribe([topic], on_assign=reset_offset)
    # Poll for new messages from Kafka and print them.
    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                print("Consumed message from topic {topic} with event={event}".format(
                    topic=topic,
                    event=msg.value().decode('utf-8')
                ))
                count=count+1
                contents.append(msg.value().decode('utf-8'))
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
        
        upload_blob(
            bucket_name=bucket_name,
            contents=contents,
            destination_blob_name=destination_blob_name,
        )
print(count)
