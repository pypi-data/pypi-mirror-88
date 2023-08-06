#!/bin/sh
# title: access.log last 24hs
# type: image
# category: report
# params: {logfn}

. $(dirname $0)/aliases.sh

DATE=$(LANG=C date "+%b %d")
grep "$DATE" "$1" | altimestamp | cut -d: -f1 | sort | uniq -c | arbigraph -o /tmp/stdout.png -w 1000 -H 800

