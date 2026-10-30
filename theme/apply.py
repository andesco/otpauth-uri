#!/usr/bin/env python3
"""Apply the otpauth.dev look to an xml2rfc HTML file, in place.

Usage: apply.py draft-name.html

The page stays one self-contained file: the theme CSS and JavaScript are inlined,
so GitHub Pages only has to publish the HTML.  Pieces:

  offcanvas.css           Bootstrap 5.3.3 offcanvas component rules, extracted unmodified
  bootstrap.bundle.min.js Bootstrap 5.3.3 (MIT)
  glue.css, toc.js        small additions that fit the offcanvas to the draft page
  otpauth-dev.css         otpauth.dev colour tokens and type, mapped onto xml2rfc's v3.css variables
  theme.js                otpauth.dev's light/dark switch, unmodified
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def apply(html):
    if 'id="tocMenu"' in html:
        return html  # already themed

    # 1. The ToC div becomes an offcanvas panel.  Renaming the id stops v3.css's #toc layout rules.
    start = html.find('<div id="toc">')
    if start < 0:
        raise SystemExit("apply.py: no <div id=\"toc\"> found; xml2rfc output changed?")
    nav_end = html.index("</nav>", start)
    div_end = html.index("</div>", nav_end)
    panel_open = (
        '<div id="tocMenu" class="offcanvas offcanvas-start" tabindex="-1" aria-labelledby="name-table-of-contents">\n'
        '<div class="offcanvas-header"><button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button></div>\n'
        '<div class="offcanvas-body">'
    )
    html = html[:start] + panel_open + html[start + len('<div id="toc">'):div_end] + "</div></div>" + html[div_end + len("</div>"):]

    # 2. Button that opens the panel, right after <body>.
    button = (
        '<button class="toc-toggle" type="button" data-bs-toggle="offcanvas" data-bs-target="#tocMenu" '
        'aria-controls="tocMenu">&#9776; Table of Contents</button>\n'
    )
    html, n = re.subn(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + button, html, count=1)
    if n != 1:
        raise SystemExit("apply.py: no <body> found")

    # 3. xml2rfc's own click-to-toggle script is replaced by Bootstrap's.
    html = re.sub(r'<script>const toc = document\.getElementById\("toc"\);.*?</script>', "", html, flags=re.S)

    # 4. Viewport (Safari tinting needs viewport-fit=cover) and head additions.
    html = html.replace('content="initial-scale=1.0"', 'content="width=device-width, initial-scale=1.0, viewport-fit=cover"', 1)
    head = (
        '<meta name="theme-color" content="#e5e7eb" media="(prefers-color-scheme: light)">\n'
        '<meta name="theme-color" content="#111827" media="(prefers-color-scheme: dark)">\n'
        "<script>" + read("theme.js") + "</script>\n"
    )
    html = re.sub(r"(<head>)", lambda m: m.group(1) + "\n" + head, html, count=1)

    # 5. Theme CSS and scripts, last in the body so they follow v3.css in the cascade.
    css = "\n".join(read(n) for n in ("offcanvas.css", "glue.css", "otpauth-dev.css"))
    bundle = read("bootstrap.bundle.min.js")
    if "</script" in bundle:
        raise SystemExit("apply.py: bootstrap bundle contains </script")
    tail = "<style>\n" + css + "</style>\n<script>" + bundle + "</script>\n<script>\n" + read("toc.js") + "</script>\n"
    return html.replace("</body>", tail + "</body>", 1)


def main(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    out = apply(html)
    tmp = path + ".theme"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(out)
    os.replace(tmp, path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
