#!/bin/bash
# Dial telephone numbers using DTMF and a sound card.

# - Register with firefox by adding network.protocol-handler.expose.tel=false in about:config.

# Configuration
national_cc=33
national_prefix="0"
international_prefix="00"

# Flags:
confirm=false

dial_about() {
    cat <<EOF >&2
dtmf-dialer: dial telephone numbers using DTMF and a sound card.

Basic usage:
 dtmf-dialer 3131
 dtmf-dialer +33987654321
 dtmf-dialer tel:3131
 dtmf-dialer tel:+33987654321

Interactive usage (currently GUI with zenity):
 dtmf-dialer --confirm 3131
 dtmf-dialer --ask
EOF
}

dial_number() {
    d="$1"
    case "$d" in
	1 | 2 | 3 | A | a)
	    f1=697
	    ;;
	4 | 5 | 6 | B | b)
	    f1=770
	    ;;
	7 | 8 | 9 | C | c)
	    f1=852
	    ;;
	'*' | 0 | '#' | D | d)
	    f1=941
	    ;;
    esac
    case "$d" in
	1 | 4 | 7 | '*')
	    f2=1209
	    ;;
	2 | 5 | 8 | 0)
	    f2=1336
	    ;;
	3 | 6 | 9 | '#')
	    f2=1477
	    ;;
	A | a | B | b | C | c | D | d)
	    f2=1633
	    ;;
    esac
    play -n synth 0.1 sin $f2 sin $f1 gain -10 remix -
    sleep 0.02    
}

dial_numbers() {
    echo "Dialing $1" >&2
    tel="$1"
    i=0
    while (( i<${#tel} )) ; do
	d=${tel:$i:1}
	case "$d" in
	    0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | A | B | C | D)
		dial_number "$d"
		;;
	esac
	(( i=$i+1 ))
    done
}

dial_prefixed() {
    a=$1
    if $confirm ; then
	a=$(ask_number "$1") || return
    fi
    case "$a" in
    +"$national_cc"*)
	dial_numbers "$national_prefix$(echo "$a" | sed s/^+$national_cc//)"
	;;
    +*)
	dial_numbers "$international_prefix$(echo "$a" | sed s/^+//)"
	;;
    *)
	dial_numbers "$a"
	;;
    esac
}

ask_number() {
    zenity --entry --title="Dial number" --text="Dial number:" --entry-text="$1"
}

dial_tel_uri() {
    number="$(echo "$1" | sed -e 's/^tel://' -e 's/;.*//')"
    dial_prefixed "$number"
}


for a in "$@"; do
    case "$a" in
	--about | --help)
	    dial_about
	    exit 0
	    ;;
	--confirm)
	    confirm=true
	    ;;
	--ask)
	    number=$(ask_number) || continue
	    dial_tel_uri "$number"
	    ;;
	-* | --*)
	    echo "Unrecognised option" >&2
	    exit 1
	    ;;
	tel:*)
	    dial_tel_uri "$a"
	    ;;
	*)
	    dial_prefixed "$a"
	    ;;
    esac
done
