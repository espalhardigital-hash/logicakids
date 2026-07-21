$path1 = "D:\Antigravity\APP_Logica_Matematicas_kids\LogicaMath\backend\app\fase5\theory_examples.py"
$path2 = "D:\Antigravity\APP_Logica_Matematicas_kids\LogicaMath\backend\app\fase5\seed.py"
$path3 = "D:\Antigravity\APP_Logica_Matematicas_kids\LogicaMath\backend\app\fase5\svg_helpers.py"

$files = @($path1, $path2, $path3)

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -Encoding UTF8

        # 1. Update background color
        # Replace background:#XXXXXX with background:#111827
        $content = [regex]::Replace($content, 'background:\s*#[0-9a-fA-F]{6}', 'background:#111827')

        # 2. Update font sizes to be at least 13
        # Match font-size='XX' or font-size="XX" or font-size=XX
        $pattern = "(font-size=)(['""]?)(\d+)(['""]?)"
        $content = [regex]::Replace($content, $pattern, {
            param($match)
            $prefix = $match.Groups[1].Value
            $quote1 = $match.Groups[2].Value
            $size = [int]$match.Groups[3].Value
            $quote2 = $match.Groups[4].Value
            
            if ($size -lt 13) {
                $size = 13
            }
            return "$prefix$quote1$size$quote2"
        })

        Set-Content -Path $file -Value $content -Encoding UTF8
        Write-Host "Patched $file"
    } else {
        Write-Host "File not found: $file"
    }
}
