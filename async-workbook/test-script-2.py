import asyncio
import logging


logging.basicConfig(format="%(asctime)s :: %(levelname)s :: %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

# Awaitables are objects that implements a special __await__ method
# An object has to be awaitable to use "await" keyword before it
# why can't we use "await" with sync code  ... like with "time.sleep"  or why can't we use "await" with sync funtions : 
# Sync libs don't have a mechanism to work with the event loop .. they don't know how to yeild control over and resume later.

# what does "await" do ?
# So when you are awaiting something you are telling the event loop pause the execution of the current function and yeild control back to the event loop
# which can then run another task. The current function, it'll stay suspended until the awaitable completes

#  In python asyncio there are three type of awaitable objects
# 1. coroutines - which are created when you call an async function
# 2. tasks - wrappers around coroutines that are scheduled on the event loop
# 3. futures - low level objects representing eventual results.





async def future_fn():
    # futures - low level objects representing eventual results.
    loop = asyncio.get_running_loop()
    future = loop.create_future() # a promise like obj
    logger.info(future)

    # Futures job is to hold a certain state and result
    # The state can be pending, meaning the -- means the future doesn't have any state or exception yet.
    # It can be cancelled using future.cancelled
    # It can be finished by a result -- set by future.set_result or it can be an exception with future.set_exception

    future.set_result("Completed")
    res = await future
    logger.info(f"RESULT : {res}")



# co-routine
async def async_fn():
    logger.info("Start of async fn")
    await asyncio.sleep(2)
    logger.info("Sleep Completed")
    return "Co-routine completed"

async def main():

    a_fn = async_fn() # fn wont run - it creates an object -- do not gets scheduled on the event loop
    logger.info(a_fn)
    res = await a_fn # awaiting a coroutine obj - schedule it in event-loop and run till completion
    logger.info(res)
    # when we await a coroutine obj directly like this ... it's both scheduled on the event loop and run to completion at the same time


# TASK -- are wrapped coroutine that can be executed independently 
# Task are how we actually run co-routines concurrently 
# when you wrap a co-routine in a task using asyncio.create_task
# Its handed over to event loop and scheduled to run whenever it gets a chance
# Task will keep track of .. whether the coroutine finish successfully or raised an error or got cancelled .. just like a future would
# Task are 'future' under the hood , but with extra logic to run the co-routine and do the work we want to do.
# unlike co-routine obj .. task can be scheduled on the event loop .. and just sit there without being run .. until the loop gets control.
# We can queue up mutliple task at once and the event loop will be able to run them whenever its ready 

async def task_fn():

    t = asyncio.create_task(async_fn())
    logger.info(t)
    logger.info('Task created .. now going to await it')
    res = await t
    logger.info(res)
    



if __name__ == "__main__":

    # asyncio.run(future_fn())

    # asyncio.run(async_fn())

    # asyncio.run(main())

    asyncio.run(task_fn())



