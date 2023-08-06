import yodel
from time import sleep

yodel.startRadio("wlx00c0caa5efb2")
yodel.setName("listener")
#yodel.addGroup("group_of_robots")
yodel.setChannel(5)
#yodel.enableRelay()

while True:

    #yodel.send("funny", name="alden",group="robot")
    #data = yodel.listen()
    sleep(0.1)
    data = yodel.listen()
    #sleep(0.1)
    if data:
        print(data.payload)
    #print(data)