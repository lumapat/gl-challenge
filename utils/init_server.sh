#!/bin/bash

./setup_db.sh
uvicorn loansvc.main:app --host 0.0.0.0 --port 8000