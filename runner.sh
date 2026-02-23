#!/bin/sh
# Shell script used to start up FastAPI for local development and testing
#
# Requires a virtual environment (venv) created as venv and all
# dependencies installed.

venv/bin/uvicorn app.main:app --reload
