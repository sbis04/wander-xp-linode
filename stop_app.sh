#!/bin/bash
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

sleep 2
echo " "
echo "========================"
echo "Stopped WanderXP API"
echo "========================"
echo " "