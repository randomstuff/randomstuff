A collection of simple programs/scripts which I found useful at some point
but which do not deserve a repository on their own.

## Design goals

Minimal number of dependencies:

* favor builtin dependencies;
* eg. `argparse` instead of `click`;
* try to use dependencies which are already packaged in your standard Linux distro;
* try to keep compatibility with different versions of the libraries.

Interface:

* the CLI interface may not be completely stable;
* some programs may have very limited CLI handling.

Simplicity:

* try to keep the code simple, easy to modify and repurpose for other purpose.

## Partial list of tools

### Admin

`admin/`:

* `gnt-instance-vnc-connect.py`, open a RDP connection to a Ganeti instance from a Ganeti node

### CMS

`content/`:

* `joomla_to_wordpress_redirect.rb`, generate redirections for a Joomla to WordPress migration.

### Content

`content/`:

* `cleanup_html.rb`, cleanup HTML snippet

### Data

`data/`:

* `accesslog2jsonl.py`, parse `access.log` (HTTP server) logs into JSON line entries
* `cbor2json.py` convert CBOR to JSON
* `decode-hc1-covid-certificate`, decode a HC1 COVID certificate
* `fods2html.xsl`, XSLT stylesheet to convert OpenDocument plain XML spreadsheets (`.fods`) into HTML
* `grexpath.rb`, like grep buth with XPATH expression
* `json2cbor.py`, convert JSON to CBOR
* `json2msgpack.py`, convert JSON to MessagePack
* `json2yaml.py`, convert JSON to YAML
* `ltsv2jsonl.py`, convert [LTSV](http://ltsv.org/) (labelLabeled Tab-separated Values) to JSON lines
* `msgpack2json.py`, convert MessagePack to JSON
* `re2jsonl.py`, convert lines int JSON based on one or more regular expressions
* `splitasciiarmor.py`, split ASCII Armor (or PEM) files into multiple files
* `tsv2html.sed`, convert TSV to HTML `<table>`
* `yaml2json.py`, convert YAML to JSON
* `zlibcat.py`, decompress raw zlib (like `zcat` and friends)

### Desktop

`desktop/`:

* `global-stopwatch.py`, desktop stopwatch based on global keybindings.
* `gui_filter.sh`, filter the content of the clipboard/selection through a UNIX command
* `keybinder.py`, execute a program when a global keyboard shortcut is triggered
* `ocrjpn.sh`, OCR a selection of the screen in order to extract Japanese characters
* `take-screenshot.sh`, take a screenhot
* `which-theme.sh`, which themes are available in both GTK2 and GTK3?
* `xrandr-helper.sh`, helper for xrandr
* `xsettings-query.py`, dump XSETTINGS
* `zbarflash.sh`, parse QR code from a selection of the screen

### Desktop and sound

`desktop/sound/`:

* `pulse-mute-toggle.py`, toggle PulseAudio default source mute with desktop notification
* `pulse-toggle-output.py`, toggle default PulseAudio output
* `pushtotalk.py`, push-to-talk using PulseAudio

### Development

`dev/`:

* `compile_commands/gen_compile_commands.rb`, generat a `compile_commands.json` from a set of rules (for helping tooling integration);

### Profiling

`dev/profiling/`:

* `aggregate-counts.py`
* `megalopoll.py`, polling command, simple building block for Poor man's profiling
* `pmp.sh`, [Poor-man's profiler](https://poormansprofiler.org/) implementation 
* `stackcollapse-jstack.py`, collapse Java stacks from `jstack` and `jcmd` for [FlameGraph](https://github.com/brendangregg/FlameGraph)

For SQL:

* `pmp-mysql.sh`, [Poor-man's profiler](https://poormansprofiler.org/) for MySQL and MariaDB requests
* `normalize-sql.py`, normalize SQL requests (useful for aggregation)

### Devices

`device/`:

* `feel-my-power.py`, display notification about battery status of devices (eg. for wireless gamepad) using upower

### Disk

`disk/`:

* `mount-diskimage.py`, mount an image (ISO) using udisks2
* `xdg-open-diskimage.sh`

### Misc

`misc/`:

* `sleep-exponential.py`, like `sleep` with following an exponential distribution

### Network

`network/`:

* `ipls.py`, list IP addresses in a subnet
* `rmcp-discover.py`, discover RMCP nodes (such as AMT or IPMI) on the LAN
* `ssdp-listen.py`, listen for SSDP announces and dump responses
* `ssdp-search.py`, launch a SSDP search request and dump responses
* `upnp-display-interfaces.py`, display human friendly description of some UPnP service

## Security

`security/`:

* `memexec.py`, execute a program from a pipe, etc. without writing the file to any filesystem.

## SSH

`ssh/`:

* `list-ssh-hosts.py`, lists known SSH hosts
* `ssh-menu.sh`, TUI menu for opening a shell on a chosen SSH host

## System

`system/`:

* `fdpass/fdpass.py`, pass a file descriptor over STDOUT
* `fdpass/fdrcv-test.py`, receive a file descriptor from `fdpass.py`
* `seccompstuff/nonetwork.c`, disable networking system calls using seccomp-bpf
* `procdump.py`, dump a process memory without stopping it
* `socket-activate.py`, systemd-style (LISTEN_FDS) socket activation (like systemd-socket-activate)
* `socket-listen-inetd.py`, LISTEN_FDS/inetd bridge

## Websites

Interaction with known web sites/services (`websites/`):

* `github-api.py`, CLI for Github API
