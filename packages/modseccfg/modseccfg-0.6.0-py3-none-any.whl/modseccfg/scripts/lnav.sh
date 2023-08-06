#!/bin/sh
# title: lnav
# description: log viewer
# type: filter
# category: viewer
# params: {logfn}

x-terminal-emulator -e "lnav $1"
