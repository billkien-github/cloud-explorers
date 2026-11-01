# Shot runner. -Shot là thư mục shot tính từ gốc dự án (ví dụ 04_PRODUCTION\EP001_Great_Rain_Experiment\sh010):
#   .\pipeline\run.ps1 build -Shot <shot>               # dựng lại <shot>.blend từ build_shot.py
#   .\pipeline\run.ps1 stills [1,120,240] -Shot <shot>  # render vài khung PNG để duyệt look
#   .\pipeline\run.ps1 preview -Shot <shot>             # cả shot, 960x540 -> renders\<shot>_preview.mp4 (có tiếng nếu scene có sound strip)
#   .\pipeline\run.ps1 final -Shot <shot>               # 1920x1080, motion blur -> renders\<shot>_final.mp4
#   .\pipeline\run.ps1 audio -Shot <shot>               # ghép audio\<shot>_mix.wav vào video preview sẵn có, không render lại hình
#   .\pipeline\run.ps1 open -Shot <shot>                # mở <shot>.blend trong Blender GUI (Space để play)
#   .\pipeline\run.ps1 mcp -Shot <shot>                 # mở kèm --online-mode để add-on MCP tự bật (cổng 9876)
param(
    [Parameter(Position = 0)][ValidateSet("build", "stills", "preview", "final", "audio", "open", "mcp")][string]$Mode = "stills",
    [Parameter(Position = 1)][string[]]$Frames = @(),                 # PowerShell đọc 300,540 thành mảng
    [Parameter(Mandatory = $true)][string]$Shot
)
$Blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
$ShotDir = Join-Path (Split-Path $PSScriptRoot -Parent) $Shot
$Name = ((Split-Path $ShotDir -Leaf) -split "_")[0]              # sh010_intro -> sh010
$Blend = Join-Path $ShotDir ($Name + ".blend")
$Build = Join-Path $ShotDir "build_shot.py"

switch ($Mode) {
    "build" { & $Blender -b --factory-startup -P $Build }
    "open" { & $Blender $Blend }
    "mcp" { Start-Process -FilePath $Blender -ArgumentList "--online-mode", "`"$Blend`"" }
    "audio" {
        $video = Join-Path $ShotDir "renders\$($Name)_preview.mp4"
        $wav = Join-Path $ShotDir "audio\$($Name)_mix.wav"
        $out = Join-Path $ShotDir "renders\$($Name)_preview_sound.mp4"
        if (-not (Test-Path $video)) { Write-Host "Chưa có $video - chạy '.\pipeline\run.ps1 preview -Shot $Shot' trước." }
        elseif (-not (Test-Path $wav)) { Write-Host "Chưa có $wav" }
        else { & $Blender -b --factory-startup -P (Join-Path $PSScriptRoot "mux_audio.py") -- $video $wav $out }
    }
    default {
        if (-not (Test-Path $Blend)) { & $Blender -b --factory-startup -P $Build }
        $extra = @($Mode)
        if ($Frames) { $extra += ($Frames -join ",") }
        & $Blender -b $Blend -P (Join-Path $PSScriptRoot "render.py") -- @extra
    }
}
