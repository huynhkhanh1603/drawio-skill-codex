#!/usr/bin/env python3
"""Validate basic draw.io XML structure before delivery or export."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_drawio_xml.py <file.drawio>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        print(f"Invalid XML: {exc}", file=sys.stderr)
        return 1

    root = tree.getroot()
    graph = root if root.tag == "mxGraphModel" else root.find(".//mxGraphModel")
    if graph is None:
        print("Missing mxGraphModel root.", file=sys.stderr)
        return 1

    graph_root = graph.find("root")
    if graph_root is None:
        print("Missing mxGraphModel/root element.", file=sys.stderr)
        return 1

    cells = graph_root.findall(".//mxCell")
    by_id: dict[str, ET.Element] = {}
    for cell in cells:
        cell_id = cell.get("id")
        if not cell_id:
            print("mxCell missing id.", file=sys.stderr)
            return 1
        if cell_id in by_id:
            print(f"Duplicate mxCell id: {cell_id}", file=sys.stderr)
            return 1
        by_id[cell_id] = cell

    if "0" not in by_id:
        print('Missing root cell id="0".', file=sys.stderr)
        return 1
    if by_id.get("1") is None or by_id["1"].get("parent") != "0":
        print('Missing default layer cell id="1" parent="0".', file=sys.stderr)
        return 1

    ids = set(by_id)
    for cell in cells:
        cell_id = cell.get("id", "<unknown>")
        parent = cell.get("parent")
        if cell_id not in {"0"} and parent and parent not in ids:
            print(f"Cell {cell_id} references missing parent {parent}.", file=sys.stderr)
            return 1

        if cell.get("edge") == "1":
            geom = cell.find("mxGeometry")
            if geom is None or geom.get("as") != "geometry":
                print(f"Edge {cell_id} missing mxGeometry as=\"geometry\".", file=sys.stderr)
                return 1
            for endpoint_attr in ("source", "target"):
                endpoint = cell.get(endpoint_attr)
                if endpoint and endpoint not in ids:
                    print(
                        f"Edge {cell_id} references missing {endpoint_attr} {endpoint}.",
                        file=sys.stderr,
                    )
                    return 1

    print("draw.io XML validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
