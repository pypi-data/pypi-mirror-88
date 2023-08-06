import yodel
from time import sleep,time

yodel.startRadio("wlx00c0caa5efb2")
yodel.setName("alden")
yodel.addGroup("robot")
yodel.setChannel(5)
its = 0
st = time()
while True:
    its += 1
    sleep(.01)
    yodel.send("this is a cool message", name="listener")
    data = yodel.listen()
    if its%10000 == 0:
        print(its/(time()-st))

    #if data:
    #    data.print()
    #print(data)
