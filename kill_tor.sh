ps -ef | grep tor| awk '{print $2}' | xargs kill -9
