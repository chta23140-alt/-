from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# フォント登録
FONT_PATHS = [
    "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf",
    "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf",
    "/usr/share/fonts/truetype/ipafont-gothic/ipagp.ttf",
    "/usr/share/fonts/truetype/ipafont/ipagp.ttf",
]
FONT_NAME = "Japanese"
registered = False
for fp in FONT_PATHS:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont(FONT_NAME, fp))
            registered = True
            print(f"Font: {fp}")
            break
        except:
            continue

if not registered:
    # フォントなしでも動くようHelveticaにフォールバック
    FONT_NAME = "Helvetica"
    print("Fallback to Helvetica")

W, H = landscape(A4)  # 297 x 210 mm → points: 841.9 x 595.3

# カラー
C_BLUE_DARK  = HexColor("#003D7A")
C_BLUE_MID   = HexColor("#0057A8")
C_BLUE_LIGHT = HexColor("#E8F0FB")
C_GREEN      = HexColor("#00A86B")
C_TEXT       = HexColor("#1A1A2E")
C_GRAY       = HexColor("#555577")
C_BG_GRAY    = HexColor("#F5F7FA")
C_DARK_BG    = HexColor("#1A1A2E")
C_WHITE      = white


def draw_rect(c, x, y, w, h, fill=None, stroke=None):
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    else:
        c.setStrokeColor(fill or C_WHITE)
    c.rect(x, y, w, h, fill=1 if fill else 0, stroke=1 if stroke else 0)


def draw_text(c, text, x, y, size=12, bold=False, color=C_TEXT, align="left", max_width=None):
    c.setFillColor(color)
    fname = FONT_NAME
    c.setFont(fname, size)
    if align == "center" and max_width:
        tw = c.stringWidth(text, fname, size)
        x = x + (max_width - tw) / 2
    elif align == "right" and max_width:
        tw = c.stringWidth(text, fname, size)
        x = x + max_width - tw
    c.drawString(x, y, text)


def slide_header(c, title):
    draw_rect(c, 0, H - 70, W, 70, fill=C_BLUE_MID)
    draw_text(c, title, 30, H - 48, size=26, bold=True, color=C_WHITE)


# =========================================================
# PDF生成
# =========================================================
pdf_path = "/home/user/-/fukoku_hemix.pdf"
c = canvas.Canvas(pdf_path, pagesize=landscape(A4))


# --- スライド1: タイトル ---
draw_rect(c, 0, 0, W, H, fill=C_BLUE_MID)
# デコ円
c.setFillColor(HexColor("#0066C0"))
c.circle(W - 60, H - 20, 220, fill=1, stroke=0)
c.setFillColor(HexColor("#004F90"))
c.circle(W - 30, 80, 150, fill=1, stroke=0)

draw_text(c, "フコクhemix", 60, H/2 + 60, size=54, bold=True, color=C_WHITE)
draw_text(c, "株式会社", 65, H/2 + 10, size=22, color=HexColor("#BBDDFF"))
draw_rect(c, 60, H/2 - 30, 6, 60, fill=C_GREEN)
draw_text(c, "化学の力で、未来をひらく", 80, H/2 - 18, size=18, color=HexColor("#CCE5FF"))
draw_text(c, "2026年3月", 62, 40, size=13, color=HexColor("#88AADD"))
c.showPage()


# --- スライド2: 会社概要 ---
draw_rect(c, 0, 0, W, H, fill=C_WHITE)
slide_header(c, "会社概要")
draw_text(c, "フコクhemix株式会社は、高機能化学品の研究・開発・製造・販売を行う専門メーカーです。", 30, H - 110, size=12, color=C_GRAY)
draw_text(c, "創業以来、化学の力で社会課題を解決し、持続可能な社会の実現に貢献しています。", 30, H - 130, size=12, color=C_GRAY)

items = [
    ("会社名",   "フコクhemix株式会社"),
    ("設立",     "1975年4月"),
    ("資本金",   "5億円"),
    ("従業員数", "850名（2024年4月現在）"),
    ("本社",     "東京都千代田区丸の内1-1-1"),
    ("事業内容", "化学品の製造・販売、研究開発"),
]
col_w = (W - 60) / 2
for i, (label, val) in enumerate(items):
    col = i % 2
    row = i // 2
    bx = 30 + col * (col_w + 10)
    by = H - 220 - row * 80
    draw_rect(c, bx, by, col_w - 10, 65, fill=C_BLUE_LIGHT)
    draw_text(c, label, bx + 10, by + 38, size=10, bold=True, color=C_BLUE_MID)
    draw_text(c, val,   bx + 10, by + 14, size=13, color=C_TEXT)
c.showPage()


# --- スライド3: 数字 ---
draw_rect(c, 0, 0, W, H, fill=C_BG_GRAY)
slide_header(c, "数字で見るフコクhemix")

stats = [
    ("50",     "年",  "創業からの歴史"),
    ("1,200+", "社",  "取引先企業数"),
    ("300+",   "品",  "製品ラインナップ"),
    ("15",     "拠点","国内外の拠点数"),
]
bw = (W - 80) / 4
for i, (num, unit, label) in enumerate(stats):
    bx = 30 + i * (bw + 8)
    by = 80
    bh = H - 160
    draw_rect(c, bx, by, bw, bh, fill=C_WHITE)
    draw_rect(c, bx, by + bh - 6, bw, 6, fill=C_BLUE_MID)
    # 数字
    draw_text(c, num,   bx, by + bh/2 + 20, size=44, bold=True, color=C_BLUE_DARK, align="center", max_width=bw)
    draw_text(c, unit,  bx, by + bh/2 - 20, size=18, color=C_BLUE_MID, align="center", max_width=bw)
    draw_text(c, label, bx, by + 20,         size=12, color=C_GRAY,     align="center", max_width=bw)
c.showPage()


# --- スライド4: 製品・サービス ---
draw_rect(c, 0, 0, W, H, fill=C_WHITE)
slide_header(c, "製品・サービス")

products = [
    ("機能性化学品",  "各種産業向けの高機能化学品"),
    ("工業用薬品",   "製造プロセス効率化・品質向上"),
    ("環境対応製品", "グリーンケミストリー製品群"),
    ("医薬・食品向け","高純度・高品質の原料・添加物"),
    ("電子材料",     "半導体・ディスプレイ向け材料"),
    ("カスタム合成",  "オーダーメイド化学品合成"),
]
cw = (W - 80) / 3
ch = (H - 140) / 2
for i, (title, desc) in enumerate(products):
    col = i % 3
    row = i // 2
    bx = 30 + col * (cw + 10)
    by = H - 95 - (row + 1) * (ch + 10)
    draw_rect(c, bx, by, cw, ch, fill=C_BLUE_LIGHT)
    draw_rect(c, bx, by + ch - 5, cw, 5, fill=C_BLUE_MID)
    draw_text(c, title, bx + 12, by + ch - 38, size=14, bold=True, color=C_BLUE_DARK)
    draw_text(c, desc,  bx + 12, by + ch - 62, size=11, color=C_GRAY)
c.showPage()


# --- スライド5: 技術力 ---
draw_rect(c, 0, 0, W, H, fill=C_DARK_BG)
slide_header(c, "技術力")

techs = [
    ("01", "先端合成技術",         "独自の触媒技術・精密合成技術により、高純度・高機能な化学品を効率よく製造します。"),
    ("02", "品質管理システム",     "ISO認証取得の品質管理体制で、お客様に安心・安全な製品をお届けします。"),
    ("03", "グリーンケミストリー", "環境に配慮したプロセス開発・製品設計で、持続可能な化学産業を目指します。"),
    ("04", "分析・評価技術",       "最新の分析機器と専門知識により、製品の性能・安全性を徹底的に評価します。"),
]
bw2 = (W - 80) / 2
bh2 = (H - 150) / 2
for i, (num, title, desc) in enumerate(techs):
    col = i % 2
    row = i // 2
    bx = 30 + col * (bw2 + 10)
    by = H - 100 - (row + 1) * (bh2 + 10)
    draw_rect(c, bx, by, bw2, bh2, fill=HexColor("#2A2A44"))
    draw_rect(c, bx, by, 6, bh2, fill=C_BLUE_MID)
    draw_text(c, num,   bx + 18, by + bh2 - 45, size=30, bold=True, color=C_BLUE_MID)
    draw_text(c, title, bx + 18, by + bh2 - 75, size=14, bold=True, color=C_WHITE)
    draw_text(c, desc,  bx + 18, by + 18,        size=10, color=HexColor("#AABBDD"))
c.showPage()


# --- スライド6: お問い合わせ ---
draw_rect(c, 0, 0, W, H, fill=C_BLUE_DARK)
c.setFillColor(HexColor("#004F90"))
c.circle(-60, H + 40, 220, fill=1, stroke=0)

draw_text(c, "お問い合わせ", 0, H/2 + 80, size=34, bold=True, color=C_WHITE, align="center", max_width=W)
draw_text(c, "製品・サービスに関するご質問はお気軽にどうぞ",
          0, H/2 + 35, size=14, color=HexColor("#BBD6FF"), align="center", max_width=W)
draw_rect(c, W/2 - 50, H/2 + 20, 100, 4, fill=C_GREEN)

contacts = [
    ("電話",  "03-1234-5678",              "平日 9:00〜17:30"),
    ("メール","info@fukoku-hemix.co.jp",   "24時間受付"),
    ("本社",  "東京都千代田区丸の内1-1-1","〒100-0005"),
]
cw3 = (W - 100) / 3
for i, (label, val, note) in enumerate(contacts):
    bx = 30 + i * (cw3 + 20)
    by = 80
    bh3 = H/2 - 40
    draw_rect(c, bx, by, cw3, bh3, fill=HexColor("#002D5E"))
    draw_text(c, label, bx + 12, by + bh3 - 38, size=13, bold=True, color=HexColor("#88CCFF"))
    draw_text(c, val,   bx + 12, by + bh3 - 68, size=12, color=C_WHITE)
    draw_text(c, note,  bx + 12, by + 16,        size=10, color=HexColor("#88AACC"))

draw_text(c, "フコクhemix株式会社", 0, 20, size=12, color=HexColor("#6688BB"), align="center", max_width=W)
c.showPage()


c.save()
print(f"Done: {pdf_path}")
