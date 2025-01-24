# sieci
Do kompilacji projektu wymagane biblioteki SQLite i cJSON: \

sudo apt install libsqlite3-dev
sudo apt install libcjson-dev

lub dostępne pod linkami:

https://github.com/DaveGamble/cJSON

https://github.com/sqlite/sqlite

serwer: gcc server.c -o server -lsqlite3 -lcjson
klient: python3 gui.py

