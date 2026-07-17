#!/usr/bin/env python3
"""Assemble mctop.org: a lean, single-column documentation site.

Sections are open (an eyebrow label over a hairline, then content), not boxed.
The client preview is a real aligned CSS component, generated once and reused so
it looks identical on every page. Dark is the default theme. Static output into
public/.

Releases are read from releases.txt (lines "tag|date|name") if present, written
at build time from the live GitHub releases, so the feed stays current.
"""
import os, hashlib, base64

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "public")
REPO = "https://github.com/mctop-org/mctop"
SITE = "https://mctop.org"

# The one inline script (sets the stored theme before paint to avoid a flash).
# Kept as a constant so its Content-Security-Policy hash stays in sync with it.
THEME_INLINE = ("try{if(localStorage.getItem('mctop-theme')==='light')"
                "document.documentElement.setAttribute('data-theme','light')}catch(e){}")
CSP_HASH = "sha256-" + base64.b64encode(hashlib.sha256(THEME_INLINE.encode()).digest()).decode()

PAGES = []  # canonical paths, collected as pages are written, for the sitemap

NAV = [("Explore", "/explore/"), ("Script", "/script/"),
       ("Test", "/test/"), ("Install", "/download/")]

def nav(active):
    out = []
    for label, href in NAV:
        on = " class=on" if href == active else ""
        out.append(f'<a{on} href="{href}">{label}</a>')
    out.append(f'<a class="ext" href="{REPO}">GitHub</a>')
    return "".join(out)

def head(title, desc, canonical):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script>{THEME_INLINE}</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://mctop.org/brand/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://mctop.org{canonical}">
<link rel="icon" type="image/svg+xml" href="/brand/icon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/brand/icon-32.png">
<link rel="apple-touch-icon" href="/brand/icon-180.png">
<link rel="preload" href="/fonts/AnthrosevkaMono-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/AnthrosevkaMono-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header class="top"><div class="wrap top-in">
  <a class="brand" href="/">mctop</a>
  <nav class="nav">{nav(canonical)}</nav>
  <button class="tbtn" id="theme" title="Light / dark" aria-label="Toggle theme" aria-pressed="false">&#9680;</button>
</div></header>
<main><div class="wrap">"""

def hero(inner):
    return f'<div class="hero">{inner}</div>'

def section(label, body, right=""):
    r = f'<a href="{right[1]}">{right[0]}</a>' if right else ""
    return (f'<section class="sec"><div class="sec-h">'
            f'<span class="eyebrow">{label}</span>{r}</div>{body}</section>')

def block(lines):
    return f'<div class="block"><pre>{lines}</pre></div>'

COPYLINE = ('<div class="copyline"><span class="d">$</span>'
            '<code>curl -fsSL https://mctop.org/install | sh</code>'
            '<button class="copy" data-cmd="curl -fsSL https://mctop.org/install | sh">Copy</button></div>')

# ---------------- the client preview: one aligned CSS component, reused everywhere ----------------
def client():
    return '''<div class="tui">
  <div class="tui-bar">
    <span class="cmd"><span class="p">&#10095;</span> mctop uvx mcp-server-time</span>
    <span class="stat"><span class="dot"></span>connected</span>
  </div>
  <div class="tui-body">
    <div class="pane list">
      <p class="grp">tools <span class="ct">2</span></p>
      <p class="row on">get_current_time</p>
      <p class="row">convert_time</p>
      <p class="grp">resources <span class="ct">0</span></p>
      <p class="grp">prompts <span class="ct">0</span></p>
    </div>
    <div class="pane detail">
      <p class="nm">get_current_time</p>
      <p class="ds">Get the current time in a given timezone</p>
      <p class="grp">arguments</p>
      <p class="arg"><span class="an">timezone</span><span class="rq">*</span> <span class="ty">string</span></p>
      <p class="call"><span class="p">&#10095;</span> enter to call</p>
    </div>
  </div>
  <div class="tui-foot">enter open &middot; / search &middot; tab section &middot; ? keys</div>
</div>'''

# ---------------- home ----------------
home = f"""
{hero('''<h1>A terminal client for <span class="mark">MCP</span> servers</h1>
<p class="tagline">curl and k9s, but for the Model Context Protocol: explore a server, call its tools, and gate its contract in CI.</p>
''' + COPYLINE)}
{section("the client", client() + '<p class="dim">Run <code>mctop &lt;target&gt;</code> with no subcommand to open the full-screen client: browse a server&#39;s tools, resources, and prompts, fill in a tool&#39;s arguments, and read the result.</p>')}
{section("commands", '''<ul class="cmds">
  <li><a class="m" href="/explore/">explore</a><code>mctop &lt;target&gt;</code><span class="d">Open the interactive client</span></li>
  <li><a class="m" href="/script/">script</a><code>mctop ls &lt;target&gt;</code><span class="d">List tools, resources, and prompts</span></li>
  <li><span class="m e"></span><code>mctop call &lt;target&gt; &lt;tool&gt;</code><span class="d">Call one tool and print the result</span></li>
  <li><a class="m" href="/test/">test</a><code>mctop test &lt;spec.yaml&gt;</code><span class="d">Assert a contract in CI, fail on drift</span></li>
  <li><span class="m u">login</span><code>mctop login &lt;url&gt;</code><span class="d">Log in to an OAuth server</span></li>
  <li><span class="m u">upgrade</span><code>mctop upgrade</code><span class="d">Update in place</span></li>
</ul>''' + '<p class="dim">A target is a command to spawn (<code>"uvx mcp-server-time"</code>) or an <code>http(s)://</code> URL. Explore, script, and test each have a page; login and upgrade are utilities.</p>')}
{{RELEASES}}
"""

def releases_body():
    f = os.path.join(HERE, "releases.txt")
    if not os.path.exists(f):
        return section("releases",
                       f'<p class="dim">Prebuilt binaries for every release. <a href="{REPO}/releases">See all releases</a>.</p>',
                       right=("All releases &rarr;", f"{REPO}/releases"))
    rows = []
    for line in open(f).read().splitlines():
        if not line.strip():
            continue
        parts = line.split("|")
        tag, date = parts[0], parts[1] if len(parts) > 1 else ""
        rows.append(f'<li><span class="date">{date}</span>'
                    f'<a class="tag" href="{REPO}/releases/tag/{tag}">{tag}</a></li>')
    return section("releases", f'<ul class="rel">{"".join(rows)}</ul>',
                   right=("All releases &rarr;", f"{REPO}/releases"))

def foot():
    return f"""</div></main>
<footer class="foot"><div class="wrap">
  <div class="foot-cols">
    <div class="foot-col"><h4>install</h4>
      <a href="/install">Shell installer</a>
      <a href="/download/#homebrew">Homebrew</a>
      <a href="/download/#go">Go install</a></div>
    <div class="foot-col"><h4>source</h4>
      <a href="{REPO}">GitHub</a>
      <a href="{REPO}/blob/main/README.md">Readme</a>
      <a href="{REPO}/issues">Issues</a></div>
    <div class="foot-col"><h4>protocol</h4>
      <a href="https://modelcontextprotocol.io">modelcontextprotocol.io</a>
      <a href="https://github.com/modelcontextprotocol">MCP on GitHub</a></div>
  </div>
  <div class="foot-bot"><span>mctop.org</span>
    <a href="{REPO}/blob/main/LICENSE">MIT License</a></div>
</div></footer>
<script src="/app.js"></script>
</body></html>"""

def page(path, title, desc, body):
    full = head(title, desc, path) + body + foot()
    outdir = PUB if path == "/" else os.path.join(PUB, path.strip("/"))
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w").write(full)
    PAGES.append(path)

def feature(title, lede, example_html, prose, keys=None):
    parts = [hero(f'<h1>{title}</h1><p class="tagline">{lede}</p>'),
             section("example", example_html + prose)]
    if keys:
        rows = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in keys)
        parts.append(section("keys", f'<dl class="keys">{rows}</dl>'))
    return "".join(parts)

script_blk = '''<span class="d">$</span> mctop call <span class="s">"uvx mcp-server-time"</span> get_current_time timezone=UTC
{
  <span class="k">"timezone"</span>: "UTC",
  <span class="k">"datetime"</span>: "2026-06-27T04:41:00+00:00",
  <span class="k">"day_of_week"</span>: "Saturday"
}'''

test_blk = '''<span class="s"># spec.yaml</span>
<span class="k">expect</span>:
  <span class="k">tools</span>: [search, fetch]
<span class="k">calls</span>:
  - <span class="k">tool</span>: search
    <span class="k">assert</span>: { not_error: true, contains: "result" }

<span class="d">$</span> mctop test spec.yaml
<span class="ok">&#10003; tools present   &#10003; search not_error   &#10003; search contains</span>
3 passed, 0 failed   <span class="ok">exit 0</span>'''

download = f"""
{hero('<h1>Install</h1><p class="tagline">One static binary, no runtime.</p>')}
{section("shell", block('<span class="d">$</span> curl -fsSL https://mctop.org/install | sh') + '<p class="dim">The installer is plain text at <a href="/install">mctop.org/install</a>. It downloads the release archive, checks its SHA-256 against the published checksums, and refuses to install on a mismatch.</p>')}
{section("homebrew", block('<span class="d">$</span> brew install mctop-org/tap/mctop'))}
{section("go", block('<span class="d">$</span> go install github.com/mctop-org/mctop@latest'))}
{section("platforms", f'<p>Prebuilt binaries for Linux and macOS on amd64 and arm64. Windows builds are on the <a href="{REPO}/releases/latest">releases page</a>.</p>')}
{section("upgrade", '<p><code>mctop upgrade</code> fetches the latest release in place. The shell installer also re-runs cleanly to update.</p>')}
"""

page("/", "mctop - a terminal client for MCP servers",
     "Explore, call, and CI-test any MCP server from your shell. curl and k9s, but for the Model Context Protocol.",
     home.replace("{RELEASES}", releases_body()))
page("/explore/", "explore - mctop",
     "Browse an MCP server's tools, resources, and prompts and run them in a schema-driven form.",
     feature("Explore", "Run mctop against a server to open the full-screen client. Move through its tools, resources, and prompts, fill a tool's arguments in a schema-driven form, run it, and read the result laid out as fields and tables, not raw JSON.",
        client(),
        "<p>The result view formats values by type: dates, yes/no, and grouped numbers. Nested objects become sections, and arrays of records become selectable tables. Press <code>t</code> for raw JSON, <code>T</code> for the protocol trace, <code>y</code> to copy.</p>",
        keys=[("&#8593;&#8595; / j k","Move and scroll"),("enter / l","Open or expand a row"),("/","Search names and descriptions"),("tab","Next section"),("T","Protocol trace"),("?","All keys")]))
page("/script/", "script - mctop",
     "Call MCP tools from the shell with mctop ls and mctop call. Pipeable, structured output.",
     feature("Script", "Skip the UI when you only need the answer. mctop ls lists what a server exposes; mctop call runs one tool and prints the structured result on stdout, ready to pipe into jq or a script.",
        block(script_blk),
        "<p>Arguments are <code>key=value</code> pairs. Values that look like JSON (numbers, booleans, arrays, objects) are typed; everything else is a string. Pass a whole object with <code>--json '{...}'</code>. Exit status reflects the call, so it composes in pipelines.</p>"))
page("/test/", "test - mctop",
     "Assert an MCP server's contract in CI with a YAML spec. Exits non-zero when a tool is renamed or a call drifts.",
     feature("Test", "Declare the tools that must exist and how their calls must behave. mctop test connects, checks the contract, and exits non-zero when it drifts, so a renamed tool fails the build instead of an agent in production.",
        block(test_blk),
        "<p>Specs are strict YAML: unknown keys are errors, so a typo never silently passes. Assert on <code>not_error</code>, substring <code>contains</code>, and the tools a server must expose. Add <code>--report json</code> for machine-readable CI output.</p>"))
page("/download/", "install - mctop",
     "Install mctop via shell, Homebrew, or go install. One static binary, self-updates with mctop upgrade.", download)

# ---------------- 404 (served with a 404 status via wrangler not_found_handling) ----------------
notfound = (hero('<h1>Page not found</h1>'
                 '<p class="tagline">That page moved or never existed. Pick up from one of these.</p>')
            + section("go", '''<ul class="cmds">
  <li><a class="m" href="/">home</a><code>mctop</code><span class="d">Overview and install</span></li>
  <li><a class="m" href="/explore/">explore</a><code>mctop &lt;target&gt;</code><span class="d">The interactive client</span></li>
  <li><a class="m" href="/download/">install</a><code>curl &#8230; | sh</code><span class="d">Get the binary</span></li>
  <li><a class="m" href="''' + REPO + '''">github</a><code>mctop-org/mctop</code><span class="d">Source and issues</span></li>
</ul>'''))
open(os.path.join(PUB, "404.html"), "w").write(
    head("Page not found - mctop", "The page you are looking for does not exist.", "/404") + notfound + foot())

# ---------------- machine-readable meta: robots + sitemap + response headers ----------------
def write_meta():
    open(os.path.join(PUB, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

    urls = "".join(f"<url><loc>{SITE}{p}</loc></url>" for p in sorted(set(PAGES)))
    open(os.path.join(PUB, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>\n")

    csp = ("default-src 'self'; "
           f"script-src 'self' '{CSP_HASH}'; "
           "style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; "
           "base-uri 'none'; object-src 'none'; frame-ancestors 'none'; form-action 'none'; "
           "upgrade-insecure-requests")
    open(os.path.join(PUB, "_headers"), "w").write(f"""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: {csp}

/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/brand/*
  Cache-Control: public, max-age=604800

/style.css
  Cache-Control: public, max-age=86400

/app.js
  Cache-Control: public, max-age=86400

/install
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=300
""")

write_meta()

print("built:", sorted(p for p in os.listdir(PUB) if not p.startswith((".", "_"))))
print("meta: robots.txt sitemap.xml _headers 404.html   csp-hash:", CSP_HASH)
