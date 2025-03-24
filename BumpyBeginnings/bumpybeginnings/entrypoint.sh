#!/bin/sh

# run database migrations
python manage.py migrate --noinput

# load data into the database
python manage.py loaddata ./startingData/auth_user_data.json
python manage.py loaddata ./startingData/site_user_data.json
python manage.py loaddata ./startingData/forums_data.json
python manage.py loaddata ./startingData/posts_data.json
python manage.py loaddata ./startingData/comments_data.json
python manage.py loaddata ./startingData/votes_data.json
python manage.py loaddata ./startingData/atomic_data.json

exec "$@"