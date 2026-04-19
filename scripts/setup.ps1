param(
    [switch]$UsePostgres = $false
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

if ($UsePostgres) {
    $env:USE_POSTGRES = "1"
}

python manage.py migrate
python manage.py check
Write-Host "Setup concluido. Rode: python manage.py runserver"
