from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import warner
import archiver
import announcer
import flagger
import os


# When testing changes, set the "TEST_SCHEDULE" envvar to run more often
if os.getenv("TEST_SCHEDULE"):
    schedule_kwargs = {"hour": "*", "minute": "*/10"}
else:
    schedule_kwargs = {"hour": "10"}

logging.basicConfig()
sched = BlockingScheduler()

@sched.scheduled_job("cron", **schedule_kwargs)
def destalinate_job():
    print("Destalinating")
    if "SB_TOKEN" not in os.environ or "API_TOKEN" not in os.environ:
        print("ERR: Missing at least one Slack environment variable.")
    else:
        scheduled_warner = warner.Warner()
        scheduled_archiver = archiver.Archiver()
        scheduled_announcer = announcer.Announcer()
        scheduled_flagger = flagger.Flagger()
        print("Warning")
        scheduled_warner.warn()
        print("Archiving")
        scheduled_archiver.archive()
        print("Announcing")
        scheduled_announcer.announce()
        print("Flagging")
        scheduled_flagger.flag()
        print("OK: destalinated")
    print("END: destalinate_job")

sched.start()
