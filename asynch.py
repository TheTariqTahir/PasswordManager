import asyncio
import time

import threading

async def main():
    task = asyncio.create_task(test())
    # await task
    print('finished')

async def test():
    print('run')
    await asyncio.sleep(5)
    print('first')
    
def first():
    time.sleep(5)
    print('first')

def second():
    time.sleep(2)
    print('2nd')
    
# asyncio.run(main())
t1= threading.Thread(target=first)
t2= threading.Thread(target=second)

t1.start()
t2.start()
