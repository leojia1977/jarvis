# S3-A Runtime Startup

## Goal
Run SecuPilot as a local investigation service with:
- `GET /health`
- `GET /ready`
- `POST /api/v1/investigate`

## Local Start Command
```powershell
py -3 run_runtime.py
```

Default listen address:
- host: `127.0.0.1`
- port: `8080`

## Example Health Check
```powershell
Invoke-RestMethod http://127.0.0.1:8080/health
```

## Example Readiness Check
```powershell
Invoke-RestMethod http://127.0.0.1:8080/ready
```

## Example Investigation Request
```powershell
$body = @{
  user_input = "请检查最近是否有横向移动"
  intent = "threat_hunt"
  time_range = "24h"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://127.0.0.1:8080/api/v1/investigate `
  -Method Post `
  -Body $body `
  -ContentType 'application/json'
```

## Current Sprint 3 Scope
- runtime mode supports `mock`
- production mode is explicitly reported as not ready
- real adapter delivery remains part of `S3-C`
