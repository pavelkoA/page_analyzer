#!/usr/bin/env bash

poetry install && psql -a -d $DATABASE_URL -f database.sql