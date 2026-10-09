1..20 | ForEach-Object {
    $scale = [Math]::Round((Get-Random -Minimum 0.4 -Maximum 1.6), 2)
    python script.py -o "alt_cover_$_.jpg" -s $scale
}
