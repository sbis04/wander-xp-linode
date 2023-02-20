#!/bin/bash
export DB_PASSWORD="$1"
export OBJECT_STORAGE_KEY_ID="$2"
export OBJECT_STORAGE_KEY_SECRET="$3"

g_pid=$GUNICORN_PROCESS_ID
a_pid=$APP_PROCESS_ID

if [ -z g_pid ]
then
    echo "No GUNICORN_PROCESS_ID set!"
else
    kill $g_pid &
fi

if [ -z a_pid ]
then
    echo "No APP_PROCESS_ID set!"
else
    kill $a_pid &
fi

sleep 5
echo " "
echo "========================"
echo "Starting WanderXP API"
echo "========================"
echo " "

cd "/root/Python_Linode_app"
gunicorn -w 3 app:app & echo "GUNICORN_PROCESS_ID: $!"
export GUNICORN_PROCESS_ID=$!
sleep 5
python3 app.py & echo "APP_PROCESS_ID: $!"
# export GUNICORN_PROCESS_ID=$gunicorn_process_id
export APP_PROCESS_ID=$!
sleep 2
echo " "
echo "========================"
echo "WanderXP API Running..."
echo "[ Re-running it will stop these processes ]"
echo "========================"
echo " "
