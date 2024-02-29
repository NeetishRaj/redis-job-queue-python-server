import time
from lib.logger import logger

def time_taking_task(query_arg1, query_arg2):
    delay = 10
    time.sleep(delay)

    message = f"Job Worker: Heavy task completed after {delay} seconds. query_arg1: '{query_arg1}', query_arg2: '{query_arg2}'"
    logger.info(message)
    print(message)

    # result = { message, query_arg1, query_arg2}
    result = {
        "message": message,
        "query_arg1": query_arg1,
        "query_arg2": query_arg2
    }

    return result


if __name__ == "__main__":
    time_taking_task()