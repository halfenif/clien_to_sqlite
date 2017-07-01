ps -ef | grep __ReloadTorrcOnSIGHUP| awk '{print $2}' | xargs kill -9
