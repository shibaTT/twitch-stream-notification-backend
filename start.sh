#!/bin/sh
poetry install
poetry run python3 database/create_db.py
# バックグランドプロセスを使って並行起動
poetry run python3 index.py &
poetry run python3 main.py &
# 待ってあげないとシェルスクリプトが終了しちゃう
wait
