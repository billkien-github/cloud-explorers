"""
Danh sách dựng Cảnh 1 tập 01 từ các take Seedance (pipeline/edit.py). Đổi take thì sửa tên file; cắt đoạn và CC lấy
từ build_shot.py của từng shot (SEGMENT, TIMING, OFFSET), không ghi số ở đây.
    blender -b --factory-startup -P pipeline/edit.py -- 04_PRODUCTION/EP001_Great_Rain_Experiment/canh01_edit.py
"""
CLIPS = [
    "sh010/seedance/sh010_take01.mp4",
    "sh020/seedance/sh020_take01.mp4",
]
