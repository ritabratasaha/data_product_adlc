#!/usr/bin/env python3
"""Verify connectivity to Supabase PostgreSQL."""

import os
import sys

import psycopg2

REQUIRED_ENV = ("POSTGRES_HOST", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB")


def main() -> int:
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        print(
            f"Missing required environment variables: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 1

    host = os.environ["POSTGRES_HOST"]
    port = int(os.environ.get("POSTGRES_PORT", "5432"))
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    dbname = os.environ["POSTGRES_DB"]
    sslmode = os.environ.get("POSTGRES_SSLMODE", "require")

    try:
        with psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
            sslmode=sslmode,
            connect_timeout=10,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("select 1 as ok")
                row = cur.fetchone()
                if row is None or row[0] != 1:
                    raise RuntimeError(f"Unexpected probe query result: {row}")
    except Exception as exc:
        print(
            f"Could not connect to PostgreSQL at {host}:{port}/{dbname}.\n"
            f"Error: {exc}",
            file=sys.stderr,
        )
        return 1

    print(f"Connected to PostgreSQL at {host}:{port}/{dbname}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
