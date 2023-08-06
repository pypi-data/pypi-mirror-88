from fk.clockwork.processor import Processor, parse_schedule
from fk.batch.BatchProcessor import BatchProcessor

import schedule
import fk.clockwork.cron
from functools import partial
import time
import logging

logger = logging.getLogger(__name__)


class Server:
    def __init__(self, config):
        self.config = config
        self.processor = Processor(self.config)
        self.batch_processor = BatchProcessor(self.config)
        self.crons_by_id = {}
        logger.info("Clockwork server initialized")

    def job_inserter(self, command, arguments=""):
        # logger.info(f"INSERTING JOB {command}({arguments})")
        if "dummy" in command:
            logger.info(f"Skipping insertion of dummy job {command}({arguments})")
        else:
            self.batch_processor.insert_batch_item(type=command, data=arguments, priority=50, source="clockwork")

    def register_schedule(self):
        # logger.info("Clockwork registering schedules")
        raw_crons = self.processor.get_crons()
        for raw_cron in raw_crons:
            do_register = False
            id = raw_cron.get("id")
            name = raw_cron.get("name")
            spec = raw_cron.get("spec")
            enabled = raw_cron.get("enabled")
            command = raw_cron.get("command")
            arguments = raw_cron.get("arguments")
            if id in self.crons_by_id:
                prev = self.crons_by_id[id]
                prev_name = prev.get("name")
                prev_spec = prev.get("spec")
                prev_command = prev.get("command")
                prev_enabled = prev.get("enabled")
                prev_arguments = prev.get("arguments")
                if prev_spec != spec:
                    logger.warning(f"Spec changed from '{prev_spec}' to '{spec}'")
                    do_register = True
                if prev.get("enabled") != enabled:
                    logger.warning(f"Enabled changed from '{prev_enabled}' to '{enabled}'")
                    do_register = True
                if prev.get("command") != command:
                    logger.warning(f"Command changed from '{prev_command}' to '{command}'")
                    do_register = True
                if prev.get("arguments") != arguments:
                    logger.warning(f"Arguments changed from '{prev_arguments}' to '{arguments}'")
                    do_register = True
                if do_register:
                    if enabled:
                        logger.info(f"Clockwork unregistering disabled schedule '{name}'")
                    else:
                        logger.info(f"Clockwork re-registering schedule '{name}'")
                    schedule.clear(id)
            else:
                if enabled:
                    logger.info(f"Clockwork registering schedule '{name}'")
                    do_register = True
            if do_register and enabled:
                job = partial(self.job_inserter, command, arguments)
                actual_schedule = parse_schedule(spec, job, id)
                if not actual_schedule:
                    logger.error(f"Could not register schedule: {name}")
                    continue
                self.crons_by_id[id] = raw_cron

    # Start server and serve until it is aborted
    def run(self):
        logger.info("Clockwork server started")
        while True:
            self.register_schedule()
            schedule.run_pending()
            time.sleep(1)
