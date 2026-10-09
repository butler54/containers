#!/bin/sh
set -eu
exec java -cp '/opt/structurizr/structurizr-cli.jar:/opt/structurizr/lib/*' com.structurizr.command.DocsCli "$@"
