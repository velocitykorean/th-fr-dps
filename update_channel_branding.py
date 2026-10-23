import os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import config

def generate_youtube_profile_avatar(output_path: str):
    """Generates an 800x800 high-res YouTube profile avatar."""
    size = 800
    img = Image.new("RGBA", (size, size), (10, 12, 18, 255))
    draw = ImageDraw.Draw(img)

    # Load one of the best Freud portraits (e.g. freud_portrait_01.jpg or freud_portrait_02.jpg)
    portrait_path = os.path.join(config.IMAGES_DIR, "freud_portrait_02.jpg")
    if not os.path.exists(portrait_path):
        portrait_path = os.path.join(config.IMAGES_DIR, "freud_portrait_01.jpg")

    raw_p = Image.open(portrait_path).convert("RGBA")
    # Crop central square around Freud's face
    pw, ph = raw_p.size
    crop_size = min(pw, ph)
    # Focus slightly left where Freud is positioned
    left = int((pw - crop_size) * 0.15)
    top = int((ph - crop_size) * 0.1)
    face_crop = raw_p.crop((left, top, left + crop_size, top + crop_size))
    face_crop = face_crop.resize((size, size), Image.Resampling.LANCZOS)

    # Circular mask for portrait
    mask = Image.new("L", (size, size), 0)
    m_draw = ImageDraw.Draw(mask)
    margin = 32
    m_draw.ellipse([(margin, margin), (size - margin, size - margin)], fill=255)

    circular_portrait = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circular_portrait.paste(face_crop, (0, 0), mask)
    img = Image.alpha_composite(img, circular_portrait)
    draw = ImageDraw.Draw(img)

    # Dual Antique Gold Ring Frame
    gold_outer = (218, 165, 32, 255)
    gold_inner = (255, 215, 0, 200)
    draw.ellipse([(margin, margin), (size - margin, size - margin)], outline=gold_outer, width=8)
    draw.ellipse([(margin + 12, margin + 12), (size - margin - 12, size - margin - 12)], outline=gold_inner, width=3)

    # Lower Monogram Plaque
    font_path = config.FONT_PATH if os.path.exists(config.FONT_PATH) else config.FALLBACK_FONT_PATH
    font_title = ImageFont.truetype(font_path, 42)
    font_sub = ImageFont.truetype(font_path, 20)

    pill_w = 440
    pill_h = 76
    pill_x = (size - pill_w) // 2
    pill_y = size - 130

    draw.rounded_rectangle(
        [(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)],
        radius=38,
        fill=(12, 14, 22, 245),
        outline=(218, 165, 32, 240),
        width=3
    )

    t_text = "THE FREUDIAN DEPTHS"
    tb = draw.textbbox((0, 0), t_text, font=ImageFont.truetype(font_path, 28))
    tw = tb[2] - tb[0]
    draw.text(((size - tw) // 2, pill_y + 22), t_text, fill=(255, 215, 0), font=ImageFont.truetype(font_path, 28))

    img.convert("RGB").save(output_path, quality=98)
    print(f"[Branding] YouTube profile avatar saved: {output_path}")
    return output_path

def generate_youtube_channel_banner(output_path: str):
    """
    Generates a 2560x1440 YouTube channel banner with desktop/mobile safe area (1546x423 in center).
    """
    width, height = 2560, 1440
    banner = Image.new("RGBA", (width, height), (8, 10, 15, 255))

    # Base portrait on left: Freud holding cigar
    portrait_path = os.path.join(config.IMAGES_DIR, "freud_portrait_02.jpg")
    if not os.path.exists(portrait_path):
        portrait_path = os.path.join(config.IMAGES_DIR, "freud_portrait_01.jpg")

    raw_p = Image.open(portrait_path).convert("RGBA")
    # Resize portrait to fit banner height
    scale = height / float(raw_p.height)
    new_w = int(raw_p.width * scale)
    scaled_p = raw_p.resize((new_w, height), Image.Resampling.LANCZOS)

    # Paste on left
    banner.paste(scaled_p, (0, 0))

    # Create rich atmospheric darkness gradient extending rightward
    gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for x in range(600, width):
        alpha = int(min(255, ((x - 600) / (width - 1200)) * 255))
        g_draw.line([(x, 0), (x, height)], fill=(8, 10, 15, alpha))
    banner = Image.alpha_composite(banner, gradient)

    draw = ImageDraw.Draw(banner)
    font_path = config.FONT_PATH if os.path.exists(config.FONT_PATH) else config.FALLBACK_FONT_PATH

    # Safe Area: Y center is 720. Safe height is 423 (from Y = 508 to 931). Safe width is 1546 (from X = 507 to 2053)
    # Center text in right zone around X = 1580, Y = 720
    text_center_x = 1580

    # 1. Top Category Pill: [Gold Dot] PSYCHOANALYSIS & THE UNCONSCIOUS MIND
    font_cat = ImageFont.truetype(font_path, 32)
    cat_text = "PSYCHOANALYSIS & THE UNCONSCIOUS MIND"
    cb = draw.textbbox((0, 0), cat_text, font=font_cat)
    cw = cb[2] - cb[0]
    pill_w = cw + 80
    pill_x = text_center_x - (pill_w // 2)
    pill_y = 560

    draw.rounded_rectangle(
        [(pill_x, pill_y), (pill_x + pill_w, pill_y + 54)],
        radius=27,
        fill=(14, 16, 26, 235),
        outline=(218, 165, 32, 220),
        width=2
    )
    draw.ellipse([(pill_x + 22, pill_y + 20), (pill_x + 36, pill_y + 34)], fill=(245, 185, 50))
    draw.text((pill_x + 48, pill_y + 10), cat_text, fill=(240, 235, 225), font=font_cat)

    # 2. Channel Main Title: THE FREUDIAN DEPTHS (Extra Bold 3D Antique Gold)
    font_title = ImageFont.truetype(font_path, 88)
    title_text = "THE FREUDIAN DEPTHS"
    tb = draw.textbbox((0, 0), title_text, font=font_title)
    tw = tb[2] - tb[0]
    tx = text_center_x - (tw // 2)
    ty = 635

    # 3D shadow layers
    for dx, dy in [(4, 6), (3, 5), (2, 4)]:
        draw.text((tx + dx, ty + dy), title_text, fill=(0, 0, 0, 230), font=font_title)
    draw.text((tx - 1, ty - 1), title_text, fill=(15, 18, 25), font=font_title)
    draw.text((tx, ty), title_text, fill=(255, 215, 0), font=font_title)

    # 3. Subtitle Line
    font_sub = ImageFont.truetype(font_path, 36)
    sub_text = "Id, Ego & Superego  •  Dream Analysis  •  Human Desire  •  Civilization"
    sb = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw = sb[2] - sb[0]
    sx = text_center_x - (sw // 2)
    sy = 750
    draw.text((sx + 2, sy + 2), sub_text, fill=(0, 0, 0, 220), font=font_sub)
    draw.text((sx, sy), sub_text, fill=(235, 225, 210), font=font_sub)

    # 4. Schedule Tag: • NEW EXPLORATIONS WEEKLY •
    font_sched = ImageFont.truetype(font_path, 26)
    sched_text = "• IN-DEPTH PHILOSOPHICAL DISCOURSES RELEASED WEEKLY •"
    scb = draw.textbbox((0, 0), sched_text, font=font_sched)
    scw = scb[2] - scb[0]
    scx = text_center_x - (scw // 2)
    scy = 825
    draw.text((scx, scy), sched_text, fill=(218, 165, 32), font=font_sched)

    banner.convert("RGB").save(output_path, quality=96)
    print(f"[Branding] YouTube channel banner saved: {output_path}")
    return output_path

def update_youtube_channel_metadata(avatar_path: str = None, banner_path: str = None):
    """Updates YouTube channel description and banner via YouTube Data API v3."""
    with open(os.path.join(config.BASE_DIR, "token.json"), "r", encoding="utf-8") as f:
        token_data = json.load(f)

    creds = Credentials(
        None,
        refresh_token=token_data["refresh_token"],
        token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=["https://www.googleapis.com/auth/youtube"]
    )
    creds.refresh(Request())
    yt = build("youtube", "v3", credentials=creds)

    desc = """Welcome to The Freudian Depths — a sanctuary of psychoanalytic inquiry, intellectual courage, and deep psychological exploration.

Here, we descend beneath the polite surfaces of conscious thought into the uncharted labyrinth of the human mind:
• The Architecture of the Unconscious: Id, Ego, and Superego
• The Interpretation of Dreams and nocturnal symbolism
• Defense Mechanisms: Why we deceive ourselves to survive reality
• Civilization and Its Discontents: The tragic bargain of human order
• Eros and Thanatos: The perpetual conflict of Life and Death drives
• The Shadow of Love, Attachment, and Unspoken Childhood Desires
• The Art of Sublimation: Transmuting primitive instincts into culture and genius

"The mind is like an iceberg, it floats with one-seventh of its bulk above water."
— Sigmund Freud

Subscribe to join our psychoanalytic circle as we illuminate the hidden motives that govern human destiny.

New in-depth philosophical and psychoanalytic explorations released weekly.

Official Handle: @thefreudiandepths"""

    # 1. Update Channel Description & Keywords
    print("[YouTube API] Updating channel description and keywords...")
    try:
        yt.channels().update(
            part="brandingSettings",
            body={
                "id": "UCFaKh33OLae6KP2I8bLmpxQ",
                "brandingSettings": {
                    "channel": {
                        "description": desc,
                        "keywords": "Sigmund Freud Psychoanalysis Psychology Unconscious Id Ego Superego Dreams Philosophy"
                    }
                }
            }
        ).execute()
        print("[YouTube API] Successfully updated channel description!")
    except Exception as e:
        print(f"[YouTube API Warning] brandingSettings update error: {e}")

    # 2. Upload Channel Banner if provided
    if banner_path and os.path.exists(banner_path):
        print("[YouTube API] Uploading channel banner to YouTube...")
        try:
            media = MediaFileUpload(banner_path, mimetype="image/jpeg", resumable=True)
            banner_res = yt.channelBanners().insert(body={}, media_body=media).execute()
            banner_url = banner_res.get("url")
            print(f"[YouTube API] Channel banner uploaded: {banner_url}")

            if banner_url:
                yt.channels().update(
                    part="brandingSettings",
                    body={
                        "id": "UCFaKh33OLae6KP2I8bLmpxQ",
                        "brandingSettings": {
                            "image": {
                                "bannerExternalUrl": banner_url
                            }
                        }
                    }
                ).execute()
                print("[YouTube API] Successfully set channel bannerExternalUrl!")
        except Exception as e:
            print(f"[YouTube API Warning] Banner upload error: {e}")

if __name__ == "__main__":
    avatar_p = os.path.join(config.ASSETS_DIR, "youtube_avatar_800.jpg")
    banner_p = os.path.join(config.ASSETS_DIR, "youtube_banner_2560.jpg")

    print("[Step 1/3] Generating YouTube 800x800 Profile Avatar...")
    generate_youtube_profile_avatar(avatar_p)

    print("[Step 2/3] Generating YouTube 2560x1440 Channel Banner...")
    generate_youtube_channel_banner(banner_p)

    print("[Step 3/3] Updating YouTube Channel Metadata & Uploading Branding...")
    update_youtube_channel_metadata(avatar_path=avatar_p, banner_path=banner_p)
