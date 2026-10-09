#!/bin/sh
set -eu
exec java -jar /opt/structurizr/structurizr.war "$@"
