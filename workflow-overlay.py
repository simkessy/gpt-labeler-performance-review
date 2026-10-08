# /// script
# requires-python = ">=3.10"
# dependencies = ["svgwrite", "cairosvg"]
# ///
"""Overlay proposed changes on the unchanged current-workflow coordinates."""
from pathlib import Path
import argparse
import svgwrite

WIDTH, HEIGHT = 1200, 370
LEFT, STRIDE, NODE_W, NODE_H = 40, 160, 140, 76
BASE_Y, TOP_Y, BRANCH_Y = 145, 24, 271
INK, GREY, LINE = '#243b35', '#60716b', '#b4c1ba'
ACCENT, LIGHT, PAPER = '#176e5e', '#e4f2e9', '#f4f6f4'
FONT = 'Arial, Helvetica, sans-serif'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='workflow-overlay.svg')
    parser.add_argument('--preview')
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    drawing = svgwrite.Drawing(str(output), size=(WIDTH, HEIGHT), viewBox=f'0 0 {WIDTH} {HEIGHT}')
    drawing.set_desc(title='Proposed workflow over the current workflow', desc='The gray path is current. The green proposal skips sample and approval, adds label verification before publication, and keeps cleanup on a separate branch.')
    def marker(name, color):
        m = drawing.marker(id=name, insert=(8,4), size=(9,8), orient='auto', markerUnits='userSpaceOnUse')
        m.add(drawing.path(d='M0 0 L8 4 L0 8 Z', fill=color))
        drawing.defs.add(m)
        return m
    current_marker, proposed_marker = marker('current-arrow', LINE), marker('proposed-arrow', ACCENT)
    def path(points, proposed=False):
        value = 'M' + ' L'.join(f'{x},{y}' for x,y in points)
        p = drawing.path(d=value, fill='none', stroke=ACCENT if proposed else LINE, stroke_width=3 if proposed else 2, class_='proposed-route' if proposed else 'current-route')
        p['marker-end']=(proposed_marker if proposed else current_marker).get_funciri()
        drawing.add(p)
    def node(index, lines, y=BASE_Y, mode='keep'):
        x = LEFT + index * STRIDE
        group = drawing.g(class_='overlay-node '+mode)
        rect = drawing.rect(insert=(x,y), size=(NODE_W,NODE_H), rx=10, fill=LIGHT if mode in ('keep','added','parallel') else PAPER, stroke=ACCENT if mode in ('keep','added','parallel') else LINE, stroke_width=2)
        if mode in ('skipped','moved','parallel'):rect['stroke-dasharray']='6,4'
        group.add(rect)
        for i,line in enumerate(lines):
            baseline=y+NODE_H/2-(len(lines)-1)*11+6+i*22
            label=drawing.text(line,insert=(x+NODE_W/2,baseline),text_anchor='middle',font_family=FONT,font_size=18,font_weight=600,fill=GREY if mode in ('skipped','moved') else INK,class_='node-text')
            if mode=='skipped':label['text-decoration']='line-through'
            group.add(label)
        if mode=='skipped':
            cross_x,cross_y=x+NODE_W-14,y+13
            for a,b in [((-4,-4),(4,4)),((-4,4),(4,-4))]:group.add(drawing.line((cross_x+a[0],cross_y+a[1]),(cross_x+b[0],cross_y+b[1]),stroke=GREY,stroke_width=2.5))
        drawing.add(group)
    center_y=BASE_Y+NODE_H/2
    for i in range(6):path([(LEFT+i*STRIDE+NODE_W+2,center_y),(LEFT+(i+1)*STRIDE-3,center_y)])
    # Proposed route bypasses the two crossed-out nodes while retaining all anchors.
    path([(LEFT+NODE_W/2,BASE_Y-2),(LEFT+NODE_W/2,TOP_Y+NODE_H/2),(LEFT+3*STRIDE+NODE_W/2,TOP_Y+NODE_H/2),(LEFT+3*STRIDE+NODE_W/2,BASE_Y-3)],True)
    path([(LEFT+3*STRIDE+NODE_W+2,center_y),(LEFT+4*STRIDE-3,center_y)],True)
    path([(LEFT+4*STRIDE+NODE_W/2,BASE_Y-2),(LEFT+4*STRIDE+NODE_W/2,TOP_Y+NODE_H/2),(LEFT+5*STRIDE-3,TOP_Y+NODE_H/2)],True)
    path([(LEFT+5*STRIDE+NODE_W+2,TOP_Y+NODE_H/2),(LEFT+6*STRIDE+NODE_W/2,TOP_Y+NODE_H/2),(LEFT+6*STRIDE+NODE_W/2,BASE_Y-3)],True)
    path([(LEFT+4*STRIDE+NODE_W/2,BASE_Y+NODE_H+2),(LEFT+4*STRIDE+NODE_W/2,BRANCH_Y+NODE_H/2),(LEFT+5*STRIDE-3,BRANCH_Y+NODE_H/2)],True)
    specs=[(['Prepare','input'],'keep'),(['Label a','sample'],'skipped'),(['Approve','job'],'skipped'),(['Label the','full job'],'keep'),(['Save','labels'],'keep'),(['Cleanup','moves below'],'moved'),(['Publish','output'],'keep')]
    for index,(lines,mode) in enumerate(specs):node(index,lines,mode=mode)
    node(5,['Verify','all labels'],TOP_Y,'added')
    node(5,['Clean up','files'],BRANCH_Y,'parallel')
    drawing.add(drawing.text('Runs separately',insert=(LEFT+6*STRIDE,BRANCH_Y+NODE_H/2+6),font_family=FONT,font_size=18,fill=INK,class_='node-text'))
    drawing.save()
    if args.preview:
        import cairosvg
        cairosvg.svg2png(url=str(output),write_to=args.preview,output_width=1440)
    print(f'Saved {output}')

if __name__=='__main__':main()
