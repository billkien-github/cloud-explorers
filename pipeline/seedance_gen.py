"""
Sinh clip Seedance của một shot qua API BytePlus ModelArk: đọc prompt và ảnh, gửi, chờ, tải take về, ghi chi phí.
    python pipeline/seedance_gen.py <thư mục shot> --dry-run    # kiểm giới hạn, ước tính chi phí; không gửi
    python pipeline/seedance_gen.py <thư mục shot>              # bản nháp: Seedance 2.5, draft 480p -> seedance/takes/<shot>_takeNN.mp4
    python pipeline/seedance_gen.py <thư mục shot> --final sh010_take07.mp4   # bản final 1080p từ bản nháp đó (người dùng chốt)
    python pipeline/seedance_gen.py <thư mục shot> --resume     # chờ tiếp task đã gửi mà chưa tải về (hết giờ chờ, mất mạng)
Tuỳ chọn: --model 2.5|2.0|2.0-fast|2.0-mini (mặc định 2.5), --no-draft (sinh thường, không qua bản nháp; dòng 2.0 luôn
thế), --resolution 480p|720p|1080p (chỉ cho --no-draft, mặc định 720p), --no-audio (mặc định có tiếng), --duration <giây>
(mặc định SECONDS của build_shot.py), --wait <phút> (mặc định 60).

- Đầu vào: bảng số tham chiếu và khối ```text của seedance/prompt.md, đọc bằng load() của pipeline/seedance_upload.py.
  @Video, @Image gửi theo đúng số; ratio 16:9, watermark tắt.
- Bản nháp (mặc định): Seedance 2.5 với draft=true, API chỉ cho 480p, tính tiền như video 480p thường. Bản final gửi ID
  task của bản nháp (content.draft_task): API tự dùng lại prompt, tham chiếu, seed, tiếng, tỉ lệ, độ dài; hiện chỉ ra 1080p,
  tính tiền 1080p kèm giây video tham chiếu của bản nháp. ID bản nháp sống 14 ngày. Chỉ chạy --final khi người dùng chốt.
- Ảnh gửi dạng base64. Video tham chiếu API chỉ nhận URL: script tải video lên một bucket riêng tư chuẩn S3 (đang dùng
  Cloudflare R2), đưa ModelArk link ký sẵn có hạn, task kết thúc thì xoá hẳn file.
- Biến môi trường (người dùng tự đặt, không ghi vào repo): ARK_API_KEY; có video tham chiếu thì thêm S3_ENDPOINT
  (<ACCOUNT_ID>.r2.cloudflarestorage.com), S3_BUCKET, S3_ACCESS_KEY và S3_SECRET_KEY (Access Key ID và Secret Access
  Key của R2 API token); dịch vụ chuẩn S3 khác thì có thể cần thêm S3_REGION.
- Task kết thúc (xong hay lỗi) thì ghi một dòng vào 04_PRODUCTION/seedance_log.csv (cột mode: draft, final hay trống
  là sinh thường). API chỉ trả số token (usage.completion_tokens), không trả tiền: chi phí = token x đơn giá trong MODELS.
  Task đang chờ ghi ở renders/seedance_pending.json của shot.
Chỉ dùng thư viện chuẩn của Python. Quy trình: 04_PRODUCTION/SEEDANCE.md.
"""
import argparse
import ast
import base64
import csv
import datetime
import hashlib
import hmac
import json
import os
import pathlib
import re
import struct
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import quote

sys.dont_write_bytecode = True  # không để __pycache__ trong pipeline/
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from seedance_upload import load  # noqa: E402

API = "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks"
NHAP_NGAY = 14  # ID task bản nháp còn dùng được để sinh final trong ngần này ngày (tra ngày 07/11/2026)

# Tra trang "Create a video generation task" và "Pricing" của ModelArk ngày 06/11/2026; đổi model hay giá thì sửa ở đây.
# anh, video: số tham chiếu tối đa; video_s: tổng giây video tham chiếu tối đa (mỗi video từ 2 giây); ra: giây ra (min, max);
# gia: USD / 1 triệu token, online inference, (không có video vào, có video vào), theo độ phân giải.
MODELS = {
    "2.5": dict(id="dreamina-seedance-2-5-260628", anh=30, video=10, video_s=30, ra=(4, 30),
                gia={"480p": (10.7, 6.4), "720p": (10.7, 6.4), "1080p": (11.7, 7.0)}),
    "2.0": dict(id="dreamina-seedance-2-0-260128", anh=9, video=3, video_s=15, ra=(4, 15),
                gia={"480p": (7.0, 4.3), "720p": (7.0, 4.3), "1080p": (7.7, 4.7)}),
    "2.0-fast": dict(id="dreamina-seedance-2-0-fast-260128", anh=9, video=3, video_s=15, ra=(4, 15),
                     gia={"480p": (5.6, 3.3), "720p": (5.6, 3.3)}),
    "2.0-mini": dict(id="dreamina-seedance-2-0-mini-260615", anh=9, video=3, video_s=15, ra=(4, 15),
                     gia={"480p": (3.5, 2.1), "720p": (3.5, 2.1)}),
}
KHUNG = {"480p": (864, 496), "720p": (1280, 720), "1080p": (1920, 1080)}  # 16:9; riêng 2.5 ở 480p là 854x480
FPS = 24
MIME = {".png": "png", ".jpg": "jpeg", ".jpeg": "jpeg", ".webp": "webp"}
XONG = ("succeeded", "failed", "expired", "cancelled")
LOG_COT = ["time", "shot", "take", "model", "task_id", "status", "resolution", "ratio", "duration_s", "images", "videos",
           "video_in_s", "audio", "tokens", "usd_per_m_tokens", "cost_usd", "est_cost_usd", "error", "mode"]


class LoiAPI(Exception):
    def __init__(self, code, text):
        try:
            err = json.loads(text).get("error") or {}
            text = f"{err.get('code', '')}: {err.get('message', text)}"
        except (ValueError, AttributeError):
            pass
        super().__init__(f"HTTP {code} {text}")


# ---------- đọc file

def giay_shot(shot):
    """SECONDS ở cấp module của build_shot.py (dạng `SECONDS = 29` hoặc `FPS, SECONDS = 24, 29`), không có thì None."""
    f = shot / "build_shot.py"
    if not f.is_file():
        return None
    for node in ast.parse(f.read_text(encoding="utf-8")).body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1):
            continue
        t, v = node.targets[0], node.value
        pairs = [(t, v)] if isinstance(t, ast.Name) else (
            zip(t.elts, v.elts) if isinstance(t, ast.Tuple) and isinstance(v, ast.Tuple) else [])
        for tt, vv in pairs:
            if isinstance(tt, ast.Name) and tt.id == "SECONDS" and isinstance(vv, ast.Constant):
                return vv.value
    return None


def mp4_giay(path):
    """Thời lượng (giây) của file mp4/mov, đọc từ hộp mvhd trong moov, không cần ffprobe."""
    end = path.stat().st_size
    with open(path, "rb") as f:
        pos = 0
        while pos + 8 <= end:
            f.seek(pos)
            size, typ = struct.unpack(">I4s", f.read(8))
            hdr = 8
            if size == 1:
                size, hdr = struct.unpack(">Q", f.read(8))[0], 16
            elif size == 0:
                size = end - pos
            if typ == b"moov":
                data = f.read(size - hdr)
                i = data.find(b"mvhd")
                if i < 0:
                    break
                if data[i + 4] == 1:  # version 1: thời điểm 64 bit
                    scale, dur = struct.unpack(">IQ", data[i + 24:i + 36])
                else:
                    scale, dur = struct.unpack(">II", data[i + 16:i + 24])
                return dur / scale
            if size < hdr:
                break
            pos += size
    sys.exit(f"Không đọc được thời lượng của {path}")


def anh(path, loi):
    """Đọc ảnh tham chiếu, kiểm giới hạn của API, trả data URL base64."""
    b = path.read_bytes()
    fmt = MIME.get(path.suffix.lower())
    if fmt is None:
        loi.append(f"{path.name}: chỉ gửi png, jpg, webp")
        return ""
    if len(b) >= 30e6:
        loi.append(f"{path.name}: {len(b) / 1e6:.1f} MB, API nhận ảnh dưới 30 MB")
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", b[16:24])
        if not (300 <= w <= 6000 and 300 <= h <= 6000 and 0.4 <= w / h <= 2.5):
            loi.append(f"{path.name}: {w}x{h}, API cần cạnh 300–6000 px, tỉ lệ rộng/cao 0.4–2.5")
    return f"data:image/{fmt};base64," + base64.b64encode(b).decode("ascii")


# ---------- mạng

def goi(method, url, body=None, headers=None, timeout=120, header_tra=None):
    """Gọi HTTP, trả nội dung; header_tra là tên một header muốn lấy thì trả (nội dung, giá trị header)."""
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            return (data, r.headers.get(header_tra, "")) if header_tra else data
    except urllib.error.HTTPError as e:
        raise LoiAPI(e.code, e.read().decode("utf-8", "replace")) from None


def ark(method, path="", payload=None):
    h = {"Authorization": f"Bearer {os.environ['ARK_API_KEY']}", "Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    return json.loads(goi(method, API + path, data, h))


def ky_s3(method, host, path, region, ak, sk, expires, now, query=None, headers=None):
    """Link ký sẵn chuẩn S3 (AWS Signature V4, ký qua query): ai có link thì làm được đúng một việc (method) với đúng
    một file trong `expires` giây (tối đa 7 ngày). headers: header được ký kèm (vd Content-Type), lúc gọi phải gửi
    đúng giá trị đó."""
    date, ts = now.strftime("%Y%m%d"), now.strftime("%Y%m%dT%H%M%SZ")
    scope = f"{date}/{region}/s3/aws4_request"
    h = {"host": host, **{k.lower(): v.strip() for k, v in (headers or {}).items()}}
    signed = ";".join(sorted(h))
    q = {"X-Amz-Algorithm": "AWS4-HMAC-SHA256", "X-Amz-Credential": f"{ak}/{scope}", "X-Amz-Date": ts,
         "X-Amz-Expires": str(expires), "X-Amz-SignedHeaders": signed, **(query or {})}
    cq = "&".join(f"{quote(k, safe='-_.~')}={quote(v, safe='-_.~')}" for k, v in sorted(q.items()))
    path = quote(path, safe="/-_.~")
    canon = "\n".join([method, path, cq, "".join(f"{k}:{h[k]}\n" for k in sorted(h)), signed, "UNSIGNED-PAYLOAD"])
    sts = "\n".join(["AWS4-HMAC-SHA256", ts, scope, hashlib.sha256(canon.encode("utf-8")).hexdigest()])
    k = ("AWS4" + sk).encode("utf-8")
    for part in (date, region, "s3", "aws4_request"):
        k = hmac.new(k, part.encode("utf-8"), hashlib.sha256).digest()
    sig = hmac.new(k, sts.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"https://{host}{path}?{cq}&X-Amz-Signature={sig}"


def s3_url(method, key, expires, query=None, headers=None):
    """Link ký sẵn tới một file trong bucket S3_BUCKET, kiểu đường dẫn https://<S3_ENDPOINT>/<bucket>/<key>.
    Cloudflare R2: endpoint <ACCOUNT_ID>.r2.cloudflarestorage.com, vùng auto. Dịch vụ chuẩn S3 khác: endpoint dạng
    s3.<vùng>.<tên miền> thì vùng lấy từ endpoint, không thì đặt S3_REGION."""
    ak, sk, bucket = (os.environ[k] for k in ("S3_ACCESS_KEY", "S3_SECRET_KEY", "S3_BUCKET"))
    host = os.environ["S3_ENDPOINT"].removeprefix("https://").strip("/")
    region = os.environ.get("S3_REGION") or (host.split(".")[1] if host.startswith("s3.") else "auto")
    return ky_s3(method, host, f"/{bucket}/{key}", region, ak, sk, expires,
                 datetime.datetime.now(datetime.timezone.utc), query, headers)


def tai_len(path, key):
    """Tải file lên bucket; trả version id nếu dịch vụ trả về (B2 cần nó để xoá hẳn)."""
    h = {"Content-Type": "video/quicktime" if path.suffix.lower() == ".mov" else "video/mp4"}
    _, version = goi("PUT", s3_url("PUT", key, 3600, headers=h), path.read_bytes(), h,
                     timeout=900, header_tra="x-amz-version-id")
    return version


def xoa_s3(files):
    """Xoá hẳn các file đã tải lên. Có version id thì xoá đúng version (B2: xoá không kèm version chỉ ẩn file); dịch vụ
    trả version id mà không nhận xoá theo version (R2 báo 501 NotImplemented) thì xoá lại không kèm version."""
    for f in files:
        try:
            try:
                goi("DELETE", s3_url("DELETE", f["key"], 600, {"versionId": f["version"]} if f["version"] else None))
            except LoiAPI as e:
                if not (f["version"] and "NotImplemented" in str(e)):
                    raise
                goi("DELETE", s3_url("DELETE", f["key"], 600))
        except (LoiAPI, OSError, KeyError) as e:
            print(f"  Chưa xoá được {f['key']} trên bucket ({e!r}); xoá tay trong trang quản lý bucket nếu cần")


# ---------- sổ task đang chờ, take, log

def doc_cho(shot):
    f = shot / "renders" / "seedance_pending.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.is_file() else []


def ghi_cho(shot, entries):
    f = shot / "renders" / "seedance_pending.json"
    if entries:
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    elif f.exists():
        f.unlink()


def take_moi(shot):
    d = shot / "seedance" / "takes"
    d.mkdir(parents=True, exist_ok=True)
    nums = [int(m.group(1)) for p in d.glob(f"{shot.name}_take*.mp4")
            if (m := re.search(r"_take(\d+)\.mp4$", p.name))]
    return d / f"{shot.name}_take{max(nums, default=0) + 1:02d}.mp4"


def ghi_log(root, row):
    f = root / "04_PRODUCTION" / "seedance_log.csv"
    moi = not f.exists()
    if not moi:  # log cũ thiếu cột mới thì viết lại với đủ cột, ô thiếu để trống
        with open(f, newline="", encoding="utf-8") as fh:
            r = csv.DictReader(fh)
            if r.fieldnames != LOG_COT:
                cu = list(r)
                with open(f, "w", newline="", encoding="utf-8") as fw:
                    w = csv.DictWriter(fw, LOG_COT, lineterminator="\n", extrasaction="ignore")
                    w.writeheader()
                    w.writerows(cu)
    with open(f, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, LOG_COT, lineterminator="\n")  # xuống dòng LF, giống nhau trên macOS và Windows
        if moi:
            w.writeheader()
        w.writerow(row)


def bay_gio():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def dong_log(e, **kw):
    """Một dòng log từ thông tin task đã ghi lúc gửi (e), cộng các cột kết quả trong kw."""
    m = MODELS[e["model"]]
    row = dict(time=bay_gio(), shot=e["shot"], take="", model=m["id"], task_id=e.get("task_id", ""), status="",
               resolution=e["resolution"], ratio="16:9", duration_s=e["duration"], images=e["images"],
               videos=e["videos"], video_in_s=e["video_in_s"], audio=e["audio"], tokens=0,
               usd_per_m_tokens=m["gia"][e["resolution"]][1 if e["videos"] else 0], cost_usd=0,
               est_cost_usd=e["est_usd"], error="", mode=e.get("mode", ""))
    row.update(kw)
    return row


# ---------- chuẩn bị, gửi, chờ

def chuan_bi(shot, a):
    """Đọc prompt.md, chọn model, kiểm mọi giới hạn. Trả thông tin để gửi; có lỗi thì in ra và thoát mã 1."""
    root, prompt, refs = load(shot)
    loi, canh_bao = [], []
    videos = sorted((r for r in refs if r[0] == "Video"), key=lambda r: r[1])
    images = sorted((r for r in refs if r[0] == "Image"), key=lambda r: r[1])
    for group, kind in ((videos, "Video"), (images, "Image")):
        if [r[1] for r in group] != list(range(1, len(group) + 1)):
            loi.append(f"Số @{kind} trong bảng phải liền nhau từ 1 (đang có {[r[1] for r in group]})")
    loi += [f"Thiếu nguồn của @{k}{n}: {src}" for k, n, _, src, path in refs if path is None]
    dung = {(k, int(n)) for k, n in re.findall(r"@(Video|Image) ?(\d+)", prompt)}
    co = {(r[0], r[1]) for r in refs}
    loi += [f"Prompt gọi @{k}{n} nhưng bảng không có" for k, n in sorted(dung - co)]
    canh_bao += [f"Bảng có @{k}{n} nhưng prompt không gọi tới" for k, n in sorted(co - dung)]
    words = len(prompt.split())

    video_giay = [mp4_giay(r[4]) if r[4] else 0.0 for r in videos]
    vin = sum(video_giay)
    duration = a.duration or giay_shot(shot)
    if duration is None:
        sys.exit("Không thấy SECONDS trong build_shot.py; truyền --duration <giây>")
    canh_bao += [f"Video tham chiếu dài {s:.1f} s, khác thời lượng sinh {duration} s"
                 for s in video_giay if s and abs(s - duration) > 0.5]

    goi_y = []
    key = a.model
    m = MODELS[key]
    draft = key == "2.5" and not a.no_draft
    res = "480p" if draft else a.resolution
    ly_do = ("bản nháp (draft 480p); bản final 1080p chỉ khi người dùng chốt: --final <take>" if draft
             else "sinh thường, không qua bản nháp")
    if len(images) > m["anh"] or len(videos) > m["video"]:
        loi.append(f"Seedance {key} nhận tối đa {m['anh']} ảnh và {m['video']} video tham chiếu "
                   f"(đang có {len(images)} ảnh, {len(videos)} video)")
    if key != "2.5" and not refs:
        loi.append(f"Seedance {key} cần ít nhất một ảnh hay video tham chiếu")
    if any(0 < s < 2 for s in video_giay):
        loi.append("Mỗi video tham chiếu phải dài ít nhất 2 giây")
    if not m["ra"][0] <= duration <= m["ra"][1] or vin > m["video_s"]:
        loi.append(f"Seedance {key} sinh {m['ra'][0]}–{m['ra'][1]} giây và nhận video tham chiếu tổng tối đa "
                   f"{m['video_s']} giây (đoạn này: sinh {duration} s, video tham chiếu {vin:.1f} s): chia lại đoạn "
                   "(04_PRODUCTION/SEEDANCE.md, mục Chia cảnh thành đoạn)")
    if res not in m["gia"]:
        loi.append(f"Seedance {key} không có {res} (có {', '.join(m['gia'])})")

    data_urls = [anh(r[4], loi) if r[4] else "" for r in images]
    body_mb = (sum(len(u) for u in data_urls) + len(prompt)) / 1e6
    if body_mb > 60:
        loi.append(f"Ảnh base64 + prompt nặng {body_mb:.0f} MB, API nhận request tối đa 64 MB: bớt ảnh hoặc nén ảnh")

    w, h = khung(key, res)
    est_tokens = (vin + duration) * w * h * FPS / 1024
    gia = m["gia"].get(res, (0, 0))[1 if videos else 0]
    est = est_tokens * gia / 1e6
    if draft:
        fw, fh = khung(key, "1080p")
        tien_final = (vin + duration) * fw * fh * FPS / 1024 * m["gia"]["1080p"][1 if videos else 0] / 1e6
        goi_y.append(f"Bản final 1080p từ bản nháp này: khoảng ${tien_final:.2f}, chỉ khi người dùng chốt")

    print(f"Shot: {shot.relative_to(root).as_posix()}")
    print(f"Model: Seedance {key} ({m['id']}) — {ly_do}")
    print(f"Sinh {duration} s · {res} · 16:9 · {'không tiếng' if a.no_audio else 'có tiếng'} · watermark tắt")
    for (kind, n, name, src, _), s in zip(videos, video_giay):
        print(f"  @{kind}{n}  {src}  ({s:.1f} s)")
    for kind, n, name, src, _ in images:
        print(f"  @{kind}{n}  {src}")
    print(f"Prompt: {words} từ")
    print(f"Ước tính: ({vin:.1f} s video vào + {duration} s ra) x {w}x{h} x {FPS} fps / 1024 = {est_tokens:,.0f} token")
    print(f"          {est_tokens:,.0f} token x ${gia} / 1 triệu token = ${est:.2f} (số thật lấy từ usage.completion_tokens)")
    for c in goi_y:
        print(f"[Gợi ý] {c}")
    for c in canh_bao:
        print(f"[Cảnh báo] {c}")
    for x in loi:
        print(f"[Lỗi] {x}")
    if loi:
        sys.exit(1)
    return dict(root=root, prompt=prompt, key=key, duration=duration, videos=videos, images=images,
                data_urls=data_urls, vin=vin, est=est, draft=draft, res=res)


def khung(key, res):
    return (854, 480) if key == "2.5" and res == "480p" else KHUNG[res]


def chuan_bi_final(shot, a):
    """Tìm bản nháp a.final của shot trong log (task 2.5, mode draft, xong, còn hạn); in chi phí bản final 1080p."""
    root = next(p for p in [shot, *shot.parents] if (p / "CLAUDE.md").exists())
    f = root / "04_PRODUCTION" / "seedance_log.csv"
    take = pathlib.Path(a.final).name
    rel = shot.relative_to(root).as_posix()
    with open(f, newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["shot"] == rel and r["take"] == take and r["status"] == "succeeded"]
    if not rows:
        sys.exit(f"Không thấy {take} của {rel} trong {f.name}")
    r = rows[-1]
    if r.get("mode") != "draft" or r["model"] != MODELS["2.5"]["id"]:
        sys.exit(f"{take} không phải bản nháp Seedance 2.5 (mode {r.get('mode') or 'thường'}, model {r['model']})")
    tuoi = datetime.datetime.now().astimezone() - datetime.datetime.fromisoformat(r["time"])
    if tuoi.days >= NHAP_NGAY:
        sys.exit(f"Bản nháp {take} đã {tuoi.days} ngày, quá hạn {NHAP_NGAY} ngày của ID task: sinh lại bản nháp")
    vin, duration, videos = float(r["video_in_s"]), int(float(r["duration_s"])), int(r["videos"])
    w, h = khung("2.5", "1080p")
    gia = MODELS["2.5"]["gia"]["1080p"][1 if videos else 0]
    est_tokens = (vin + duration) * w * h * FPS / 1024
    est = est_tokens * gia / 1e6
    print(f"Shot: {rel}")
    print(f"Bản final Seedance 2.5 1080p từ bản nháp {take} (task {r['task_id']}, {tuoi.days} ngày tuổi); API dùng lại "
          "prompt, tham chiếu, seed, tiếng, tỉ lệ, độ dài của bản nháp")
    print(f"Ước tính: ({vin:.1f} s video vào + {duration} s ra) x {w}x{h} x {FPS} fps / 1024 = {est_tokens:,.0f} token")
    print(f"          {est_tokens:,.0f} token x ${gia} / 1 triệu token = ${est:.2f} (số thật lấy từ usage.completion_tokens)")
    return dict(root=root, draft_id=r["task_id"], out=pathlib.Path(take).stem + "_final.mp4", duration=duration,
                images=int(r["images"]), videos=videos, vin=vin, audio=r["audio"] == "True", est=est)


def gui_final(shot, p):
    root = p["root"]
    e = dict(shot=shot.relative_to(root).as_posix(), model="2.5", resolution="1080p", duration=p["duration"],
             images=p["images"], videos=p["videos"], video_in_s=round(p["vin"], 2), audio=p["audio"],
             est_usd=round(p["est"], 3), uploads=[], mode="final", out=p["out"])
    body = {"model": MODELS["2.5"]["id"], "content": [{"type": "draft_task", "draft_task": {"id": p["draft_id"]}}],
            "resolution": "1080p", "watermark": False}
    try:
        task = ark("POST", "", body)
    except (LoiAPI, OSError) as x:
        ghi_log(root, dong_log(e, status="rejected", error=str(x)))
        sys.exit(f"ModelArk từ chối task: {x}")
    e.update(task_id=task["id"], submitted=bay_gio())
    ghi_cho(shot, doc_cho(shot) + [e])
    print(f"Đã gửi: task {task['id']}")
    return e


def gui(shot, a, p):
    """Tải video lên bucket, tạo task, ghi sổ chờ. Trả mục sổ chờ của task."""
    root, key = p["root"], p["key"]
    e = dict(shot=shot.relative_to(root).as_posix(), model=key, resolution=p["res"], duration=p["duration"],
             images=len(p["images"]), videos=len(p["videos"]), video_in_s=round(p["vin"], 2),
             audio=not a.no_audio, est_usd=round(p["est"], 3), uploads=[], mode="draft" if p["draft"] else "")
    content = [{"type": "text", "text": p["prompt"]}]
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for kind, n, name, src, path in p["videos"]:
        obj = f"seedance/{shot.name}/{stamp}_{name}"
        print(f"Tải @Video{n} lên bucket ({path.stat().st_size / 1e6:.1f} MB)…")
        try:
            e["uploads"].append(dict(key=obj, version=tai_len(path, obj)))
        except (LoiAPI, OSError) as x:
            xoa_s3(e["uploads"])
            sys.exit(f"Không tải được @Video{n} lên bucket: {x}")
        # link đọc sống bằng hạn mặc định của task (48 giờ), phòng task phải xếp hàng lâu
        content.append({"type": "video_url", "video_url": {"url": s3_url("GET", obj, 172800)}, "role": "reference_video"})
    for url in p["data_urls"]:
        content.append({"type": "image_url", "image_url": {"url": url}, "role": "reference_image"})
    body = {"model": MODELS[key]["id"], "content": content, "ratio": "16:9", "resolution": p["res"],
            "duration": p["duration"], "watermark": False, "generate_audio": not a.no_audio}
    if p["draft"]:
        body["draft"] = True
    if key == "2.5":
        body["omni_reference_task_type"] = "reference"  # sinh mới theo tham chiếu, không phải sửa hay nối video
    try:
        task = ark("POST", "", body)
    except (LoiAPI, OSError) as x:
        xoa_s3(e["uploads"])
        ghi_log(root, dong_log(e, status="rejected", error=str(x)))
        sys.exit(f"ModelArk từ chối task: {x}")
    e.update(task_id=task["id"], submitted=bay_gio())
    ghi_cho(shot, doc_cho(shot) + [e])
    print(f"Đã gửi: task {task['id']}")
    return e


def ket_thuc(shot, root, e, t):
    """Task đã kết thúc: tải take, ghi log, xoá video đã tải lên bucket, bỏ khỏi sổ chờ."""
    st, take = t["status"], ""
    if st == "succeeded":
        out = shot / "seedance" / "takes" / e["out"] if e.get("out") else take_moi(shot)
        tmp = out.with_suffix(".part")
        with urllib.request.urlopen(t["content"]["video_url"], timeout=600) as r, open(tmp, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)
        tmp.replace(out)
        take = out.name
    tokens = (t.get("usage") or {}).get("completion_tokens", 0)
    err = t.get("error") or {}
    row = dong_log(e, take=take, status=st, tokens=tokens,
                   error=f"{err.get('code', '')}: {err.get('message', '')}" if err else "")
    row["cost_usd"] = round(tokens * row["usd_per_m_tokens"] / 1e6, 3) if st == "succeeded" else 0  # lỗi thì không tính tiền
    ghi_log(root, row)
    xoa_s3(e["uploads"])
    ghi_cho(shot, [x for x in doc_cho(shot) if x["task_id"] != e["task_id"]])
    if take:
        print(f"Xong: seedance/takes/{take} · {tokens:,} token · ${row['cost_usd']:.2f} (ước tính ${e['est_usd']:.2f})")
    else:
        print(f"Task {e['task_id']} {st}: {row['error']}")


def cho(shot, root, entries, wait_min):
    """Hỏi trạng thái 15 giây một lần tới khi mọi task kết thúc hoặc hết giờ chờ (thoát mã 2, task vẫn chạy trên server)."""
    han, con, cu = time.time() + wait_min * 60, list(entries), {}
    loi = False
    while con:
        for e in list(con):
            try:
                t = ark("GET", "/" + e["task_id"])
            except (LoiAPI, OSError) as x:
                print(f"  Lỗi khi hỏi trạng thái {e['task_id']}: {x}; thử lại sau")
                continue
            if t["status"] != cu.get(e["task_id"]):
                cu[e["task_id"]] = t["status"]
                print(f"{datetime.datetime.now():%H:%M:%S}  {e['task_id']}: {t['status']}")
            if t["status"] in XONG:
                try:
                    ket_thuc(shot, root, e, t)
                except OSError as x:  # tải take lỗi: giữ trong sổ chờ, link video sống 24 giờ
                    print(f"  Chưa tải được take ({x}); chạy lại với --resume trong 24 giờ")
                    loi = True
                con.remove(e)
                loi |= t["status"] != "succeeded"
        if con:
            if time.time() > han:
                sys.exit(f"Hết {wait_min:g} phút chờ, {len(con)} task vẫn chạy trên server: chạy lại với --resume")
            time.sleep(15)
    return loi


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Sinh clip Seedance của một shot qua API BytePlus ModelArk")
    ap.add_argument("shot")
    ap.add_argument("--model", default="2.5", choices=list(MODELS))
    ap.add_argument("--no-draft", action="store_true", help="sinh thường, không qua bản nháp")
    ap.add_argument("--final", help="tên take bản nháp 2.5 để sinh bản final 1080p (chỉ khi người dùng chốt)")
    ap.add_argument("--resolution", default="720p", choices=list(KHUNG))
    ap.add_argument("--duration", type=int)
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--wait", type=float, default=60, help="phút chờ tối đa")
    a = ap.parse_args()
    shot = pathlib.Path(a.shot).resolve()
    root = next(p for p in [shot, *shot.parents] if (p / "CLAUDE.md").exists())

    if a.resume:
        entries = doc_cho(shot)
        if not entries:
            sys.exit("Shot này không có task nào đang chờ")
    else:
        p = chuan_bi_final(shot, a) if a.final else chuan_bi(shot, a)
        if a.dry_run:
            return
    can_s3 = any(e.get("uploads") for e in entries) if a.resume else bool(p["videos"]) and not a.final
    thieu = [k for k in ("ARK_API_KEY",) + (("S3_ENDPOINT", "S3_BUCKET", "S3_ACCESS_KEY", "S3_SECRET_KEY")
                                             if can_s3 else ()) if not os.environ.get(k)]
    if thieu:
        sys.exit(f"Chưa đặt biến môi trường: {', '.join(thieu)} (04_PRODUCTION/SEEDANCE.md, mục Sinh qua API)")
    if not a.resume:
        entries = [gui_final(shot, p) if a.final else gui(shot, a, p)]
    sys.exit(1 if cho(shot, root, entries, a.wait) else 0)


if __name__ == "__main__":
    main()
