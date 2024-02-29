import requests
from lib.logger import logger


def on_success_callback(job, connection, result, *args, **kwargs):
  
    message = result.get("message")
    query_arg1 = result.get("query_arg1")
    query_arg2 = result.get("query_arg2")

    logger.info(
        f"on_succes_callback: Job ID '{job.id}' successfully completed. query_arg1: '{query_arg1}', query_arg2: '{query_arg2}'"
    )
    logger.info(f"on_succes_callback: Job completion message: {message}")

    # task is completed, now let's notify the relevant API, service etc. (if required)
    
    try:
        response = requests.post('https://test.com/', json=result)

        if response.status_code == 200:
            logger.info("on_succes_callback: Task notification POST successful!")
            logger.info("on_succes_callback: Task notification Response:", response.json())
        else:
            logger.error("on_succes_callback: Task notification POST failed with status code:", response.status_code)
    except Exception as e:
        logger.critical(f"on_succes_callback: Task notification POST failed {e}")


def on_failure_callback(job, connection, type, value, traceback):
    logger.error(f"on_failure_callback: Job  with ID '{job.id}' failed, retry!")


def on_stopped_callback(job, connection):
    logger.critical(f"on_stopped_callback: Job  with ID '{job.id}', failed as Job worker stopped")





