A collection of simple programs/scripts which I found useful at some point
but which do not deserve a repository on their own

Admin (`admin/`):

* `gnt-instance-vnc-connect`, open a RDP connection to a Ganeti instance from a Ganeti node

CMS (`cms/`):

* `joomla_to_wordpress_redirect`, generate redirections for a Joomla to WordPress migration.

Content:

* `cbor2json` convert CBOR to JSON
* `cleanup_html`, cleanup HTML snippet
* `fods2html.xsl`, convert OpenDocument plain XML spreadsheets (.fods) into HTML
* `grexpath`, like grep buth with XPATH expression
* `json2cbor`, convert JSON to CBOR
* `json2msgpack`, convert JSON to MessagePack
* `json2yaml`, convert JSON to YAML
* `msgpack2json`, convert MessagePack to JSON
* `splitasciiarmor`, split ASCII Armor (or PEM) files into multiple files
* `tilt-render`, CLI for Ruby Tilt
* `tsv2html`, convert TSV to HTML `<table>`
* `yaml2json`, convert YAML to JSON
* `decode-hc1-covid-certificate`, decode a HC1 COVID certificate
* `zlibcat`, decompress raw zlib

Desktop (`desktop/`)

* `gui_filter`, filter the content of the clipboard/selection through a UNIX command
* `keybinder`, execute a program when a global keyboard shortcut is triggered
* `take-screenshot`, take a screenhot
* `which-theme`, which themes are available in both GTK2 and GTK3?
* `xrandr-helper`, helper for xrandr
* `xsettings-query`, dump XSETTINGS

Desktop sound (`desktop/sound`):

* `pulse-mute-toggle`, toggle PulseAudio default source mute with desktop notification
* `pushtotalk`, push-to-talk using PulseAudio
* `pulse-toggle-output`, toggle default output

Devices (`device/`):

* `feel-my-power`, display notification about battery status of devices (eg. for wireless gamepad) using upower

Disk (`disk/`):

* `mount-diskimage`, mount an image (ISO) using udisks2
* `xdg-open-diskimage`

Misc (`misc/`):

* `askpass`
* `sleep-exponential`, like `sleep` with following an exponential distribution

Network (`network`/):

* `rmcp-discover`, discover RMCP nodes (such as AMT or IPMI) on the LAN
* `ssdp-listen.py`, listen for SSDP announces and dump responses
* `ssdp-search.py`, launch a SSDP search request and dump responses
* `upnp-display-interfaces.py`, display human friendly description of some UPnP service
* `ipls`, list IP addresses in a subnet

System (`system/`):

* `fdpass`, pass a file descriptor over STDOUT
* `seccompstuff/nonetwork`, disable networking system calls using seccomp-bpf
* `procdump`, dump a process memory without stopping it
* `socket-activate`, systemd-style (LISTEN_FDS) socket activation (like systemd-socket-activate)
* `socket-listen-inetd`, LISTEN_FDS/inetd bridge

Interaction with known web sites/services (`websites/`):

* `github-api`, CLI for Github API
