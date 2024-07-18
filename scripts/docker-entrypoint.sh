#!/usr/bin/env bash

set -e

hatch run alembic upgrade head
exec hatch run python -O -m bot
