#!/usr/bin/env bash

CM=$(which cm)

$CM selenoid start
$CM selenoid-ui start