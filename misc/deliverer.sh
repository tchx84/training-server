#!/bin/bash
if [ "`pgrep -fx /bin/bash\ /opt/training/misc/deliverer.sh`" = "$$" ]; then
    /usr/bin/python /opt/training/deliverer.py
fi
