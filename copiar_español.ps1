# Script para copiar idioma español a Tesseract
# Ejecutar como Administrador

Write-Host "Copiando idioma español a Tesseract..." -ForegroundColor Green
Write-Host ""

$origen = "C:\Fabian\Cursor\Pods_DAS\spa.traineddata"
$destino = "C:\Program Files\Tesseract-OCR\tessdata\spa.traineddata"

if (Test-Path $origen) {
    try {
        Copy-Item $origen -Destination $destino -Force
        Write-Host "[OK] Idioma español instalado correctamente!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Archivo copiado a: $destino" -ForegroundColor Cyan
    }
    catch {
        Write-Host "[ERROR] No se pudo copiar el archivo" -ForegroundColor Red
        Write-Host "Error: $_" -ForegroundColor Red
    }
}
else {
    Write-Host "[ERROR] No se encontró el archivo: $origen" -ForegroundColor Red
}

Write-Host ""
Write-Host "Presiona Enter para cerrar..." -ForegroundColor Yellow
Read-Host


