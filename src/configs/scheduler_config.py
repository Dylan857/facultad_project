from flask_apscheduler import APScheduler
from dotenv import load_dotenv
import os

load_dotenv()

class SchedulerConfig:
    def __init__(self, app):
        self.SCHEDULER_API_ENABLED = os.getenv("SCHEDULER_API_ENABLED")
        self.JOBS = eval(os.getenv("JOBS"))
