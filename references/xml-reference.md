# Draw.io XML Reference

Use this reference when generating or debugging native `.drawio` XML.

## Practical Layout

Use a simple grid before writing XML:

- Column x: `col * 180 + 40`
- Row y: `row * 120 + 40`
- Standard rectangle: `140 x 60`
- Decision diamond: `140 x 80`
- Circle: `60 x 60`
- Document: `120 x 80`
- Database cylinder: `100 x 70`

Do not spend tokens narrating coordinate math. Pick positions, write cells, and rely on draw.io routing for connectors.

## Common Styles

- Rounded process: `rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;`
- Decision: `rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;`
- Database: `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;`
- Document: `shape=mxgraph.flowchart.document;whiteSpace=wrap;html=1;`
- Orthogonal edge: `edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;`
- ER edge: `edgeStyle=entityRelationEdgeStyle;html=1;endArrow=none;`
- Curved informal edge: `curved=1;html=1;endArrow=classic;`
- Swimlane: `swimlane;horizontal=0;startSize=110;html=1;`
- Container: `rounded=1;whiteSpace=wrap;html=1;container=1;pointerEvents=0;`

## Edges

Always use expanded edge cells:

```xml
<mxCell id="edge-1" value="Label" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;" edge="1" parent="1" source="source-id" target="target-id">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

Prefer one edge style per diagram:

- Flowcharts, architecture, network diagrams: `orthogonalEdgeStyle`
- ER diagrams: `entityRelationEdgeStyle`
- UML class and sequence diagrams: straight edges
- Mind maps and informal diagrams: `curved=1`

Avoid manual waypoints, `exitX`, `exitY`, `entryX`, and `entryY` unless the user asked for exact routing.

## Containers

Use parent-child containment rather than placing shapes visually on top of large boxes.

- Child cells set `parent` to the container id.
- Child coordinates are relative to the container.
- Edges between cells in different containers use `parent="1"` to avoid clipping.
- Use `pointerEvents=0` when a visual container should not capture child connections.

For flat swimlanes:

- Make each lane a top-level swimlane.
- Put lane children inside the lane.
- Keep cross-lane edges at `parent="1"`.
- Use consistent lane height and title width.

For nested architecture diagrams:

- Represent hierarchy as nested swimlanes or containers.
- Use relative coordinates inside each parent.
- Keep cross-container edges at the root layer.

## Labels

- Use `html=1` in styles by default.
- Use `&#xa;` or escaped `<br>` for line breaks.
- Use `fontStyle=1` for all-bold labels, `fontStyle=2` for italic, and `fontStyle=4` for underline.
- XML-escape any HTML-like label content inside attributes.

## Layers, Tags, And Metadata

Use layers for major visibility groups. Layers are `mxCell` elements with `parent="0"` and no `vertex` or `edge` attribute. Assign shapes to a layer by setting their `parent` to the layer id.

Use tags and metadata only when the user needs filtering, status, owners, versions, or data-driven labels. Tags and metadata require wrapping a cell in an `object` element.

## Shape Selection

Use basic shapes for standard flowcharts, UML, ERD, org charts, mind maps, timelines, and wireframes.

Use domain-specific draw.io shape libraries for cloud architecture, network topology, Kubernetes, electrical diagrams, P&ID diagrams, or branded infrastructure icons when exact visual conventions matter.

## Well-Formedness Checklist

- No XML comments.
- One `mxGraphModel` root.
- Root contains `mxCell id="0"` and `mxCell id="1" parent="0"`.
- Unique ids.
- Valid parent references.
- Escaped attribute values.
- Every edge has a child `mxGeometry relative="1" as="geometry"`.
- Vertex cells have `mxGeometry` with `x`, `y`, `width`, `height`, and `as="geometry"`.
