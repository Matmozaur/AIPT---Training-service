FROM python:3.12-slim

WORKDIR /app

# Prepare venv
RUN	make -e REQUIREMENTS_FILE=requirements.txt VENV=venv make_env

COPY ./app /app

CMD ["venv/bin/python", "main.py"]
