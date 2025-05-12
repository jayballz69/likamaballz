Write-Host "Docker Network Inspection" -ForegroundColor Cyan

# Get the ovos_network details
Write-Host "
Network: ovos_network" -ForegroundColor Green
docker network inspect ovos_network | ConvertFrom-Json | ForEach-Object {
    Write-Host "  Name: "
    Write-Host "  Driver: "
    Write-Host "  Subnet: "
    Write-Host "  Gateway: "
    
    Write-Host "
  Containers:" -ForegroundColor Yellow
    .Containers.PSObject.Properties | ForEach-Object {
        Write-Host "     ()"
    }
}

# Get container details
Write-Host "
OVOS Container Details:" -ForegroundColor Green
docker inspect ovos | ConvertFrom-Json | ForEach-Object {
    Write-Host "  Name: "
    Write-Host "  Networks:"
    .NetworkSettings.Networks.PSObject.Properties | ForEach-Object {
        Write-Host "    : "
    }
    
    Write-Host "
  Environment Variables:" -ForegroundColor Yellow
    .Config.Env | ForEach-Object {
        if ( -match "BUS|HOST|PORT") {
            Write-Host "    "
        }
    }
}

# Get messagebus container details
Write-Host "
MessageBus Container Details:" -ForegroundColor Green
docker inspect ovos_messagebus | ConvertFrom-Json | ForEach-Object {
    Write-Host "  Name: "
    Write-Host "  Networks:"
    .NetworkSettings.Networks.PSObject.Properties | ForEach-Object {
        Write-Host "    : "
    }
    
    Write-Host "  Ports:"
    .NetworkSettings.Ports.PSObject.Properties | ForEach-Object {
        Write-Host "    : :"
    }
}
