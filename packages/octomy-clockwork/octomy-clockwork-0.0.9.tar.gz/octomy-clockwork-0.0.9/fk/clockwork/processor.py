from fk.clockwork.db import Database
from pprint import pformat
import datetime
import fk.utils
import fk.utils.Watchdog
import logging
import pytz
import re
import schedule
import time
import traceback

logger = logging.getLogger(__name__)


def job():
    logger.info("Performing dummy job")


props = ["seconds", "minutes", "hours", "days", "weeks", "second", "minute", "hour", "day", "week", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def parse_schedule(spec, job=job, tag=None):
    # logger.info(f"Processing spec: {spec}")
    if str != type(spec):
        logger.error("Spec not string")
        return None
    spec = "." + spec.strip()
    if not spec:
        logger.error("Empty spec")
        return None
    parts = spec.split(".")
    if not parts:
        logger.error("Could not split spec")
        return None
    if parts[0] == "schedule":
        del parts[0]
    better = "." + ".".join(parts)
    regex = r"\.(?P<op>every|to|at|do|" + "|".join(props) + r')(?:\([\'"]?(?P<arg>job|[1-9]?[0-9]*|[1-9][0-9]*:[0-9][0-9]|:[0-9][0-9])[\'"]?\))?'
    # logger.info(f"REGEX IS: {regex}")
    matches = list(re.finditer(regex, better))
    # logger.info(f"Found total of {len(matches)} matches")
    if not matches:
        logger.error("No matches in spec")
        return None
    first = True
    base = None
    saw_job = False
    processed = 0
    for match in matches:
        groups = match.groupdict()
        # logger.info(groups)
        op = groups.get("op")
        arg = groups.get("arg")
        try:
            arg = int(arg)
        except:
            pass
        # logger.info(f"Match[{processed}]: {op}({arg}) ----")
        processed += 1
        try:
            if first:
                first = False
                if op != "every":
                    logger.error("Spec did not start with 'every'")
                    return None
                base = schedule.every(int(float(arg or 1)))
                if tag:
                    base.tag(tag)
                # logger.info("Created schedule")
                continue
            if saw_job:
                logger.error("Commands after job")
                return None
            if op == "every":
                logger.error("Invalid second call to every")
                return None
            if op in props:
                base = getattr(base, op)
                # logger.info(f"Added {op}")
                continue
            if op in ["to", "at"]:
                func = getattr(base, op)
                base = func(arg)
                # logger.info(f"Added {op}({arg})")
                continue
            if op == "do":
                if arg != "job":
                    logger.error(f"Invalid job {arg}")
                    return None
                base = base.do(job)
                # logger.info(f"Finalized")
                saw_job = True
                continue
        except Exception as e:
            logger.error(f'Failed to parse schedule with "{e}"')
            return None
    # Output: ['cats', 'dogs']
    # logger.info(f"Processed total of {processed} matches")
    return base
    # [x.group() for x in re.finditer( r'all (.*?) are', 'all cats are smarter than dogs, all dogs are dumber than cats')]
    # Output: ['all cats are', 'all dogs are']


class Processor:
    def __init__(self, config):
        self.config = config
        self.db = Database(self.config)
        self.task_filter = re.compile("^([0-9a-z\-_]+)$")
        self.last_status_time = None
        self.callables = {}
        self.last_time = self.db.get_now()
        self.universal_basetime = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)

    def _execute_safely(self, entrypoint, item):
        # logger.info("SAFE EXECUTION STARTED!")
        # We cap runtime at 60 seconds
        timeout = 30
        failure = None
        result = None
        try:
            watchdog = fk.utils.Watchdog.Watchdog(timeout)
            # logger.info("££££ Entry")
            result, failure = entrypoint(item, self.config)
            # logger.info("££££ Exit")
        except fk.utils.Watchdog.Watchdog:
            logger.warning("Watchdag triggered exception")
            failure = f"execution timed out after {timeout} seconds"
        except Exception as e:
            logger.warning("")
            logger.warning("")
            logger.warning(f"###############################################")
            logger.warning(f"#    Batch item: {item}")
            logger.warning(f"# Failed with: {e}")
            failure = f"{e}"
            logger.warning(f"#          At:")
            traceback.print_exc()
            logger.warning(f"#######################################")
            logger.warning("")
            logger.warning("")
        watchdog.stop()
        # logger.info("SAFE EXECUTION FINISHED!")
        return result, failure

    def execute_one_cron(self):
        """
        Take ownership of one cron and make sure it is properly executed and updated with status underway
        """
        item = self.db.book_batch_item(self.db.PENDING, self.db.IN_PROGRESS)
        if item:
            logger.info("Processing item:")
            logger.info(pformat(item))
            id = item.get("id", None)
            type = item.get("type", None)
            updated_at = item.get("updated_at", None)
            if id and type and updated_at:
                entrypoint, failure = self.get_callable_for_type(type)
                if entrypoint and failure:
                    entrypoint = None
                    failure = f"{failure} AND ENTRYPOINT WAS SET!"
                result = None
                if entrypoint:
                    result, failure = self._execute_safely(entrypoint, item)
                if failure:
                    logger.warning("¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ CRON FILTER FAILED WITH ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤")
                    logger.warning(failure)
                    logger.warning("")
                id2, updated_at2 = self.db.bump_batch_item(id, self.db.FAILED if failure else self.db.DONE, failure, updated_at) or (None, None)
                logger.info(f"id2={id2}, updated_at2={updated_at2}, id={id}, updated_at={updated_at}")
            else:
                logger.warning(f"Missing data for item id={id}, type={type}, updated_at={updated_at}")

        # else:
        # logger.info(f"No pending items found")

    def get_now(self):
        return self.db.get_now()

    def get_crons(self):
        return self.db.get_crons(limit=100)

    def log_cron_run(self, cron_id):
        self.db.log_cron_run(cron_id)

    def upsert_cron(self, type="test", data=None, priority=50, source=None):
        """
        Insert a new cron item into the database, ready for execution
        """
        return self.db.insert_cron_item({"priority": priority, "data": data, "type": type, "status": self.db.PENDING, "source": source})

    def delete_all_crons(self, time_sec=30):
        self.db.delete_all()

    def get_status(self):
        status = {"type": self.db.get_type_counts(), "status": self.db.get_status_counts(), "last": self.db.get_last_jobs(limit=10), "type_status": self.db.get_type_status_counts()}
        return status

    def process(self):
        if not self.execute_one_cron_item():
            # Put a status
            # if not self.last_status_time or (datetime.now() - self.last_status_time).total_seconds() > 10.0:
            # 	self.print_status()
            # Lets not get stuck in a loop!
            time.sleep(1)
