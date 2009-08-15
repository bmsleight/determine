#!/bin/bash
#
find /tmp/* -mmin +180 -exec rm -fR {} \;
