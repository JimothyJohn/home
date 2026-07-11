#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# Display help information
if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    echo 'Usage: Update.sh'
    exit 0
fi

main() {
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            *)
                echo "Unknown parameter passed: $1"
                exit 1
                ;;
        esac
        shift
    done

    aws s3 cp docs s3://uplink-website --recursive --acl public-read
}

main "$@"
