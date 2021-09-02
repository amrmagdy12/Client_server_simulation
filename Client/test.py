from client import client
from threading import Thread

import time

c1 = client("nader")
c2 = client("ahmed")


def update_messages(client):
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # update every 1/10 of a second
        new_messages = client.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to local list of messages

        # if the client is disconnected
        if client.client_id.fileno() == -1:
            break

        for msg in new_messages:  # display new messages
            print(msg)


Thread(target=update_messages, args=(c1,)).start()

c1.send_message("hello ahmed")
time.sleep(1)

c2.send_message("hello nader")
time.sleep(1)

c1.send_message("how are u ")
time.sleep(1)

c2.send_message("iam fine ")
time.sleep(2)

c1.disconnect()
time.sleep(2)
c2.disconnect()
