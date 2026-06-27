#!/usr/bin/env python3
"""Assemble the mctop.org pages as plain-text documents from a shared shell.

Pages: home, /explore/, /script/, /test/, /download/. Static assets (fonts,
brand, /install script, _headers, style.css, app.js) are left untouched.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "public")
DASH = "–"   # en dash, allowed; em dashes are not used anywhere

NAV = [("explore", "/explore/"), ("script", "/script/"),
       ("test", "/test/"), ("install", "/download/")]

def head(title, desc, canonical):
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="/brand/icon-512.png">
<meta name="twitter:card" content="summary">
<link rel="canonical" href="https://mctop.org{canonical}">
<link rel="icon" type="image/svg+xml" href="/brand/icon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/brand/icon-32.png">
<link rel="apple-touch-icon" href="/brand/icon-180.png">
<link rel="preload" href="/fonts/AnthrosevkaMono-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/AnthrosevkaMono-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header class="masthead"><div class="wrap">
  <a class="brand" href="/"><span class="br l">[</span>mctop<span class="br r">]</span></a>
  <nav class="menu">{menu(canonical)}<button class="tbtn" id="theme" title="light / dark" aria-label="toggle theme">&#9680;</button></nav>
</div><div class="wrap"><hr class="rule"></div></header>
<main><div class="wrap">"""

def menu(active):
    out = []
    for label, href in NAV:
        on = " class=on" if href == active else ""
        out.append(f'<a{on} href="{href}">{label}</a>')
    out.append('<a href="https://github.com/mctop-org/mctop">github</a>')
    return "".join(out)

FOOT = f"""</div></main>
<footer class="man"><div class="wrap">
  <div class="row head"><span>MCTOP(1)</span><span>General Commands Manual</span><span>MCTOP(1)</span></div>
  <div class="row"><span>NAME &nbsp; mctop {DASH} a terminal client for the model context protocol</span></div>
  <div class="row"><span>SEE ALSO &nbsp; <a href="/explore/">explore</a> <a href="/script/">script</a> <a href="/test/">test</a> <a href="/download/">install</a> <a href="https://github.com/mctop-org/mctop">github</a></span></div>
  <div class="row" style="margin-top:14px"><span>mctop.org</span><span>MIT</span><span>built for the shell</span></div>
</div></footer>
<script src="/app.js"></script>
</body></html>"""

def write(path, title, desc, body):
    full = head(title, desc, path) + body + FOOT
    outdir = PUB if path == "/" else os.path.join(PUB, path.strip("/"))
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w").write(full)

COPYLINE = ('<div class="copyline"><span class="d">$</span>'
            '<code>curl -fsSL <span class="url">https://mctop.org/install</span> | sh</code>'
            '<button class="copy" data-cmd="curl -fsSL https://mctop.org/install | sh">copy</button></div>')

def block(lines):
    return f'<div class="block"><pre>{lines}</pre></div>'

# ---------------- home ----------------
home = f"""
<h1>a terminal client for <span class="mark">MCP</span> servers</h1>
<p class="tagline">curl and k9s, but for the model context protocol. connect to any server, browse its tools, resources, and prompts, call them, and read the result, without leaving the shell. then gate its contract in CI.</p>
{COPYLINE}

<section class="sec"><h2>synopsis</h2>
{block('''<span class="s">mctop &lt;target&gt;</span>                 open the interactive client
<span class="s">mctop ls &lt;target&gt;</span>              list tools, resources, prompts
<span class="s">mctop call &lt;target&gt; &lt;tool&gt;</span>     call one tool, print the result
<span class="s">mctop test &lt;spec.yaml&gt;</span>         run a contract, exit 0 or 1
<span class="s">mctop login &lt;url&gt;</span>              log in to an OAuth server
<span class="s">mctop upgrade</span>                  update to the latest release''')}
<p class="dim">a target is a command to spawn (<code>"uvx mcp-server-time"</code>) or an <code>http(s)://</code> url.</p>
</section>

<section class="sec"><h2>commands</h2>
<ul class="toc">
  <li><a class="name" href="/explore/">explore</a><span class="desc">browse a server and run a tool in a schema-driven form</span></li>
  <li><a class="name" href="/script/">script</a><span class="desc">one-shot calls from the shell, structured output, pipeable</span></li>
  <li><a class="name" href="/test/">test</a><span class="desc">assert a server's contract in CI, fail the build on drift</span></li>
  <li><a class="name" href="/download/">install</a><span class="desc">shell, homebrew, or go install. one static binary</span></li>
</ul>
</section>
"""

# ---------------- feature pages ----------------
def feature(path, title, lede, blk, prose, keys=None):
    keyhtml = ""
    if keys:
        rows = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in keys)
        keyhtml = f'<section class="sec"><h2>keys</h2><dl class="keys">{rows}</dl></section>'
    return f"""
<h1>{title}</h1>
<p class="tagline">{lede}</p>
<section class="sec"><h2>example</h2>{block(blk)}{prose}</section>
{keyhtml}
<section class="sec"><h2>install</h2>{COPYLINE}<p class="dim">other ways on the <a href="/download/">install page</a>.</p></section>
"""

explore_blk = '''<span class="s">  mctop  &middot;  uvx mcp-server-time</span>        <span class="ok">&#9679;</span> connected
 <span class="k">TOOLS (2)</span>              <span class="s">|</span>  <span class="k">get_current_time</span>
 <span class="k">&#9612; get_current_time</span>     <span class="s">|</span>  get current time in a
   <span class="s">convert_time</span>        <span class="s">|</span>  specific timezone
 <span class="s">RESOURCES (0)</span>         <span class="s">|</span>  <span class="s">timezone</span><span class="k">*</span> string
 <span class="s">PROMPTS (0)</span>           <span class="s">|</span>  <span class="k">enter</span> to call'''

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

# ---------------- download ----------------
download = f"""
<h1>install</h1>
<p class="tagline">one static binary, no runtime. it self-updates with <code>mctop upgrade</code>, however you installed it.</p>

<section class="sec"><h2>shell</h2>{block('<span class="d">$</span> curl -fsSL https://mctop.org/install | sh')}
<p class="dim">the installer is plain text at <a href="/install">mctop.org/install</a>. read it first if you like; it downloads the release archive, checks its sha256 against the published checksums, and refuses to install on a mismatch.</p></section>

<section class="sec"><h2>homebrew</h2>{block('<span class="d">$</span> brew install mctop-org/tap/mctop')}</section>

<section class="sec"><h2>go</h2>{block('<span class="d">$</span> go install github.com/mctop-org/mctop@latest')}</section>

<section class="sec"><h2>platforms</h2>
<p>prebuilt binaries for linux and macos on amd64 and arm64. windows builds are on the <a href="https://github.com/mctop-org/mctop/releases">releases page</a>.</p></section>

<section class="sec"><h2>upgrade</h2>
<p><code>mctop upgrade</code> fetches the latest release in place. the shell installer also re-runs cleanly to update.</p></section>
"""

write("/", "mctop — a terminal client for MCP servers".replace("—","-"),
      "Explore, call, and CI-test any MCP server from your shell. curl and k9s, but for the Model Context Protocol.", home)
write("/explore/", "explore - mctop",
      "Browse an MCP server's tools, resources, and prompts and run them in a schema-driven form.",
      feature("/explore/", "explore", "run mctop against a server to open the full-screen client. move through tools, resources, and prompts, fill a tool's arguments in a schema-driven form, run it, and read the result laid out as fields and tables, not raw json.",
              explore_blk,
              "<p>the result view reads the data: dates, yes/no, and grouped numbers are formatted, nested objects become sections, and arrays of records become selectable tables. press <code>t</code> for raw json, <code>T</code> for the protocol trace, <code>y</code> to copy.</p>",
              keys=[("&#8593;&#8595; / j k","move and scroll"),("enter / l","open, expand a row"),("/","search names and descriptions"),("tab","next section"),("T","protocol trace"),("?","all keys")]))
write("/script/", "script - mctop",
      "Call MCP tools from the shell with mctop ls and mctop call. Pipeable, structured output.",
      feature("/script/", "script", "skip the ui when you just need an answer. mctop ls lists what a server exposes; mctop call runs one tool and prints the structured result on stdout, ready to pipe into jq or a script.",
              script_blk,
              "<p>arguments are <code>key=value</code> pairs. values that look like json (numbers, booleans, arrays, objects) are typed; everything else is a string. pass a whole object with <code>--json '{...}'</code>. exit status reflects the call, so it composes in pipelines.</p>"))
write("/test/", "test - mctop",
      "Assert an MCP server's contract in CI with a YAML spec. Exits non-zero when a tool is renamed or a call drifts.",
      feature("/test/", "test", "declare the tools that must exist and how their calls must behave. mctop test connects, checks the contract, and exits non-zero when it drifts, so a renamed tool fails the build instead of an agent in production.",
              test_blk,
              "<p>specs are strict yaml: unknown keys are errors, so a typo never silently passes. assert on <code>not_error</code>, substring <code>contains</code>, and the tools a server must expose. add <code>--report json</code> for machine-readable ci output.</p>"))
write("/download/", "install - mctop",
      "Install mctop via shell, Homebrew, or go install. One static binary, self-updates with mctop upgrade.", download)

print("built:", sorted(os.listdir(PUB)))
