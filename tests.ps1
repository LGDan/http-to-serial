#!/usr/bin/pwsh

$baseurl = "http://127.0.0.1:8000/api/v1"
$command = "abc"

Invoke-RestMethod -uri "$baseurl/device/ttyUSB0:115200/open" | Out-String
Invoke-RestMethod -uri "$baseurl/writeline/ttyUSB0/$command" | Out-String
Start-Sleep -Seconds 2
Invoke-RestMethod -uri "$baseurl/device/ttyUSB0/waiting/in" | Out-String
$result = Invoke-RestMethod -uri "$baseurl/readall/ttyUSB0"

$result.read_result