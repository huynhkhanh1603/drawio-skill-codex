---
name: drawio
description: Create, edit, validate, and export native draw.io diagrams. Use when the user asks for a diagram, flowchart, architecture diagram, ERD, UML/class/sequence diagram, network diagram, mockup, wireframe, UI sketch, .drawio file, or draw.io-compatible PNG/SVG/PDF export.
---

# Draw.io

Generate native draw.io `.drawio` files as `mxGraphModel` XML. Export to PNG, SVG, or PDF when requested and when the draw.io desktop CLI is available.

## Workflow

1. Determine the diagram type, target filename, and requested output format.
2. Read `references/xml-reference.md` when generating non-trivial XML, using containers, creating edges, or debugging draw.io rendering.
3. Generate a `.drawio` file directly in `mxGraphModel` XML. Do not use Mermaid, CSV, or comments in XML.
4. Run `scripts/validate_drawio_xml.py <file.drawio>` before export or delivery.
5. If the user requested `png`, `svg`, or `pdf`, locate the draw.io CLI and export with embedded diagram XML.
6. Deliver the exported file when export succeeds. Otherwise deliver the `.drawio` file and explain that draw.io Desktop is needed for local export.

## Output Format

Use the user's requested format:

- No format mentioned: create `<name>.drawio`.
- PNG: create `<name>.drawio.png` with embedded diagram XML.
- SVG: create `<name>.drawio.svg` with embedded diagram XML.
- PDF: create `<name>.drawio.pdf` with embedded diagram XML.
- JPG: only use when explicitly requested; JPG cannot embed editable draw.io XML.

After a successful PNG/SVG/PDF export, the exported file is the primary artifact because it remains editable in draw.io when `--embed-diagram` is used.

## File Naming

Use lowercase, hyphenated names based on the diagram content, such as `login-flow.drawio` or `payments-architecture.drawio.svg`.

## XML Requirements

Every `.drawio` file must include:

```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
  </root>
</mxGraphModel>
```

Follow these rules:

- Set every diagram cell's `parent` to `1`, a layer id, or a container id.
- Use unique `id` values for all cells.
- Escape XML attribute values: `&amp;`, `&lt;`, `&gt;`, `&quot;`.
- Add `html=1` to styles by default, especially when labels contain formatting or line breaks.
- Never include XML comments.
- Give every edge cell an expanded `<mxGeometry relative="1" as="geometry"/>` child.
- Prefer domain-appropriate draw.io shapes when the diagram calls for them.

## Export

Locate the CLI in this order:

1. `drawio` on `PATH`
2. macOS: `/Applications/draw.io.app/Contents/MacOS/draw.io`
3. Linux: `drawio`
4. WSL2: `/mnt/c/Program Files/draw.io/draw.io.exe` or `/mnt/c/Users/$WIN_USER/AppData/Local/Programs/draw.io/draw.io.exe`
5. Windows: `C:\Program Files\draw.io\draw.io.exe`

Export command:

```bash
drawio -x -f <png|svg|pdf> -e -b 10 -o <output> <input.drawio>
```

Useful options:

- `-x`: export mode
- `-f`: output format
- `-e`: embed editable diagram XML
- `-b 10`: add a 10 px border
- `-t`: transparent PNG background
- `-s`: export scale
- `--width` or `--height`: fit to a target dimension
- `-a`: export all pages for PDF
- `-p`: export a specific 1-based page index

## Open Or Report

If opening files is allowed in the environment, open the final artifact:

- macOS: `open <file>`
- Linux: `xdg-open <file>`
- WSL2: `cmd.exe /c start "" "$(wslpath -w <file>)"`
- Windows: `start <file>`

If opening is unavailable or blocked, report the absolute path.

## Troubleshooting

- CLI not found: keep the `.drawio` file and tell the user export needs draw.io Desktop.
- Blank diagram: check root cells `id="0"` and `id="1"`, parent ids, and geometry.
- Missing edges: ensure each edge has a child `mxGeometry` element.
- Corrupt file: run the validation script and fix XML well-formedness issues.
- Text renders as raw HTML: add `html=1` to the cell style and XML-escape tag characters inside attributes.
