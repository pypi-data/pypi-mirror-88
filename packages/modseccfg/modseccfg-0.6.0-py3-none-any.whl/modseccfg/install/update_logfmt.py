# api: modseccfg
# title: craft *.log.fmt
# description: record current log formats
# type: internal
# category: update
# version: 0.1
#
# Create a *.fmt descriptor for each Apache *.log


import re, json
from modseccfg import vhosts, writer
from modseccfg.vhosts import tmp
from modseccfg.utils import conf, log, srvroot


print("# Doesn't really create anything\n# Just an experiment at the moment\n")


# traverse log files, create .fmt descriptor with current format string
for fn,ty in tmp.log_map.items():

    fn_fmt = f"{fn}.fmt"
    fmt_record = tmp.log_formats.get(ty)
    if not fmt_record:
        continue
    
    j = {}
    if srvroot.exists(fn_fmt):
        try:
            j = json.loads(srvroot.read(fn_fmt))
        except:
            print(f"WARN: {fn_fmt} contained invalid json")
            continue
    if not "class" in j:
        j["class"] = f"apache {ty}"
    if not "record" in j or j["record"] != fmt_record:
        j["record"] = fmt_record
        
    # add descriptors for known placeholders
    if not "fields" in j or True:
        j["fields"] = { k: '{"id":"??", "rx":"\S+"}' for k in re.findall("%[\{\w\-\}]+", fmt_record)}
    # prebuilt-regex (like lnav)
    if not "regex" in j or True:
        pass

    print(f"→ {fn_fmt}")
    print(json.dumps(j, indent=4))
    #srvroot.write(fn_fmt, json_dumps(j, indent=4))

