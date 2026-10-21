#!/usr/bin/env python3
"""Original clarify release artwork. Writes NEW files only; never overwrites.

Run from the repository root with the system Python:
    /usr/bin/python3 -B assets/source/render-artwork.py
Requires system PyGObject/librsvg, Pycairo and Pillow. Fonts: Fira Code and Lato.
Proofs go to assets/artwork-qa; final paths are reserved until visual review.
Re-renders must use a NEW --variant name, never replace an earlier source/proof.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

import cairo
import gi
gi.require_version('Rsvg', '2.0')
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Rsvg, Pango, PangoCairo
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PAPER = '#F4F4EB'
INK = '#16342D'
MINT = '#BDE8CE'
MUTED = '#53695F'
RULE = '#CDD6CA'
MONO = 'Fira Code'
SANS = 'Lato'
TAGLINE = 'Rough request in. Clear prompt back in your prompt box, unsent.'
ROUGH = 'fix the login loop on safari, dont touch the api --clarify'
CLEAR = 'Fix the login redirect loop that happens in Safari. Do not change the API. Before editing, find where the redirect is triggered and explain the cause.'


def write_new(path: Path, data: bytes | str) -> None:
    path.resolve().relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        expected = data if isinstance(data, bytes) else data.encode()
        if path.read_bytes() == expected:
            return  # Resume an interrupted run without modifying the file.
        raise FileExistsError(f'Refusing to change existing file: {path}')
    with path.open('xb' if isinstance(data, bytes) else 'x') as file:
        file.write(data)


def text(x, y, value, size=24, fill=INK, family=SANS, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" {extra}>{escape(value)}</text>'


def rect(x, y, w, h, fill, radius=0, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" {extra}/>'


def line(x1, y1, x2, y2, stroke=RULE, width=1, extra=''):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{stroke}" stroke-width="{width}" {extra}/>' if y1 == y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def mark(transform='', stroke=26):
    # An original, non-letterform knot resolves into a line and insertion caret.
    return f'''<g transform="{transform}" fill="none" stroke-linecap="round" stroke-linejoin="round">
<path d="M108 291 C54 249 82 171 144 169 C214 167 237 265 177 299 C117 333 89 267 133 237 C181 204 221 253 259 271 C278 280 291 280 314 280" stroke="{PAPER}" stroke-width="{stroke}"/>
<path d="M314 280H378" stroke="{MINT}" stroke-width="{stroke}"/>
<rect x="414" y="196" width="28" height="168" rx="6" fill="{MINT}" stroke="none"/>
</g>'''


def svg(width, height, title, desc, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<style>text {{ font-variant-ligatures: none; }}</style>
{body}
</svg>'''


def make_icon():
    return svg(1024, 1024, 'clarify icon', 'An original tangled line resolves into a straight line and an insertion caret. No lettering.',
        '<g transform="scale(2)">' + rect(0, 0, 512, 512, INK) + rect(8, 8, 496, 496, 'none', 0, 'stroke="#527768" stroke-width="2"') + mark() + '</g>')


def make_banner():
    body = rect(0, 0, 1600, 640, PAPER)
    body += rect(16, 16, 1568, 608, 'none', 28, f'stroke="{RULE}" stroke-width="2"')
    body += text(72, 90, 'A LITTLE CLARITY, BEFORE ENTER.', 20, MUTED, MONO, extra='letter-spacing="1"')
    body += text(1528, 90, 'OPEN SOURCE / MIT', 20, MUTED, MONO, extra='text-anchor="end"')
    body += text(64, 278, 'clarify', 158, INK, MONO, 500, 'letter-spacing="-9" data-copy="wordmark"')
    body += f'<text x="72" y="352" font-family="{SANS}" font-size="36" fill="{INK}" data-copy="tagline">'
    for i, value in enumerate(['Rough request in. ', 'Clear prompt back in your ', 'prompt box, unsent.']):
        body += f'<tspan x="72" y="{352+i*48}">{escape(value)}</tspan>'
    body += '</text>'
    # The illustration is a deliberately schematic prompt field, not a screenshot.
    body += rect(992, 146, 536, 342, INK, 24)
    body += text(1028, 190, 'PROMPT BOX', 20, MINT, MONO, extra='letter-spacing="1.2"')
    body += rect(1376, 167, 120, 32, 'none', 16, f'stroke="#527768" stroke-width="1.5"')
    body += text(1436, 189, 'UNSENT', 20, MINT, MONO, extra='text-anchor="middle"')
    body += line(1028, 218, 1492, 218, '#3A574B', 1)
    body += line(1042, 360, 1490, 360, '#3A574B', 1, 'stroke-dasharray="3 9"')
    body += mark('translate(978,80)', 16)
    body += text(1028, 460, 'ready for your review', 20, MINT, MONO)
    body += line(72, 536, 1528, 536)
    body += rect(72, 558, 154, 36, INK, 7)
    body += text(149, 583, '--clarify', 20, PAPER, MONO, extra='text-anchor="middle"')
    body += text(246, 583, 'or /clarify <request>', 22, MUTED, MONO)
    body += text(1528, 583, 'Your words. Your final say.', 24, INK, SANS, extra='text-anchor="end"')
    return svg(1600, 640, 'clarify', TAGLINE, body)


def prompt_text(x, y, lines, role):
    full = ROUGH if role == 'rough' else CLEAR
    assert ' '.join(lines) == full
    out = f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="28" fill="{PAPER}" data-copy="{role}">'
    for i, value in enumerate(lines):
        content = escape(value + (' ' if i < len(lines)-1 else ''))
        if role == 'rough':
            content = content.replace('--clarify', f'<tspan fill="{MINT}">--clarify</tspan>')
        out += f'<tspan x="{x}" y="{y+i*40}">{content}</tspan>'
    return out + '</text>'


def make_flow():
    left_lines = ['fix the login loop on safari,', 'dont touch the api --clarify']
    right_lines = ['Fix the login redirect loop that', 'happens in Safari. Do not change', 'the API. Before editing, find', 'where the redirect is triggered', 'and explain the cause.']
    body = rect(0, 0, 1600, 900, PAPER)
    body += rect(16, 16, 1568, 868, 'none', 28, f'stroke="{RULE}" stroke-width="2"')
    body += text(64, 76, 'THE PROMPT STAYS WITH YOU', 20, MUTED, MONO, extra='letter-spacing="1.2"')
    body += text(1536, 76, 'ILLUSTRATED FLOW', 20, MUTED, MONO, extra='text-anchor="end"')
    body += text(60, 153, 'A rewrite. Not a send.', 64, INK, SANS, 700)
    body += text(64, 204, 'The same prompt box, before and after clarify.', 27, MUTED)
    for x, n, label in [(64, '01', 'ROUGH REQUEST'), (886, '02', 'CLEARER DRAFT')]:
        body += rect(x, 257, 42, 32, 'none', 8, f'stroke="{RULE}" stroke-width="1.5"')
        body += text(x+21, 280, n, 17, MUTED, MONO, extra='text-anchor="middle"')
        body += text(x+58, 280, label, 19, INK, MONO, 500, 'letter-spacing="0.5"')
        body += rect(x, 314, 650, 376, INK, 22)
        body += text(x+34, 353, 'PROMPT BOX', 20, MINT, MONO, extra='letter-spacing="0.8"')
        body += line(x+34, 377, x+616, 377, '#3A574B', 1)
        body += text(x+614, 353, 'draft', 18, '#95B8A7', MONO, extra='text-anchor="end"')
    body += rect(1404, 255, 132, 34, '#DCEBDD', 17)
    body += text(1470, 279, 'UNSENT', 20, INK, MONO, 500, 'text-anchor="middle"')
    body += prompt_text(98, 430, left_lines, 'rough')
    body += prompt_text(920, 430, right_lines, 'clear')
    # Insertion cursor is deliberately small and never a send/checkmark icon.
    last_line_width = measure(right_lines[-1], MONO, 28)[0]
    body += rect(920 + last_line_width + 5, 566, 3, 28, MINT, 1)
    body += text(98, 657, 'trailing flag requests a rewrite', 20, '#AACAB9', MONO)
    body += text(920, 657, 'press Enter to send', 20, MINT, MONO)
    # One directional connector explains a temporal change in the same box.
    body += text(800, 468, 'clarify', 20, INK, MONO, 500, 'text-anchor="middle"')
    body += line(746, 502, 852, 502, MUTED, 2.5)
    body += f'<path d="M841 492L853 502L841 512" fill="none" stroke="{MUTED}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    body += text(800, 540, 'in place', 18, MUTED, MONO, extra='text-anchor="middle"')
    body += line(64, 754, 1536, 754)
    body += text(64, 817, 'You decide what gets sent.', 32, INK, SANS, 700)
    body += text(1536, 817, 'Read it. Edit it. Then press Enter.', 25, MUTED, SANS, extra='text-anchor="end"')
    return svg(1600, 900, 'A rough request becomes a clearer, unsent draft', 'Illustration, not a product screenshot. Rough draft: ' + ROUGH + ' Rewritten draft: ' + CLEAR + ' The rewritten draft remains unsent; press Enter to send.', body)


def measure(value, family, size, weight=400):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
    context = cairo.Context(surface)
    layout = PangoCairo.create_layout(context)
    font = Pango.FontDescription()
    font.set_family(family)
    font.set_absolute_size(size * Pango.SCALE)
    font.set_weight(weight)
    layout.set_font_description(font)
    layout.set_text(value, -1)
    return layout.get_pixel_size()


def render(source, width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width*2, height*2)
    context = cairo.Context(surface)
    handle = Rsvg.Handle.new_from_data(source.encode())
    viewport = Rsvg.Rectangle()
    viewport.x, viewport.y, viewport.width, viewport.height = 0, 0, width*2, height*2
    handle.render_document(context, viewport)
    buffer = io.BytesIO()
    surface.write_to_png(buffer)
    image = Image.open(io.BytesIO(buffer.getvalue())).convert('RGB')
    return image.resize((width, height), Image.Resampling.LANCZOS)


def png_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, format='PNG', optimize=True, compress_level=9)
    return buffer.getvalue()


def luminance(hex_color):
    values = [int(hex_color[i:i+2], 16) / 255 for i in [1, 3, 5]]
    values = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(v*w for v,w in zip(values, [.2126, .7152, .0722]))


def contrast(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi+.05)/(lo+.05)


def make_sheet(images):
    # Real 32 px/64 px samples, followed by contextual README renders at 800 px.
    canvas = Image.new('RGB', (1744, 1330), '#E7EBE5')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 18)
    for column, bg in enumerate(['#FFFFFF', '#0D1117']):
        x = 32 + column*856
        draw.rounded_rectangle((x, 28, x+824, 1298), radius=16, fill=bg)
        fg = '#53695F' if column == 0 else '#BDE8CE'
        draw.text((x+20, 48), 'GITHUB LIGHT' if column == 0 else 'GITHUB DARK', font=font, fill=fg)
        for i, size in enumerate([32, 64, 128]):
            icon = images['icon'].resize((size,size), Image.Resampling.LANCZOS)
            px = x+24+i*170
            canvas.paste(icon, (px, 110))
            draw.text((px, 254), f'{size}px', font=font, fill=fg)
        draw.text((x+20, 314), 'README BANNER / 800 px', font=font, fill=fg)
        canvas.paste(images['banner'].resize((800,320), Image.Resampling.LANCZOS), (x+12,350))
        draw.text((x+20, 708), 'FLOW / 800 px', font=font, fill=fg)
        canvas.paste(images['before-after'].resize((800,450), Image.Resampling.LANCZOS), (x+12,744))
    return canvas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', default='v2')
    args = parser.parse_args()
    if not args.variant.replace('-', '').isalnum():
        raise SystemExit('Use an alphanumeric variant name.')
    source_dir = ROOT / 'assets/source' / args.variant
    proof_dir = ROOT / 'assets/artwork-qa' / args.variant
    targets = [source_dir / f'{name}.svg' for name in ['icon','banner','before-after']] + [proof_dir / f'{name}.png' for name in ['icon','banner','before-after','theme-and-size-review']] + [proof_dir / 'checks.json']
    if any(path.exists() for path in targets if path.suffix != '.svg'):
        raise SystemExit('Refusing to overwrite a proof. Select a NEW --variant.')
    specs = [('icon', 1024, 1024, make_icon()), ('banner', 1600, 640, make_banner()), ('before-after', 1600, 900, make_flow())]
    images = {}
    checks = {'renderer': f'librsvg {Rsvg.MAJOR_VERSION}.{Rsvg.MINOR_VERSION}.{Rsvg.MICRO_VERSION} / Cairo {cairo.cairo_version_string()} / Pillow {Image.__version__}', 'supersampling': '2x, LANCZOS reduction', 'assets': {}, 'exact_copy': {}, 'contrast_ratios': {}, 'type_widths': {}}
    for name, width, height, source in specs:
        root = ET.fromstring(source)
        for node in root.iter():
            if 'data-copy' in node.attrib:
                key = node.attrib['data-copy']
                actual = ''.join(node.itertext())
                expected = {'wordmark':'clarify', 'tagline':TAGLINE, 'rough':ROUGH, 'clear':CLEAR}[key]
                assert actual == expected, (key, actual, expected)
                checks['exact_copy'][key] = {'pass': True, 'text': actual}
        if name == 'icon':
            assert not root.findall('.//{http://www.w3.org/2000/svg}text')
        write_new(source_dir / f'{name}.svg', source)
        image = render(source, width, height)
        images[name] = image
        data = png_bytes(image)
        assert name != 'icon' or len(data) < 2_000_000
        write_new(proof_dir / f'{name}.png', data)
        checks['assets'][name] = {'width':width, 'height':height, 'bytes':len(data), 'mode':image.mode, 'sha256':hashlib.sha256(data).hexdigest(), 'opaque':True}
    for label, value, family, size, limit in [('tagline line 2', 'Clear prompt back in your', SANS, 36, 840), ('rough line 1', 'fix the login loop on safari,', MONO, 28, 582), ('clear longest line', 'Fix the login redirect loop that', MONO, 28, 582), ('footer left', 'You decide what gets sent.', SANS, 32, 800)]:
        width, height = measure(value, family, size)
        assert width <= limit
        checks['type_widths'][label] = {'width_px':width,'available_px':limit,'pass':True}
    for label, a,b in [('ink on paper',INK,PAPER),('muted on paper',MUTED,PAPER),('paper on ink',PAPER,INK),('mint on ink',MINT,INK),('terminal hint on ink','#AACAB9',INK)]:
        ratio = contrast(a,b)
        assert ratio >= 4.5
        checks['contrast_ratios'][label] = round(ratio,2)
    write_new(proof_dir / 'theme-and-size-review.png', png_bytes(make_sheet(images)))
    write_new(proof_dir / 'checks.json', json.dumps(checks, indent=2) + '\n')
    print(json.dumps(checks, indent=2))
    print('Proofs created. Inspect them before writing final destination PNGs.')


if __name__ == '__main__':
    main()
