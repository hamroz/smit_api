#!/bin/sh

set -e

host="$1"
shift
port="$1"
shift
cmd="$@"

until nc -z "$host" "$port"; do
  echo "$(date) - waiting for $host:$port..."
  sleep 1
done

>&2 echo "$(date) - $host:$port is available - executing command"
exec $cmd
