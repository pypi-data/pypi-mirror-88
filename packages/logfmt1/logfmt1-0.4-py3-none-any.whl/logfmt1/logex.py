#!/usr/bin/env python3
# encoding: utf-8
# title: logex
# description: extract fields from log (with .fmt)
# version: 0.2
# type: cli
# category: extract
#
#
# First parameter should be the log file. And a .log.fmt must exist
# alongside (generate with `update-logfmt`).
#
# Syntax:
#   logex.py /var/log/apache2/access.log  request_path  request_time  @host
#
# Other args:
#   --json / --tab / --csv
#   --iso8601 / --debug
#
# Where any @'s are decoration, and fields can be supplied as individual
# arguments (become space-separated without --tab/--csv). Field names are
# application-type specific (internal) names. (E.g. @request_method, @host
# or @tm_wday for Apache logs. With some predefined aliases, e.g. the w3c
# extended log field names.)
#
# Field name prefixes are irrelevant for normal log entries.
# But may join list-entries from container fields:
#    @name   will just show the first entry
#    %name   space-separated list
#    *name   comma-separated list
#    +name   plus-joined list
#    #name   as json array
#     name   whatever
#
# Fields can be given as individual arguments, or as part of a string
# output groups:
#    logex fn.log --tab  @individual "@combined,@with,@comma" @tabagain
#    logex fn.log --csv  "@lone" "*multi" "#json"
# Though you usually don't wanna overcomplicate the log format again.
#


import sys, re, json
import traceback, dateutil.parser
try:
    import logfmt1
except:
    from modseccfg import logfmt1


#-- args
argv = sys.argv
space = " "
if "--tab" in argv:
    space = "\t"
if "--csv" in argv:
    space = "," 
iso8601 = any(a in argv for a in ("--iso", "--iso8601", "--date", "--fixdates", "--die-apachedateformat-die"))
as_json = any(a in argv for a in ("--json", "--asjson", "--as-json"))
dodebug = any(a in argv for a in ("--debug", "-D"))
# remove --params
argv = [a for a in argv if not re.match("^--\w+$|^-\w$", a)]
# filename and field list
log_fn = argv[1]
output_fields = space.join(argv[2:])


#-- open log file
try:
    reader = logfmt1.logopen(log_fn, debug=dodebug, duplicate=False)
    #if dodebug:
    #    sys.stdout.write(json.dumps(reader.__dict__, indent=2, default=lambda x:str(x))+"\n")
except Exception as e:
    sys.stderr.write(traceback.format_exc()+"\n")
    sys.stderr.write("Use `update-logfmt-apache` or modseccfg→File→Install→update_logfmt to generate a .fmt descriptor\n")
    sys.exit()


# extra aliases (for apache/httpd)
alias = {
    "time": "request_time",
    "bytes": "bytes_sent",
    "ip": "remote_addr",
    "c-ip": "remote_addr",
    "dns": "server_name",
    "status": "status",
    "method": "request_method",
    "uri": "request_path",
    "url": "request_path",
    "path": "request_path",
    "uri-stem": "request_path",
    "uri-query": "request_query",
}
alias.update(reader.alias)


# substitute occurences
def get_field(m, row):
    pfx, name = m.groups()
    val = row.get(name) or row.get(alias.get(name)) or "-"
    if isinstance(val, list):  # how to handle lists (for unpacked [key "value"] fields)
        if pfx == "@":
            val = val[0]
        elif pfx == "+":
            val = "+".join(val)
        elif pfx == "%":
            val = " ".join(val)
        elif pfx == "*":
            val = ",".join(val)
        elif pfx == "#":
            val = json.dumps(val)
        else:
            val = str(val)
    return val


# loop over lines, and output selection
for row in reader:

    if not row:
        row = {}
    if iso8601:
        for key in ["date", "request_time", "datetime"]:
            if key in row:
                # the […] wrapping should already be gone at this point
                row[key] = dateutil.parser.parse(row[key].strip("[]"))
    if as_json:
        print(
            json.dumps(row)
        )
    else:
        print(
            re.sub("([@+*#%]?)([\w\-]+)", lambda m: get_field(m, row), output_fields)
        )

