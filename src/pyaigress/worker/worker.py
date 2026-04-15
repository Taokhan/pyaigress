from arq.connections import RedisSettings
from pyaigress.worker.documentTask import process_document
import os
from dotenv import load_dotenv

load_dotenv()

class WorkerSettings:
    functions = [process_document]
    redis_settings = RedisSettings.from_dsn(os.environ["REDIS_URL"])
    max_jobs = 4
    job_timeout = 300  # 5 minutes per job