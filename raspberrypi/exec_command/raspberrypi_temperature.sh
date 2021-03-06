#! /bin/bash
BASE_DIR="/usr/local/project/raspberrypi_video/raspberrypi/exec_command/"
SCRIPT_NAME="get_temperature.py"
SCRIPT_PATH=$BASE_DIR$SCRIPT_NAME
CHANNEL=29

start() {
    cd $BASE_DIR
    [ -f $SCRIPT_PATH ] || exit 5
	pids=`ps -aux|grep $SCRIPT_NAME|grep -v grep|awk '{print $2}'`
    if [ ! ${pids} ];then
		nohup python $SCRIPT_PATH -c $CHANNEL > /dev/null 2>&1 &
		retval=$?
		echo start $SCRIPT_NAME success
	else
	    echo $SCRIPT_NAME is running
	    retval=0
	fi
	return $retval
}
stop() {
    PID=$(ps -aux|grep $SCRIPT_NAME|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID}
    if [ $? -eq 0 ];then
        echo kill $SCRIPT_NAME success
    else
        echo kill $SCRIPT_NAME fail
    fi
}
restart() {
    stop
    sleep 1
    start
}
watch_dog(){
    pids=`ps -aux|grep $SCRIPT_NAME|grep -v grep|awk '{print $2}'`
    if [ ${pids} ];then
        echo $SCRIPT_NAME is running
    else
        start
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    watchdog)
        watch_dog || exit 0
        ;;
    *)
        echo $"Usage: $0 {start|stop|watchdog}"
        exit 2
esac
