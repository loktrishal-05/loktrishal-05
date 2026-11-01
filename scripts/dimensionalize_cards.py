"""Add material depth to generated summary charts without changing their data."""
from copy import deepcopy
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

directory = Path(sys.argv[1])
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def element(name, **attributes):
    return ET.Element(f"{{{NS}}}{name}", {key:str(value) for key,value in attributes.items()})


for path in directory.glob("*.svg"):
    if not re.match(r"[0-4]-", path.name):
        continue
    root = ET.parse(path).getroot()
    labels = [node.text for node in root.iter(f"{{{NS}}}text")]
    width, height = map(float, root.get("viewBox").split()[2:])
    key = path.stem
    defs = ET.fromstring(f'''<defs xmlns="{NS}">
      <linearGradient id="metal-{key}" x2=".2" y2="1"><stop stop-color="#223747"/><stop offset=".3" stop-color="#101D2A"/><stop offset="1" stop-color="#080E16"/></linearGradient>
      <linearGradient id="bar-{key}"><stop stop-color="#658EA9"/><stop offset=".5" stop-color="#BFDEED"/><stop offset="1" stop-color="#719AB5"/></linearGradient>
    </defs>''')
    root.insert(0, defs)
    root.insert(1, element("rect", x=5, y=7, width=width-2, height=height-2, rx=9, fill="#010408"))
    background = next(node for node in root.iter(f"{{{NS}}}rect") if node.get("height") == "99%")
    background.attrib.update(width=str(width-2), height=str(height-2), rx="9", ry="9",
                             fill=f"url(#metal-{key})", stroke="#40586C")
    for parent in list(root.iter()):
        for node in list(parent):
            if node.tag == f"{{{NS}}}rect" and node.get("class") == "bar":
                x,y,w,h = (float(node.get(attr)) for attr in ("x","y","width","height"))
                if h > 0:
                    index = list(parent).index(node)
                    cap = element("path", d=f"M{x} {y}l3 -3h{w}l-3 3Z", fill="#D5ECF7")
                    side = element("path", d=f"M{x+w} {y}l3 -3v{h}l-3 3Z", fill="#304F68")
                    parent.insert(index,side)
                    parent.insert(index,cap)
                node.set("fill",f"url(#bar-{key})")
            if node.tag == f"{{{NS}}}path" and "A60,60" in node.get("d",""):
                index = list(parent).index(node)
                bottom = deepcopy(node)
                bottom.set("transform","translate(0 9) scale(1 .72)")
                bottom.set("style","fill:#203A50;stroke-width:1px")
                bottom.set("stroke","#182D3F")
                parent.insert(index,bottom)
                node.set("transform","scale(1 .72)")
    for node in root.iter(f"{{{NS}}}text"):
        style = node.get("style", "")
        node.set("style",re.sub(r"fill:\s*[^;]+", "fill:#BBD0DF", style))
    title = next(root.iter(f"{{{NS}}}text"))
    title.set("style",title.get("style","").replace("#BBD0DF","#F0F7FC"))
    style = element("style")
    style.text = ".gpsc-root *,.gpsc-item,.gpsc-chart,rect.bar,.arc,.gpsc-reveal{animation:none!important}"
    root.append(style)
    root.set("viewBox",f"-5 -5 {width+15} {height+18}")
    root.set("width",str(width+15))
    root.set("height",str(height+18))
    assert labels == [node.text for node in root.iter(f"{{{NS}}}text")], "Chart values changed"
    path.write_text(ET.tostring(root,encoding="unicode"),encoding="utf-8")

for name, files in [("analytics-depth",["2-most-commit-language.svg","4-productive-time.svg"]),
                    ("metrics-depth",["3-stats.svg","1-repos-per-language.svg"])]:
    for mobile in (False,True):
        width,height = (520,650) if mobile else (1000,310)
        combined = element("svg",viewBox=f"0 0 {width} {height}",role="img")
        title = element("title")
        title.text = "GitHub language and time-of-day analytics" if name.startswith("analytics") else "GitHub metrics and repository languages"
        combined.append(title)
        for index, filename in enumerate(files):
            card = ET.parse(directory/filename).getroot()
            card.attrib.update(x=str(0 if mobile else index*510),y=str(index*330 if mobile else 0),
                               width=str(520 if mobile else 490),height=str(319 if mobile else 301))
            combined.append(card)
        target = directory/f"{name}{'-mobile' if mobile else ''}.svg"
        target.write_text(ET.tostring(combined,encoding="unicode"),encoding="utf-8")
print("Verified: chart labels and source values preserved; dimensional desktop/mobile panels generated")
