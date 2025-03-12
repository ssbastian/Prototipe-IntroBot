@echo off
set TELEGRAM_TOKEN=7649773848:AAF-3g2luGrAPlm3KTGuhxTJD_dEfqODbpQ  REM Token fijo

set /p NGROK_URL=Ingresa la URL de Ngrok: 

set WEBHOOK_URL=%NGROK_URL%/webhooks/telegram/webhook

curl -X POST "https://api.telegram.org/bot%TELEGRAM_TOKEN%/setWebhook?url=%WEBHOOK_URL%"

echo Webhook configurado con éxito.
pause
