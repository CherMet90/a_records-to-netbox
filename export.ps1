$dcName = "sw-dc1"
$outputFolder = ".\input"
# Получаем список всех прямых зон на DNS-сервере
$zones = Get-DnsServerZone -ComputerName $dcName | Where-Object { $_.IsReverseLookupZone -eq $false -and $_.ZoneName -ne 'TrustAnchors'}

if (-Not (Test-Path $outputFolder))
{
    New-Item -ItemType Directory -Path $outputFolder
    Write-Host "Folder created: $outputFolder"
}

# Проходимся по каждой прямой зоне и выгружаем записи
foreach ($zone in $zones) {
    $zoneName = $zone.ZoneName
    $outputPath = "$outputFolder\$zoneName.csv"

    # Выгружаем записи для текущей прямой зоны
    Get-DnsServerResourceRecord -ComputerName $dcName -ZoneName $zoneName -RRType A |
        Where-Object { $_.HostName -notlike "*.$zoneName" -and $_.RecordData.IPv4Address -ne "10.10.5.100" } |
        Select-Object HostName, Timestamp, RecordType, @{
            Name       = 'RecordData'
            Expression = { $_.RecordData.IPv4Address }
        } |
        Export-Csv -Path $outputPath -NoTypeInformation
}