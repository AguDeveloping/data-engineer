# Script de PowerShell para actualizar datasets de Power BI

# Configuración
$workspaceName = "Mi Workspace ETL"
$datasetName = "ETL PostgreSQL"
$refreshType = "Full" # Opciones: Full, Incremental

# Requisitos: Módulo MicrosoftPowerBIMgmt
# Para instalar: Install-Module -Name MicrosoftPowerBIMgmt -Scope CurrentUser

Write-Host "Iniciando actualización programada de datasets en Power BI..."

# Verificar si el módulo está instalado
if (-not (Get-Module -ListAvailable -Name MicrosoftPowerBIMgmt)) {
    Write-Host "El módulo MicrosoftPowerBIMgmt no está instalado. Por favor, ejecute:"
    Write-Host "Install-Module -Name MicrosoftPowerBIMgmt -Scope CurrentUser"
    exit 1
}

try {
    # Importar módulo
    Import-Module MicrosoftPowerBIMgmt
    
    # Iniciar sesión en Power BI Service
    Write-Host "Conectando a Power BI Service..."
    Connect-PowerBIServiceAccount
    
    # Obtener el workspace
    $workspace = Get-PowerBIWorkspace -Name $workspaceName
    
    if ($workspace) {
        # Obtener dataset
        $dataset = Get-PowerBIDataset -WorkspaceId $workspace.Id | Where-Object {$_.Name -eq $datasetName}
        
        if ($dataset) {
            # Iniciar actualización
            Write-Host "Iniciando actualización del dataset '$datasetName'..."
            Invoke-PowerBIRestMethod -Url "https://api.powerbi.com/v1.0/myorg/groups/$($workspace.Id)/datasets/$($dataset.Id)/refreshes" -Method POST -Body "{\"type\": \"$refreshType\"}"
            
            Write-Host "Solicitud de actualización enviada correctamente."
        } else {
            Write-Host "No se encontró el dataset '$datasetName' en el workspace."
        }
    } else {
        Write-Host "No se encontró el workspace '$workspaceName'."
    }
    
} catch {
    Write-Host "Error al actualizar el dataset: $_"
} finally {
    # Desconectar sesión
    Disconnect-PowerBIServiceAccount
}

Write-Host "Proceso de actualización completado."
