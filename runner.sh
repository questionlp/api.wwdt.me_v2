#!/bin/sh
# Shell script used to start up FastAPI for local development and testing

. venv/bin/activate
uvicorn app.main:app --reload
