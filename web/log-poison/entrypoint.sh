#!/bin/bash
set -e
: > /var/log/apache2/access.log
chmod 0644 /var/log/apache2/access.log
exec apache2-foreground
