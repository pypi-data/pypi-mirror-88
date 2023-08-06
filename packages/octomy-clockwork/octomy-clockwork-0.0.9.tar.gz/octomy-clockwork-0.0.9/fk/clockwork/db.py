import json
import os
import sqlite3
import pprint
import psycopg2
import psycopg2.extras
import traceback
import sys
import pytz
import logging
from flask import g

from fk.db.DatabaseConnection import DatabaseConnection


logger = logging.getLogger(__name__)


class Database:
    def __init__(self, config):
        self.config = config
        self.dbc = DatabaseConnection.get_connection(self.config)
        assert self.dbc.is_ok()
        self.create_tables()

    def create_tables(self):

        # Create a table to keep track of crons
        self.dbc.query_none(
            """
			create table if not exists "clockwork_crons" (
				id serial primary key,
				name varchar(31),
				spec text,
				command varchar(255),
				arguments text, 
				enabled boolean not null default true,
				run_count bigint not null default 0, 
				last_run_at timestamptz not null default now(),
				created_at timestamptz not null default now(),
				updated_at timestamptz not null default now()
			);
			comment on column clockwork_crons.id is 'Unique internal id for this cron';
			comment on column clockwork_crons.name is 'The cron''s name.';
			comment on column clockwork_crons.spec is 'The cron''s time specification.';
			comment on column clockwork_crons.command is 'The cron''s command to execute.';
			comment on column clockwork_crons.arguments is 'The cron''s command arguments.';
			comment on column clockwork_crons.last_run_at is 'When the cron was last run';
			comment on column clockwork_crons.created_at is 'When the cron was first created';
			comment on column clockwork_crons.updated_at is 'When cron item was last updated';
			"""
        )

    # Insert a new cron into
    def upsert_cron(self, cron):
        return self.dbc.query_one(
            """
				insert into clockwork_crons
					(
					name,
					spec,
					command,
					arguments, 
					enabled,
					run_count,
					last_run_at
					)
				values
					(
					%(name)s,
					%(spec)s,
					%(command)s,
					%(arguments)s,
					%(enabled)s,
					%(run_count)s,
					%(last_run_at)s
					)
				on conflict(id)
				do update
					set
					name=%(name)s,
					spec=%(spec)s,
					command=%(command)s,
					arguments=%(arguments)s,
					enabled=%(enabled)s,
					run_count=%(run_count)s,
					last_run_at=%(last_run_at)s,
					updated_at=now()
				returning id
				;
				""",
            cron,
        )

    # Register a new cron execution
    def log_cron_run(self, id):
        return self.dbc.query_one(
            """
				update
					clockwork_crons
				set
					run_count = run_count + 1,
					last_run_at = now(),
					updated_at = now()
				where
					id = %(id)s
				returning
					updated_at
				;
				""",
            {"id": (id,)},
        )

    # Update a cron with a new enabled state
    def set_cron_enabled(self, id, enabled=True):
        return self.dbc.query_one(
            """
                update
                    clockwork_crons
                set
                    enabled = %(enabled)s
                    updated_at = now()
                where
                    id = %(id)s
                returning
                    updated_at
                ;
                """,
            {"id": (id,), "enabled": (enabled,)},
        )

        # Delete cron with given id

    def delete_cron_with_id(self, cron_id):
        self.dbc.query_none(
            """
				delete from clockwork_crons
				where id=%(cron_id)s,
				;
				""",
            {"cron_id": (cron_id,)},
        )

    # Clear out the crons table
    def delete_all(self):
        return self.dbc.query_none(
            """
				delete from clockwork_crons
				;
				"""
        )

    # Get crons from cron list fitting the optional filter
    def get_crons(self, id=None, name=None, spec=None, command=None, arguments=None, enabled=None, run_count=None, last_run_at=None, limit=1):
        return self.dbc.query_many(
            """
				select
					id,
					name,
					spec,
					command,
					arguments, 
					enabled,
					run_count,
					last_run_at,
					created_at,
					updated_at
				from
					clockwork_crons
				where
					true
				and
					(%(id)s is null or id = any(%(id)s))
				and
					(%(name)s is null or name = any(%(name)s))
				and
					(%(spec)s is null or spec = any(%(spec)s))
				and
					(%(command)s is null or command = any(%(command)s))
				and
					(%(arguments)s is null or arguments = any(%(arguments)s))
				and
					(%(enabled)s is null or enabled = any(%(enabled)s))
				and
					(%(run_count)s is null or run_count = any(%(run_count)s))
				and
					(%(last_run_at)s is null or last_run_at = any(%(last_run_at)s))
				order by
					last_run_at asc
				limit
					%(limit)s
				;
				""",
            {"id": (id,), "enabled": (enabled,), "name": (name,), "spec": (spec,), "command": (command,), "arguments": (arguments,), "run_count": (run_count,), "last_run_at": (last_run_at,), "limit": (limit,)},
        )

    # Get cron by id from cron list
    def get_cron_by_id(self, id):
        return self.dbc.query_one(
            """
				select
					id,
					name,
					spec,
					command,
					arguments, 
					enabled,
					run_count,
					last_run_at,
					created_at,
					updated_at
				from
					clockwork_crons
				where
					id = %(id)s
				order by
					updated_at asc
				limit
					1
				;
				""",
            {"id": (id,)},
        )

    def get_now(self):
        r = self.dbc.query_one(
            """
				select now()
			;"""
        )
        if not r:
            return None
        r = r.get("now")
        if not r:
            return None
        # logger.info(r)
        r = r.replace(tzinfo=pytz.UTC)
        return r


# What is this shit you ask? Gotta love python.... https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
def get_flask_clockwork_db(config) -> Database:
    if "clockwork_database" not in g:
        g.clockwork_database = Database(config)
    return g.clockwork_database


def close_flask_clockwork_db(e=None):
    clockwork_database = g.pop("clockwork_database", None)

    if clockwork_database is not None:
        del clockwork_database
