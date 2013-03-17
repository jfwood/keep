#!/bin/bash

# keep_web_init.sh - Use uwsgi to run Cloud Keep python and wsgi web app.
#
# chkconfig: - 85 15
# description: Use uwsgi to run Cloud Keep python and wsgi web app.
# processname: keep_init.sh

PATH=/opt/uwsgi:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/opt/uwsgi/uwsgi
VENV=vkeep

OWNER=cloud_keep

NAME=keep_init
DESC=Cloud Keep start script (web-node)
CONF_FILE=/etc/default/keep_web_init.ini


test -x $DAEMON || exit 0

# Include cloud keep defaults if available
if [ -f /etc/default/keep_web_init.conf ] ; then
	. /etc/default/keep_web_init.conf
fi

set -e

get_pid() {
    if [ -f /var/run/$daemon_name.pid ]; then
        echo `cat /var/run/$daemon_name.pid`
    fi
}   

#DAEMON_OPTS="-s 127.0.0.1:9001 -M 4 -t 30 -A 4 -p 4 -d /var/log/keep_web.log --pidfile /var/run/$NAME.pid --pythonpath $PYTHONPATH --module $MODULE"
DAEMON_OPTS="-H $VENV --ini $CONF_FILE"

case "$1" in
  start)
	echo -n "Starting $DESC: "
        PID=$(get_pid)
        if [ -z "$PID" ]; then
            [ -f /var/run/$NAME.pid ] && rm -f /var/run/$NAME.pid

            touch /var/run/$NAME.pid                                         
            chown $OWNER /var/run/$NAME.pid
	    su - $OWNER -pc "source /usr/local/bin/$VENV/bin/activate"
	    su - $OWNER -pc "$DAEMON $DAEMON_OPTS"
	    echo "$NAME."
        fi

	;;
  stop)
	echo -n "Stopping $DESC: "
        PID=$(get_pid)
        [ ! -z "$PID" ] && kill -s 3 $PID &> /dev/null
        if [ $? -gt 0 ]; then
            echo "was not running" 
            exit 1
        else 
	    echo "$NAME."
            rm -f /var/run/$NAME.pid &> /dev/null
	    su - $OWNER -pc "deactivate"            
        fi
	;;
  reload)
        echo "Reloading $NAME" 
        PID=$(get_pid)
        [ ! -z "$PID" ] && kill -s 1 $PID &> /dev/null
        if [ $? -gt 0 ]; then
            echo "was not running" 
            exit 1
        else 
	    echo "$NAME."
            rm -f /var/run/$NAME.pid &> /dev/null
        fi
	;;
  force-reload)
        echo "Reloading $NAME" 
        PID=$(get_pid)
        [ ! -z "$PID" ] && kill -s 15 $PID &> /dev/null
        if [ $? -gt 0 ]; then
            echo "was not running" 
            exit 1
        else 
	    echo "$NAME."
            rm -f /var/run/$NAME.pid &> /dev/null
        fi
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
	;;
  status)  
	killall -10 $DAEMON
	;;
      *)  
	    N=/etc/init.d/$NAME
	    echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
	    exit 1
	    ;;
    esac
    exit 0
