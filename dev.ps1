param (
    [string]$Command = "help"
)

switch ($Command) {
    "help" {
        Write-Host "OpenMCP Windows Dev Script commands:" -ForegroundColor Cyan
        Write-Host "Docker Environment:"
        Write-Host "  .\dev.ps1 up           - Start local Docker environment in the background"
        Write-Host "  .\dev.ps1 down         - Stop local Docker environment"
        Write-Host "  .\dev.ps1 logs         - Tail logs from all containers"
        Write-Host "  .\dev.ps1 db-shell     - Open PostgreSQL shell"
        Write-Host ""
        Write-Host "Local Development:"
        Write-Host "  .\dev.ps1 install      - Install frontend, backend, SDK, and docs dependencies"
        Write-Host "  .\dev.ps1 dev-backend  - Run backend server locally (uvicorn)"
        Write-Host "  .\dev.ps1 dev-web      - Run web frontend locally (vite)"
        Write-Host "  .\dev.ps1 docs         - Run mkdocs server locally"
    }
    "up" {
        docker compose up -d
    }
    "down" {
        docker compose down
    }
    "logs" {
        docker compose logs -f
    }
    "db-shell" {
        docker compose exec db psql -U openmcp_user -d openmcp_db
    }
    "install" {
        Write-Host "Installing backend dependencies..." -ForegroundColor Green
        Push-Location backend
        pip install -r requirements.txt
        Pop-Location
        
        Write-Host "Installing web dependencies..." -ForegroundColor Green
        Push-Location web
        npm install
        Pop-Location
        
        Write-Host "Installing docs dependencies..." -ForegroundColor Green
        pip install mkdocs-material
        
        Write-Host "Installing CLI in dev mode..." -ForegroundColor Green
        Push-Location cli
        pip install -e .
        Pop-Location
        
        Write-Host "Installing SDK in dev mode..." -ForegroundColor Green
        Push-Location sdk
        pip install -e .
        Pop-Location
    }
    "dev-backend" {
        Push-Location backend
        python -m uvicorn app.main:app --reload
        Pop-Location
    }
    "dev-web" {
        Push-Location web
        npm run dev
        Pop-Location
    }
    "docs" {
        python -m mkdocs serve
    }
    default {
        Write-Host "Unknown command: $Command. Run '.\dev.ps1 help' to see available commands." -ForegroundColor Red
    }
}
