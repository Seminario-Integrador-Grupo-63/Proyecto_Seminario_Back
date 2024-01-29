Start-Process -FilePath "C:\WINDOWS\system32\cmd.exe" -ArgumentList "/c docker compose down  && docker compose up"
Start-Sleep 16
$containerProcess = Start-Process -FilePath "C:\WINDOWS\system32\cmd.exe" -ArgumentList '/c docker exec -it QResto_back bash -c "python -m alembic upgrade head"' -PassThru
Start-Sleep 12
$url = "http://localhost:8000/mock"
Invoke-RestMethod -Uri $url -Method Post


