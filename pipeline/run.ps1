# Shot runner. -Shot là thư mục shot tính từ gốc dự án (ví dụ 04_PRODUCTION\EP001_Great_Rain_Experiment\sh010):
#   .\pipeline\run.ps1 build -Shot <shot>               # dựng lại <shot>.blend từ build_shot.py
#   .\pipeline\run.ps1 stills [1,360,720]               # render vài khung PNG để duyệt look
#   .\pipeline\run.ps1 preview                          # cả shot, 960x540 -> renders\<shot>_preview.mp4 (có tiếng nếu có audio)
#   .\pipeline\run.ps1 final                            # 1920x1080, motion blur -> renders\<shot>_final.mp4
#   .\pipeline\run.ps1 audio                            # tạo lại âm thanh (build_audio.py) rồi ghép vào video preview sẵn có
#   .\pipeline\run.ps1 open                             # mở <shot>.blend trong Blender GUI (Space để play, có tiếng)
#   .\pipeline\run.ps1 mcp                              # mở kèm --online-mode để add-on MCP tự bật (cổng 9876)
param(
    [Parameter(Position = 0)][ValidateSet("build", "stills", "preview", "final", "audio", "open", "mcp")][string]$Mode = "stills",
    [Parameter(Position = 1)][string]$Frames = "",
    [Parameter(Mandatory = $true)][string]$Shot
)
$Blender = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
$BlenderPython = "C:\Program Files\Blender Foundation\Blender 5.2\5.2\python\bin\python.exe"   # có sẵn numpy
$ShotDir = Join-Path (Split-Path $PSScriptRoot -Parent) $Shot
$Name = ((Split-Path $ShotDir -Leaf) -split "_")[0]              # sh010_intro -> sh010
$Blend = Join-Path $ShotDir ($Name + ".blend")
$Build = Join-Path $ShotDir "build_shot.py"

switch ($Mode) {
    "build" { & $Blender -b --factory-startup -P $Build }
    "open" { & $Blender $Blend }
    "mcp" { Start-Process -FilePath $Blender -ArgumentList "--online-mode", "`"$Blend`"" }
    "audio" {
        & $BlenderPython (Join-Path $ShotDir "build_audio.py")
        $video = Join-Path $ShotDir "renders\$($Name)_preview.mp4"
        $wav = Join-Path $ShotDir "audio\$($Name)_mix.wav"
        $out = Join-Path $ShotDir "renders\$($Name)_preview_sound.mp4"
        if (Test-Path $video) { & $Blender -b --factory-startup -P (Join-Path $PSScriptRoot "mux_audio.py") -- $video $wav $out }
        else { Write-Host "Chưa có $video - chạy '.\pipeline\run.ps1 preview -Shot $Shot' trước." }
    }
    default {
        if (-not (Test-Path $Blend)) { & $Blender -b --factory-startup -P $Build }
        $extra = @($Mode)
        if ($Frames) { $extra += $Frames }
        & $Blender -b $Blend -P (Join-Path $PSScriptRoot "render.py") -- @extra
    }
}
