#!/bin/bash

uvicorn app.chat:app \
    --reload \
    --port 8080 \
    --host 0.0.0.0 \
    --host '::'
