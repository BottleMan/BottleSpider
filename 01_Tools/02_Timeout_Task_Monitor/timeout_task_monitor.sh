#!/bin/bash

function kill_timeout_process()
{
    pid=$1
    max_time=$2
    start_time=$(cat /proc/$pid/stat | cut -d" " -f22)

    if [[ "$start_time" == "" ]]
    then
        echo "[$pid] not exists."
        return 0
    fi

    user_hz=$(getconf CLK_TCK)
    sys_uptime=$(cat /proc/uptime | cut -d" " -f1)

    runs_time=$(( ${sys_uptime%.*} - $start_time/$user_hz ))

    echo "[$pid] runs for $runs_time seconds."

    if [ "$runs_time" -ge "$max_time" ]
    then
        echo "[$pid] killed."
        kill -9 $pid
    fi

    return 1
}

process_name="scrapy"
timeout=7200

for pid in `pgrep $process_name`
do
    kill_timeout_process $pid $timeout
done