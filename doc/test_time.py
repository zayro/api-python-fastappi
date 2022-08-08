
import time

import threading 


def uno():
    time.sleep(2.4)
    print('uno')


def dos():
    print('dos')


uno()
dos()


print('----------------')


t1 = threading.Thread(target=uno)  
t2 = threading.Thread(target=dos)  

t1.start()
t2.start()