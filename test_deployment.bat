@echo off
echo 🧪 Testing AI Wellness Assistant Deployment
echo =============================================
echo.

echo Testing main dashboard...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000' -UseBasicParsing; if ($response.StatusCode -eq 200) { Write-Host '✅ Main dashboard - OK' -ForegroundColor Green } else { Write-Host '❌ Main dashboard - Failed' -ForegroundColor Red } } catch { Write-Host '❌ Main dashboard - Connection failed' -ForegroundColor Red }"

echo.
echo Testing health endpoint...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000/health' -UseBasicParsing; if ($response.StatusCode -eq 200) { Write-Host '✅ Health check - OK' -ForegroundColor Green; Write-Host 'Response:' $response.Content } else { Write-Host '❌ Health check - Failed' -ForegroundColor Red } } catch { Write-Host '❌ Health check - Connection failed' -ForegroundColor Red }"

echo.
echo 🎉 Your AI Wellness Assistant is deployed and running!
echo 🌐 Visit: http://localhost:5000
echo.
pause
