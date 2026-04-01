from apscheduler.schedulers.blocking import BlockingScheduler
from check_replies import check_for_replies

scheduler = BlockingScheduler()
scheduler.add_job(check_for_replies, "interval", minutes=1)

print("Reply checker started...")
scheduler.start()