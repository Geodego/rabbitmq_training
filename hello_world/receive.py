"""
This program receive a message from the queue and print it on the screen.

June 21, 2022
"""
import pika, sys, os


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # we need to connect to RabbitMQ server. The next step is to make sure that the queue exists. Creating a queue using queue_declare is idempotent ‒ we can run
    # the command as many times as we like and only one will be created.
    # We have already declared the queue in send.py. We could avoid that if we were sure that the queue already exists, for example if send.py program was run before.
    # But we're not yet sure which program to run first. In such cases it's a good practice to repeat declaring the queue in both programs.
    channel.queue_declare(queue="hello")

    def callback(ch, method, properties, body):
        """
        Receiving messages from the queue is works by subscribing a callback function to a queue. Whenever we receive a message, 
        this callback function is called by the Pika library. This function will print on the screen the contents of the message.
        """
        print(" B Received %r" % body)

    # We need to tell RabbitMQ that this particular callback function should receive messages from our hello queue.
    # For that command to succeed we must be sure that a queue which we want to subscribe to exists. Fortunately we're confident
    # about that ‒ we've created a queue above ‒ using queue_declare.
    channel.basic_consume(queue="hello", auto_ack=True, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
