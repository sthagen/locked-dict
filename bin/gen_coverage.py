#! /usr/bin/env bash
# Some coverage tallying.
printf "verifying presence of required tools ...\n"

succ="+ found "
fail="- did not find "
problem=false

declare -A pairs=(
    [jq]="json query / path implementation"
    [tr]="translate characters implementation"
    [b2sum]="blake2 hashing implementation"
    [b3sum]="blake3 hashing implementation"
    [sha512sum]="sha512sum hashing implementation"
    [sha384sum]="sha384sum hashing implementation"
    [sha256sum]="sha256sum hashing implementation"
    [sha1sum]="sha1 hashing implementation"
    [md5sum]="md5 hashing implementation"
    [ent]="entropy (shannon max is 8 bits per byte) calculator implementation"
    [cut]="cut out selected portions of each line of a file implementation"
    [wc]="word count implementatiom for line count"
    [sed]="stream editor implementation"
)

for tool in "${!pairs[@]}"; do
    message="${pairs[$tool]} (${tool})"
    if report="$(type "${tool}" 2>&1)" 
    then 
        printf "%s%s\n" "${succ}" "${message}"
        printf "  -> %s\n" "${report}"
    else 
        printf "%s%s\n" "${fail}" "${message}"
        printf "  -> %s\n" "${report}"
        problem=true
    fi
done

if $problem
then
    printf "did not find all required tools - exiting\n" && exit 1
fi

rk="$(basename "${PWD}")"
printf "executing tests and deriving total converage and context information in (%s) ...\n" "${rk}"

# shellcheck disable=SC2046
{ timeout 369 echo "\n\n\n\n\n\n" | bin/local_covli.sh && \
  cov_db="etc/coverage-totals.json" && \
  coverage json --pretty-print --data-file=.coverage --show-contexts -o local_coverage.json && \
  ts="$(date -u +'%Y-%m-%d %H:%M:%S +00:00')" && nid="$(bin/gen_node_identifier.py)" && \
  files="$(jq '.files |keys' local_coverage.json)" && \
  nfiles=$(jq -r '.files |keys[]' local_coverage.json  | wc -l | tr -d ' ') && \
  cat $(jq -r '.files |keys[]' local_coverage.json  | tr '\n' ' ') > local_cat.py && \
  blake3="$(b3sum local_cat.py | cut -f1 -d' ')" && \
  blake2="$(b2sum local_cat.py | cut -f1 -d' ')" && \
  sha512="$(sha512sum local_cat.py | cut -f1 -d' ')" && \
  sha384="$(sha384sum local_cat.py | cut -f1 -d' ')" && \
  sha256="$(sha256sum local_cat.py | cut -f1 -d' ')" && \
  sha1="$(sha1sum local_cat.py | cut -f1 -d' ')" && \
  md5="$(md5sum local_cat.py | cut -f1 -d' ')" && \
  python_version="$(python -V | cut -f2 -d ' ')" &&\
  entropy="$(ent -t local_cat.py | grep 1 | cut -f 3 -d ',' | tr -d '\n')" && \
  sed -i '' "s/\"version\":/\"coverage_tool_version\":/g;" local_coverage.json && \
  jq .meta,.totals local_coverage.json | jq --slurp 'reduce .[] as $item ({}; . * $item)' > local_bizarre.json && \
  jo "${rk}"=:local_bizarre.json "${rk}[timestamp]"="${ts}" "${rk}[node_id]"="${nid}" "${rk}[nfiles]"="${nfiles}" \
    "${rk}[files]"="${files}" "${rk}[blake3]"="${blake3}"  "${rk}[blake2]"="${blake2}" "${rk}[sha512]"="${sha512}" \
    "${rk}[sha384]"="${sha384}" "${rk}[sha256]"="${sha256}"  "${rk}[sha1]"="${sha1}" "${rk}[md5]"="${md5}" \
    "${rk}[python_version]"="${python_version}" "${rk}[entropy]"="${entropy}" \
    | jq . > "${cov_db}" && \
  rm -f local_coverage.json local_bizarre.json local_cat.py && \
  jq -C . "${cov_db}" && \
  printf "Successfully updated the total converage and context database in (%s) ...\n" "${rk}" 
} || printf "Failed to update the total converage and context database in (%s) ...\n" "${rk}" 
  
