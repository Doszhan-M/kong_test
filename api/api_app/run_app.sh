#!/bin/bash


if [ "$DEPLOY" = "TRUE" ]; then
    echo "Running deploy"
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 3 
else
    echo "Running test"
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 --reload 
    # gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 проблемы с CORS
fi