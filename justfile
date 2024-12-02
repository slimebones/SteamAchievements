set shell := ["nu", "-c"]
set dotenv-load

run:
    @ python -m server --host 0.0.0.0 --port 3000
