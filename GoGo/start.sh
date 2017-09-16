#!/bin/bash

echo -ne "\033]0;GoGo (Web Console: http://127.0.0.1:9092)\007"

# Detect if we should use JAVA_HOME or just try PATH.
get_java_cmd() {
  if [[ -n "$JAVA_HOME" ]] && [[ -x "$JAVA_HOME/bin/java" ]];  then
    echo "$JAVA_HOME/bin/java"
  else
    echo "java"
  fi
}

declare -r java_cmd=$(get_java_cmd)

# Now check to see if it works
declare -r java_version=$("$java_cmd" -version 2>&1 | awk -F '"' '/version/ {print $2}')

if [[ "$java_version" == "" ]]; then
  echo
  echo No java installations was detected.
  echo Please go to http://www.java.com/getjava/ and download
  echo
  exit 1
else
  cd `dirname $0`
  $java_cmd -Xmx200m -cp lib/gogo.jar io.gogo.GoGo
  exit 1
fi

