#! /usr/bin/env bash
# Some fingerprints for the tag annotations.
[ $# -ne 1 ] && exit 2
[ -n "${1}" ] || exit 2
path="${1}"
[ -f "${path}" ] || exit 1
printf "%s artifact:%s:\n\n" "-" "${path}"
printf "  + %s:" "blake2"
b2sum "${path}" | cut -f 1 -d ' ' | tr -d "\n"
printf "\n  + %s:" "blake3"
b3sum "${path}" | cut -f 1 -d ' ' | tr -d "\n"
printf "\n  + %s:" "bytes"
wc -c < "${path}" | tr -d "\n" | tr -d " "
printf "\n  + %s:" "crc32"
crc32 "${path}" | tr -d "\n"
printf "\n  + %s:" "entropy"
ent -t "${path}" | grep 1 | cut -f 3 -d ',' | tr -d "\n"
printf "\n  + %s:(" "file"
file "${path}" | cut -f 2- -d ':' | cut -c 2- | tr -d "\n"
printf ")"
printf "\n  + %s:" "hex32"
xxd -ad -ps -g 32 -c 32 -len 32 "${path}" | tr -d "\n"
printf "\n  + %s:" "md5"
md5sum "${path}" | cut -f 1 -d ' ' | tr -d "\n"
printf "\n  + %s:(" "mime-encoding"
file --mime-encoding "${path}" | cut -f 2- -d ':' | cut -c 2- | tr -d "\n"
printf ")"
printf "\n  + %s:(" "mime-type"
file --mime-type "${path}" | cut -f 2- -d ':' | cut -c 2- | tr -d "\n"
printf ")\n"
for h in sha sha256 sha384 sha512
do
    printf "  + %s:" "${h}"
    ${h}sum "${path}" | cut -f 1 -d ' '
done
printf "  + %s:" "ssdeep"
ssdeep "${path}" 2>&1 | grep -v -e ssdeep -e "large enough" | cut -f 1 -d ',' | tr -d "\n"
printf "\n  + %s:" "tlsh"
tlsh -f "${path}" | cut -f 1 | tr -d "\n"
printf "\n"
