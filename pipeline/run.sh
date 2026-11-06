#!/bin/bash
# Shot runner cho macOS, cùng chế độ và đối số với run.ps1. -Shot là thư mục shot tính từ gốc dự án, viết bằng /
# (ví dụ 04_PRODUCTION/EP001_Great_Rain_Experiment/sh010):
#   pipeline/run.sh build -Shot <shot>               # dựng lại <shot>.blend từ build_shot.py
#   pipeline/run.sh stills [1,120,240] -Shot <shot>  # render vài khung PNG để duyệt look
#   pipeline/run.sh preview -Shot <shot>             # cả shot, 960x540 -> renders/<shot>_preview.mp4 (có tiếng nếu scene có sound strip)
#   pipeline/run.sh final -Shot <shot>               # 1920x1080, motion blur -> renders/<shot>_final.mp4
#   pipeline/run.sh ref -Shot <shot>                 # 1920x1080, ít sample -> renders/<shot>_ref.mp4 (video dẫn cho Seedance)
#   pipeline/run.sh open -Shot <shot>                # mở <shot>.blend trong Blender GUI (Space để play)
#   pipeline/run.sh mcp -Shot <shot>                 # mở kèm --online-mode để add-on MCP tự bật (cổng 9876)
# Blender mặc định ở /Applications/Blender.app; để nơi khác thì đặt biến môi trường BLENDER.
# Giữ đồng bộ với run.ps1 (bản Windows): sửa file này thì sửa luôn file kia (pipeline/README.md).
set -u

BLENDER="${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

lower() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]'; }
fail() { echo "$1" >&2; exit 2; }

MODE="" FRAMES="" SHOT=""
while [ $# -gt 0 ]; do
    case "$(lower "$1")" in
        -shot | --shot)
            [ $# -ge 2 ] || fail "Thiếu thư mục shot sau -Shot."
            SHOT="$2"; shift 2 ;;
        *)
            if [ -z "$MODE" ]; then MODE="$(lower "$1")"
            elif [ -z "$FRAMES" ]; then FRAMES="$1"
            else fail "Thừa đối số: $1"
            fi
            shift ;;
    esac
done
MODE="${MODE:-stills}"
case "$MODE" in
    build | stills | preview | final | ref | open | mcp) ;;
    *) fail "Chế độ không có: $MODE (build, stills, preview, final, ref, open, mcp)" ;;
esac
[ -n "$SHOT" ] || fail "Cần -Shot <thư mục shot tính từ gốc dự án>."

SHOT="${SHOT//\\//}"                                              # nhận cả đường dẫn kiểu Windows trong ngoặc kép
SHOT="${SHOT%/}"
case "$SHOT" in /*) SHOT_DIR="$SHOT" ;; *) SHOT_DIR="$ROOT/$SHOT" ;; esac
[ -d "$SHOT_DIR" ] || fail "Không có thư mục $SHOT_DIR"
[ -x "$BLENDER" ] || fail "Không thấy Blender ở $BLENDER. Cài Blender 5.2 vào /Applications hoặc đặt BLENDER=<đường dẫn>."
BASE="$(basename "$SHOT_DIR")"
NAME="${BASE%%_*}"                                                # sh010_intro -> sh010
BLEND="$SHOT_DIR/$NAME.blend"
BUILD="$SHOT_DIR/build_shot.py"

case "$MODE" in
    build)
        [ -f "$BUILD" ] || fail "Không có $BUILD"
        exec "$BLENDER" -b --factory-startup -P "$BUILD" ;;
    open)
        exec "$BLENDER" "$BLEND" ;;
    mcp)
        nohup "$BLENDER" --online-mode "$BLEND" >/dev/null 2>&1 &
        echo "Đã mở Blender với --online-mode, add-on MCP nghe ở 127.0.0.1:9876." ;;
    *)
        if [ ! -f "$BLEND" ]; then "$BLENDER" -b --factory-startup -P "$BUILD"; fi
        exec "$BLENDER" -b "$BLEND" -P "$ROOT/pipeline/render.py" -- "$MODE" ${FRAMES:+"$FRAMES"} ;;
esac
