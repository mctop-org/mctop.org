#!/usr/bin/env python3
"""Assemble mctop.org in the classic Linux-project layout (Arch lineage):
header + tabbed nav, boxed sections with dark header bars, a live releases feed,
and a multi-column footer. Static output into public/.

Releases are read from releases.txt (lines "tag|date|name") if present, written
at build time from the live GitHub releases, so the feed stays current.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "public")
REPO = "https://github.com/mctop-org/mctop"

NAV = [("home", "/"), ("explore", "/explore/"), ("script", "/script/"),
       ("test", "/test/"), ("install", "/download/")]

def nav(active):
    out = []
    for label, href in NAV:
        on = " class=on" if href == active else ""
        out.append(f'<a{on} href="{href}">{label}</a>')
    return ("".join(out) + '<span class="grow"></span>'
            f'<a class="ext" href="{REPO}">github</a>')

def head(title, desc, canonical):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
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
<header class="top">
  <div class="wrap topbar">
    <a class="brand" href="/">mctop</a>
    <button class="tbtn" id="theme" title="light / dark" aria-label="toggle theme">&#9680;</button>
  </div>
  <nav class="mainnav"><div class="wrap">{nav(canonical)}</div></nav>
</header>
<main><div class="wrap">"""

def box(title, body, right="", anchor=""):
    r = f'<a href="{right[1]}">{right[0]}</a>' if right else ""
    aid = f' id="{anchor}"' if anchor else ""
    return f'<section class="box"{aid}><div class="h"><span>{title}</span>{r}</div><div class="b">{body}</div></section>'

def block(lines):
    return f'<div class="block"><pre>{lines}</pre></div>'

COPYLINE = ('<div class="copyline"><span class="d">$</span>'
            '<code>curl -fsSL https://mctop.org/install | sh</code>'
            '<button class="copy" data-cmd="curl -fsSL https://mctop.org/install | sh">copy</button></div>')

FOOT = f"""</div></main>
<footer class="foot"><div class="wrap">
  <div class="foot-cols">
    <div class="foot-col"><h4>install</h4>
      <a href="/install">shell installer</a>
      <a href="/download/#homebrew">homebrew</a>
      <a href="/download/#go">go install</a></div>
    <div class="foot-col"><h4>source</h4>
      <a href="{REPO}">github</a>
      <a href="{REPO}/blob/main/README.md">readme</a>
      <a href="{REPO}/issues">issues</a></div>
    <div class="foot-col"><h4>protocol</h4>
      <a href="https://modelcontextprotocol.io">modelcontextprotocol.io</a>
      <a href="https://github.com/modelcontextprotocol">MCP on github</a></div>
  </div>
  <div class="foot-bot"><span>mctop.org</span>
    <a href="{REPO}/blob/main/LICENSE">MIT license</a></div>
</div></footer>
<script src="/app.js"></script>
</body></html>"""

def page(path, title, desc, body):
    full = head(title, desc, path) + body + FOOT
    outdir = PUB if path == "/" else os.path.join(PUB, path.strip("/"))
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w").write(full)

def releases_box():
    f = os.path.join(HERE, "releases.txt")
    if not os.path.exists(f):
        body = f'<p class="dim">prebuilt binaries for every release. <a href="{REPO}/releases">see all releases</a>.</p>'
        return box("releases", body, right=("all releases &rarr;", f"{REPO}/releases"))
    rows = []
    for line in open(f).read().splitlines():
        if not line.strip():
            continue
        parts = line.split("|")
        tag, date = parts[0], parts[1] if len(parts) > 1 else ""
        rows.append(f'<li><span class="date">{date}</span>'
                    f'<a class="tag" href="{REPO}/releases/tag/{tag}">{tag}</a></li>')
    body = f'<ul class="rel">{"".join(rows)}</ul>'
    return box("releases", body, right=("all releases &rarr;", f"{REPO}/releases"))

# ---------------- the client panel (generated so every column lines up) ----------------
def client_panel():
    W, LW = 48, 21            # inner width, left-pane width; divider + right pane fill the rest
    RW = W - LW - 1
    sp = lambda cls, s: f'<span class="{cls}">{s}</span>' if cls else s
    vis = lambda cells: sum(len(t) for t, _ in cells)
    htm = lambda cells: "".join(sp(c, t) for t, c in cells)
    pad = lambda cells, width: htm(cells) + " " * (width - vis(cells))
    def split(left, right, trail=2):                      # left-aligned, right-aligned, computed gap
        gap = W - vis(left) - vis(right) - trail
        return htm(left) + " " * gap + htm(right) + " " * trail
    B = lambda ch: sp("s", ch)
    rows = [
        ([("  TOOLS (2)", "k")],          [("  get_current_time", "k")]),
        ([("  ▌ get_current_time", "k")], [("  get the current time", None)]),
        ([("    convert_time", "s")],      [("  in a given timezone", None)]),
        ([("  RESOURCES (0)", "s")],       [("", None)]),
        ([("  PROMPTS (0)", "s")],         [("  ARGUMENTS", "s")]),
        ([("", None)],                     [("  ", None), ("timezone", "s"), ("*", "k"), ("  string", None)]),
        ([("", None)],                     [("  ", None), ("❯", "k"), (" enter to call", "s")]),
    ]
    header = split([("  ❯ mctop uvx mcp-server-time", "s")], [("●", "ok"), (" connected", "s")])
    footer = pad([("  enter open · / search · tab section · ? keys", "s")], W)
    out = [B("┌" + "─" * W + "┐"),
           B("│") + header + B("│"),
           B("├" + "─" * LW + "┬" + "─" * RW + "┤")]
    for lc, rc in rows:
        out.append(B("│") + pad(lc, LW) + B("│") + pad(rc, RW) + B("│"))
    out += [B("├" + "─" * LW + "┴" + "─" * RW + "┤"),
            B("│") + footer + B("│"),
            B("└" + "─" * W + "┘")]
    return "\n".join(out)

# ---------------- home ----------------
DEMO = block(client_panel())

home = f"""
<h1>a terminal client for <span class="mark">MCP</span> servers</h1>
<p class="tagline">curl and k9s, but for the model context protocol: explore a server, call its tools, and gate its contract in CI.</p>
{COPYLINE}
{box("the client", DEMO + '<p class="dim">run <code>mctop &lt;target&gt;</code> with no subcommand to open the full-screen client: browse a server&#39;s tools, resources, and prompts, fill in a tool&#39;s arguments, and read the result.</p>')}
{box("commands", '''<ul class="cmds">
  <li><a class="m" href="/explore/">explore</a><code>mctop &lt;target&gt;</code><span class="d">open the interactive client</span></li>
  <li><a class="m" href="/script/">script</a><code>mctop ls &lt;target&gt;</code><span class="d">list tools, resources, prompts</span></li>
  <li><span class="m e"></span><code>mctop call &lt;target&gt; &lt;tool&gt;</code><span class="d">call one tool, print the result</span></li>
  <li><a class="m" href="/test/">test</a><code>mctop test &lt;spec.yaml&gt;</code><span class="d">assert a contract in CI, fail on drift</span></li>
  <li><span class="m u">login</span><code>mctop login &lt;url&gt;</code><span class="d">log in to an OAuth server</span></li>
  <li><span class="m u">upgrade</span><code>mctop upgrade</code><span class="d">update in place</span></li>
</ul>''' + '<p class="dim">a target is a command to spawn (<code>"uvx mcp-server-time"</code>) or an <code>http(s)://</code> url. explore, script, and test each have a page; login and upgrade are utilities.</p>')}
{releases_box()}
"""

def feature(path, title, lede, blk, prose, keys=None):
    inner = block(blk) + prose
    parts = [f'<h1>{title}</h1><p class="tagline">{lede}</p>', box("example", inner)]
    if keys:
        rows = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in keys)
        parts.append(box("keys", f'<dl class="keys">{rows}</dl>'))
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
<h1>install</h1>
<p class="tagline">one static binary, no runtime.</p>
{box("shell", block('<span class="d">$</span> curl -fsSL https://mctop.org/install | sh') + '<p class="dim">the installer is plain text at <a href="/install">mctop.org/install</a>. it downloads the release archive, checks its sha256 against the published checksums, and refuses to install on a mismatch.</p>')}
{box("homebrew", block('<span class="d">$</span> brew install mctop-org/tap/mctop'), anchor="homebrew")}
{box("go", block('<span class="d">$</span> go install github.com/mctop-org/mctop@latest'), anchor="go")}
{box("platforms", f'<p>prebuilt binaries for linux and macos on amd64 and arm64. windows builds are on the <a href="{REPO}/releases/latest">releases page</a>.</p>')}
{box("upgrade", '<p><code>mctop upgrade</code> fetches the latest release in place. the shell installer also re-runs cleanly to update.</p>')}
"""

page("/", "mctop - a terminal client for MCP servers",
     "Explore, call, and CI-test any MCP server from your shell. curl and k9s, but for the Model Context Protocol.", home)
page("/explore/", "explore - mctop",
     "Browse an MCP server's tools, resources, and prompts and run them in a schema-driven form.",
     feature("/explore/", "explore", "run mctop against a server to open the full-screen client. move through its tools, resources, and prompts, fill a tool's arguments in a schema-driven form, run it, and read the result laid out as fields and tables, not raw json.",
        client_panel(),
        "<p>the result view formats values by type: dates, yes/no, and grouped numbers. nested objects become sections, and arrays of records become selectable tables. press <code>t</code> for raw json, <code>T</code> for the protocol trace, <code>y</code> to copy.</p>",
        keys=[("&#8593;&#8595; / j k","move and scroll"),("enter / l","open or expand a row"),("/","search names and descriptions"),("tab","next section"),("T","protocol trace"),("?","all keys")]))
page("/script/", "script - mctop",
     "Call MCP tools from the shell with mctop ls and mctop call. Pipeable, structured output.",
     feature("/script/", "script", "skip the ui when you only need the answer. mctop ls lists what a server exposes; mctop call runs one tool and prints the structured result on stdout, ready to pipe into jq or a script.",
        script_blk,
        "<p>arguments are <code>key=value</code> pairs. values that look like json (numbers, booleans, arrays, objects) are typed; everything else is a string. pass a whole object with <code>--json '{...}'</code>. exit status reflects the call, so it composes in pipelines.</p>"))
page("/test/", "test - mctop",
     "Assert an MCP server's contract in CI with a YAML spec. Exits non-zero when a tool is renamed or a call drifts.",
     feature("/test/", "test", "declare the tools that must exist and how their calls must behave. mctop test connects, checks the contract, and exits non-zero when it drifts, so a renamed tool fails the build instead of an agent in production.",
        test_blk,
        "<p>specs are strict yaml: unknown keys are errors, so a typo never silently passes. assert on <code>not_error</code>, substring <code>contains</code>, and the tools a server must expose. add <code>--report json</code> for machine-readable CI output.</p>"))
page("/download/", "install - mctop",
     "Install mctop via shell, Homebrew, or go install. One static binary, self-updates with mctop upgrade.", download)

print("built:", sorted(p for p in os.listdir(PUB) if not p.startswith((".", "_"))))
