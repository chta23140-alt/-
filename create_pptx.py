from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# カラーパレット
BLUE_DARK  = RGBColor(0x00, 0x3D, 0x7A)
BLUE_MID   = RGBColor(0x00, 0x57, 0xA8)
BLUE_LIGHT = RGBColor(0xE8, 0xF0, 0xFB)
GREEN      = RGBColor(0x00, 0xA8, 0x6B)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_TEXT  = RGBColor(0x55, 0x55, 0x77)
DARK_TEXT  = RGBColor(0x1A, 0x1A, 0x2E)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]  # blank


def add_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=None):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, left, top, width, height,
             font_size=18, bold=False, color=DARK_TEXT,
             align=PP_ALIGN.LEFT, wrap=True):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Meiryo"
    return txBox


# =========================================================
# スライド 1: タイトル
# =========================================================
slide = prs.slides.add_slide(BLANK)

# 背景グラデーション風（2矩形）
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=BLUE_DARK)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=RGBColor(0x00, 0x55, 0xA0))  # 上書きで単色

# アクセント丸
circle = slide.shapes.add_shape(9, Inches(9.5), Inches(-1), Inches(6), Inches(6))
circle.fill.solid()
circle.fill.fore_color.rgb = RGBColor(0x00, 0x6E, 0xC8)
circle.line.fill.background()

circle2 = slide.shapes.add_shape(9, Inches(10.5), Inches(3.5), Inches(4), Inches(4))
circle2.fill.solid()
circle2.fill.fore_color.rgb = RGBColor(0x00, 0x4F, 0x90)
circle2.line.fill.background()

# ロゴ文字
add_text(slide, "フコクhemix", 1, 1.8, 8, 1.2, font_size=52, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

# サブタイトル
add_text(slide, "株式会社", 1, 3.0, 6, 0.6, font_size=24, bold=False, color=RGBColor(0xBB, 0xD6, 0xFF), align=PP_ALIGN.LEFT)

# キャッチコピー
add_rect(slide, 1, 3.9, 0.05, 1.0, fill_color=GREEN)
add_text(slide, "化学の力で、未来をひらく", 1.2, 3.85, 9, 0.8, font_size=20, bold=False, color=RGBColor(0xCC, 0xE5, 0xFF), align=PP_ALIGN.LEFT)

# 日付
add_text(slide, "2026年3月", 1, 6.5, 4, 0.5, font_size=14, color=RGBColor(0x88, 0xAA, 0xDD), align=PP_ALIGN.LEFT)


# =========================================================
# スライド 2: 会社概要
# =========================================================
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=WHITE)

# ヘッダーバー
add_rect(slide, 0, 0, 13.33, 1.1, fill_color=BLUE_MID)
add_text(slide, "会社概要", 0.5, 0.15, 12, 0.8, font_size=28, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

# アクセントライン
add_rect(slide, 0.5, 1.4, 0.08, 0.6, fill_color=BLUE_MID)

# 概要テキスト
add_text(slide, "フコクhemix株式会社は、高機能化学品の研究・開発・製造・販売を行う専門メーカーです。\n創業以来、化学の力で社会課題を解決し、持続可能な社会の実現に貢献しています。",
         0.7, 1.3, 12, 1.0, font_size=15, color=GRAY_TEXT, align=PP_ALIGN.LEFT)

# 情報ボックス
items = [
    ("会社名",    "フコクhemix株式会社"),
    ("設立",      "1975年4月"),
    ("資本金",    "5億円"),
    ("従業員数",  "850名（2024年4月現在）"),
    ("本社",      "東京都千代田区丸の内1-1-1"),
    ("事業内容",  "化学品の製造・販売、研究開発"),
]
for i, (label, value) in enumerate(items):
    row = i // 2
    col = i % 2
    x = 0.5 + col * 6.3
    y = 2.6 + row * 1.4
    add_rect(slide, x, y, 5.9, 1.1, fill_color=BLUE_LIGHT)
    add_text(slide, label, x + 0.2, y + 0.05, 5.5, 0.4, font_size=11, bold=True, color=BLUE_MID)
    add_text(slide, value, x + 0.2, y + 0.48, 5.5, 0.5, font_size=14, bold=False, color=DARK_TEXT)


# =========================================================
# スライド 3: 数字で見るフコクhemix
# =========================================================
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=RGBColor(0xF5, 0xF7, 0xFA))

add_rect(slide, 0, 0, 13.33, 1.1, fill_color=BLUE_MID)
add_text(slide, "数字で見るフコクhemix", 0.5, 0.15, 12, 0.8, font_size=28, bold=True, color=WHITE)

stats = [
    ("50", "年", "創業からの歴史"),
    ("1,200+", "社", "取引先企業数"),
    ("300+", "品", "製品ラインナップ"),
    ("15", "拠点", "国内外の拠点数"),
]
for i, (num, unit, label) in enumerate(stats):
    x = 0.5 + i * 3.1
    add_rect(slide, x, 1.5, 2.8, 4.5, fill_color=WHITE)
    add_rect(slide, x, 1.5, 2.8, 0.12, fill_color=BLUE_MID)
    add_text(slide, num, x, 2.2, 2.8, 1.4, font_size=48, bold=True, color=BLUE_DARK, align=PP_ALIGN.CENTER)
    add_text(slide, unit, x, 3.6, 2.8, 0.6, font_size=20, bold=False, color=BLUE_MID, align=PP_ALIGN.CENTER)
    add_text(slide, label, x, 4.5, 2.8, 0.8, font_size=14, bold=False, color=GRAY_TEXT, align=PP_ALIGN.CENTER)


# =========================================================
# スライド 4: 製品・サービス
# =========================================================
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=WHITE)

add_rect(slide, 0, 0, 13.33, 1.1, fill_color=BLUE_MID)
add_text(slide, "製品・サービス", 0.5, 0.15, 12, 0.8, font_size=28, bold=True, color=WHITE)

products = [
    ("🔬", "機能性化学品",  "各種産業向けの高機能化学品"),
    ("⚗️", "工業用薬品",   "製造プロセス効率化・品質向上"),
    ("🌱", "環境対応製品", "グリーンケミストリー製品群"),
    ("💊", "医薬・食品向け", "高純度・高品質の原料・添加物"),
    ("🔋", "電子材料",     "半導体・ディスプレイ向け材料"),
    ("🛠️", "カスタム合成",  "オーダーメイド化学品合成"),
]
for i, (icon, title, desc) in enumerate(products):
    row = i // 3
    col = i % 3
    x = 0.4 + col * 4.2
    y = 1.4 + row * 2.7
    add_rect(slide, x, y, 3.8, 2.3, fill_color=BLUE_LIGHT)
    add_text(slide, icon,  x + 0.15, y + 0.15, 0.8, 0.7, font_size=28)
    add_text(slide, title, x + 0.15, y + 0.85, 3.5, 0.5, font_size=14, bold=True, color=BLUE_DARK)
    add_text(slide, desc,  x + 0.15, y + 1.35, 3.5, 0.7, font_size=11, color=GRAY_TEXT)


# =========================================================
# スライド 5: 技術力
# =========================================================
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=DARK_TEXT)

add_rect(slide, 0, 0, 13.33, 1.1, fill_color=BLUE_DARK)
add_text(slide, "技術力", 0.5, 0.15, 12, 0.8, font_size=28, bold=True, color=WHITE)

techs = [
    ("01", "先端合成技術",        "独自の触媒技術・精密合成技術により、高純度・高機能な化学品を効率よく製造します。"),
    ("02", "品質管理システム",    "ISO認証取得の品質管理体制で、お客様に安心・安全な製品をお届けします。"),
    ("03", "グリーンケミストリー","環境に配慮したプロセス開発・製品設計で、持続可能な化学産業を目指します。"),
    ("04", "分析・評価技術",      "最新の分析機器と専門知識により、製品の性能・安全性を徹底的に評価します。"),
]
for i, (num, title, desc) in enumerate(techs):
    col = i % 2
    row = i // 2
    x = 0.5 + col * 6.4
    y = 1.4 + row * 2.7
    add_rect(slide, x, y, 6.0, 2.3, fill_color=RGBColor(0x2A, 0x2A, 0x44))
    add_rect(slide, x, y, 0.08, 2.3, fill_color=BLUE_MID)
    add_text(slide, num,   x + 0.25, y + 0.15, 1.2, 0.8, font_size=32, bold=True, color=BLUE_MID)
    add_text(slide, title, x + 0.25, y + 0.9,  5.5, 0.5, font_size=15, bold=True, color=WHITE)
    add_text(slide, desc,  x + 0.25, y + 1.4,  5.5, 0.8, font_size=11, color=RGBColor(0xAA, 0xBB, 0xDD))


# =========================================================
# スライド 6: お問い合わせ
# =========================================================
slide = prs.slides.add_slide(BLANK)
add_rect(slide, 0, 0, 13.33, 7.5, fill_color=BLUE_DARK)

circle3 = slide.shapes.add_shape(9, Inches(-1), Inches(-1), Inches(7), Inches(7))
circle3.fill.solid()
circle3.fill.fore_color.rgb = RGBColor(0x00, 0x4F, 0x90)
circle3.line.fill.background()

add_text(slide, "お問い合わせ", 1, 1.2, 11, 1.0, font_size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide, "製品・サービスに関するご質問はお気軽にどうぞ",
         1, 2.2, 11, 0.6, font_size=16, color=RGBColor(0xBB, 0xD6, 0xFF), align=PP_ALIGN.CENTER)

# アクセントライン
add_rect(slide, 5.5, 3.0, 2.3, 0.06, fill_color=GREEN)

contacts = [
    ("📞 電話",  "03-1234-5678",              "平日 9:00〜17:30"),
    ("✉️ メール", "info@fukoku-hemix.co.jp",   "24時間受付"),
    ("📍 本社",  "東京都千代田区丸の内1-1-1", "〒100-0005"),
]
for i, (label, value, note) in enumerate(contacts):
    x = 0.8 + i * 4.1
    add_rect(slide, x, 3.3, 3.7, 2.8, fill_color=RGBColor(0x00, 0x2D, 0x5E))
    add_text(slide, label, x + 0.2, 3.5,  3.3, 0.5, font_size=13, bold=True, color=RGBColor(0x88, 0xCC, 0xFF))
    add_text(slide, value, x + 0.2, 4.1,  3.3, 0.6, font_size=13, bold=False, color=WHITE)
    add_text(slide, note,  x + 0.2, 4.85, 3.3, 0.5, font_size=11, color=RGBColor(0x88, 0xAA, 0xCC))

add_text(slide, "フコクhemix株式会社", 0, 6.7, 13.33, 0.5, font_size=13,
         color=RGBColor(0x66, 0x88, 0xBB), align=PP_ALIGN.CENTER)


prs.save("/home/user/-/fukoku_hemix.pptx")
print("Done: fukoku_hemix.pptx")
