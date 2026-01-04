import asyncio
import logging
import argparse
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter(fmt="%(asctime)s :: %(levelname)s :: %(message)s"))
logger.addHandler(console)

async def a_fn(param:int):
    logger.info(f"START async fn {param}")
    await asyncio.sleep(delay=param)
    logger.info(f"Completed sleeping ... fn {param}")
    return f"Completed running fn {param}"

# CREATE TASKS
async def main(param:int=1):
    fn1 = asyncio.create_task(a_fn(param))
    fn2 = asyncio.create_task(a_fn(param + 1))

    logger.info("Running .. Main")
    res1 = await fn1
    res2 = await fn2
    logger.info("Main fn completed")

    return [res1, res2]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='asyncio 101', description="study asyncio by coding")
    parser.add_argument("-p", "--param", help="sleep delay an interger value", type=int)

    args = parser.parse_args()

    start = time.perf_counter()
    res = asyncio.run(main(args.param))
    stop = time.perf_counter()

    logger.info(f"Results : {res}")
    logger.info(f"TIME COST : {stop - start :0.2f}")