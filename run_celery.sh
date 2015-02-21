#!/bin/bash
celery -A task_simple worker --loglevel=info
