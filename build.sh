#!/usr/bin/env bash

source .env
poetry install && psql -a -d $DATABASE_URL -f database.sql