ps -ef | grep python3 | awk '{print $2}' | xargs kill -9
ps -ef | grep __ReloadTorrcOnSIGHUP| awk '{print $2}' | xargs kill -9
