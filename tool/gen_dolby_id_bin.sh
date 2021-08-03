 #!/bin/bash

EXEC_BASEDIR=$(dirname $(readlink -f $0))

#
# Settings
#
VERSION=0.1

usage() {
    cat << EOF
Usage: $(basename $0) --help
       $(basename $0) --version
       $(basename $0) --id dolby_customer_id_value -o dolby_id.bin
EOF
    exit 1
}

function append_uint32_le() {
    local input=$1
    local output=$2
    local v=
    local vrev=
    v=$(printf %08x $input)
    # 00010001
    vrev=${v:6:2}${v:4:2}${v:2:2}${v:0:2}

    echo $vrev | xxd -r -p >> $output
}

function gen_dolby_id_bin() {
    local argv=("$@")
    local i=0
    local dolby_id=0
    # Parse args
    i=0
    while [ $i -lt $# ]; do
        arg="${argv[$i]}"
        #echo "i=$i argv[$i]=${argv[$i]}"
        i=$((i + 1))
        case "$arg" in
            --id)
                dolby_id_value="${argv[$i]}" ;;
            -o)
                output="${argv[$i]}" ;;
            *)
                echo "Unknown option $arg"; exit 1
                ;;
        esac
        i=$((i + 1))
    done

    if [ -z $dolby_id_value ]; then
        echo Error: invalid dolby_id_value
        exit 1
    fi

    if [ -z $output ]; then
        echo Error: invalid output
        exit 1
    fi

    append_uint32_le $dolby_id_value $dolby_id
    dd if=$dolby_id of=$output bs=1 count=4 conv=notrunc >& /dev/null

    rm -f $dolby_id
    echo generate $output success
}

parse_main() {
    case "$@" in
        --help)
            usage
            ;;
        --version)
            echo "$(basename $0) version $VERSION"
            ;;
        *--id*)
            gen_dolby_id_bin "$@"
            ;;
        *)
            usage "$@"
            ;;
    esac
}

parse_main "$@"
