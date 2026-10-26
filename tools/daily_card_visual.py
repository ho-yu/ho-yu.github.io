"""Approved visual-first card renderer. Evidence records require human/agent review."""
import argparse
import ast
from datetime import date
from functools import lru_cache
import hashlib
import io
import json
import math
from pathlib import Path
import re
import tokenize
from PIL import Image, ImageDraw, ImageFont

WIDTH, SCALE = 1080, 2
MARGIN, CONTENT = 48, 984
INNER_X, INNER_W = 86, 908
BG, INK, MUTED = '#F5F4EF', '#233A3B', '#647674'
PALETTE = [('#177B72','#E4F2EC'),('#4476B5','#EAF1FC'),('#7960A5','#F0EBF8'),('#BA7539','#FFF0DD')]
FONT_PATH = BOLD_PATH = None
ASSETS = Path(__file__).resolve().parent/'assets'/'daily-card'
STYLE = 'visual-first-rounded-v1'

@lru_cache(maxsize=128)
def load_font(size, bold=False, code=False):
    if code:
        candidates = ['C:/Windows/Fonts/consola.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf']
    else:
        candidates = [BOLD_PATH if bold and BOLD_PATH else FONT_PATH,ASSETS/('NanumSquareRoundB.ttf' if bold else 'NanumSquareRoundR.ttf')]
    for candidate in candidates:
        if candidate and Path(candidate).is_file(): return ImageFont.truetype(str(candidate),size)
    raise ValueError('Required rounded Korean font or monospace code font is missing.')

def wrap_text(value, font, width):
    measure=ImageDraw.Draw(Image.new('RGB',(1,1))); lines=[]
    for paragraph in value.split('\n'):
        line=''
        for token in re.findall(r'\S+|\s+',paragraph):
            if measure.textlength(line+token,font=font)<=width:
                line+=token; continue
            if line.strip(): lines.append(line.rstrip()); line=''
            for char in token.lstrip():
                if measure.textlength(line+char,font=font)>width:
                    if not line: raise ValueError('Text area is narrower than a glyph.')
                    lines.append(line); line=''
                line+=char
        if line.strip() or not paragraph: lines.append(line.rstrip())
    return lines

def validate(data):
    for key in ['date','title','summary','remember']:
        if not isinstance(data.get(key),str) or not data[key].strip(): raise ValueError(f'{key} must be nonempty text')
    date.fromisoformat(data['date'])
    if not data.get('sources') or not data.get('sections'): raise ValueError('Real sources and substantive sections are required')
    verification=data.get('verification',{})
    if verification.get('status')!='verified': raise ValueError('Concept and diagram verification must be completed first')
    date.fromisoformat(verification.get('checked_at',''))
    visible=[data['title'],data['summary'],data['remember']]
    for section in data['sections']:
        if not section.get('title') or not section.get('body') or any(not isinstance(p,str) or not p.strip() for p in section['body']): raise ValueError('Each section needs a title and concise explanation')
        evidence=section.get('verification',{})
        if not evidence.get('claim') or not evidence.get('sources'): raise ValueError('Every concept and diagram needs a checked claim and primary sources')
        if any(not re.match(r'^https://',s.get('url','')) for s in evidence['sources']): raise ValueError('Verification references need valid HTTPS URLs')
        visual=section.get('visual',{}); kind=visual.get('type')
        if kind not in ['flow','compare','pairing','matrix','curve']: raise ValueError('Every concept needs a supported diagram')
        if kind in ['flow','compare','pairing']:
            items=visual.get('items',[])
            if not 2<=len(items)<=4 or any(not isinstance(i,dict) or not i.get('label') for i in items): raise ValueError('Diagram needs 2–4 labeled items')
        if kind=='matrix' and not 1<=len(visual.get('shape',[]))<=4: raise ValueError('Matrix diagram needs 1–4 explicit axis lengths')
        if kind=='curve' and visual.get('function') not in ['relu','sigmoid','tanh','quadratic']: raise ValueError('Unsupported mathematical function')
        example=section.get('example')
        if example: ast.parse(example['code'])
        visible.extend([section['title'],*section['body'],json.dumps(visual,ensure_ascii=False)])
        if example: visible.extend([example.get('title',''),example['code'],example.get('explanation','')])
    if any(re.search(r'https?://|www\.',s) for s in visible): raise ValueError('Images must not contain URLs')

class Canvas:
    def __init__(self):
        self.commands=[]; self.text_bounds=[]; self.panels=[]
        self.measure=ImageDraw.Draw(Image.new('RGB',(1,1)))

    def box(self,x,y,w,h,fill='#FFFFFF',radius=22,outline=None): self.commands.append(('box',(x,y,w,h),fill,radius,outline))
    def line(self,points,color=INK,width=3): self.commands.append(('line',points,color,width))
    def circle(self,x,y,r,fill,outline=None): self.commands.append(('circle',(x,y,r),fill,outline))
    def arrow(self,x1,y1,x2,y2,color=PALETTE[0][0]):
        self.line([(x1,y1),(x2,y2)],color,4); a=math.atan2(y2-y1,x2-x1)
        self.line([(x2-13*math.cos(a-.55),y2-13*math.sin(a-.55)),(x2,y2),(x2-13*math.cos(a+.55),y2-13*math.sin(a+.55))],color,4)

    def text(self,value,x,y,width=INNER_W,size=38,bold=False,color=INK,center=False,code=False,line_height=None):
        # The approved font lacks these math glyphs; retain their exact meaning in ASCII.
        if not code:value=str(value).replace('ᵀ','^T').replace('−','-')
        face=load_font(size*SCALE,bold,code); step=line_height or round(size*1.4)
        for value in wrap_text(str(value),face,width*SCALE):
            length=self.measure.textlength(value,font=face)/SCALE
            left=x+(width-length)/2 if center else x
            if left<0 or left+length>WIDTH+.1: raise ValueError(f'Text overflow: {value}')
            self.commands.append(('text',(left,y),value,face,color))
            self.text_bounds.append({'text':value,'box':[round(left,2),y,round(left+length,2),y+size]}); y+=step
        return y

    def pill(self,value,x,y,w,fill,color,size=32,h=58):
        self.box(x,y,w,h,fill,h//2)
        self.text(value,x+10,y+(h-size)/2-1,w-20,size,True,color,True,line_height=size+6)

    def icon(self,kind,x,y,w=100,h=92,color=PALETTE[0][0],fill='#FFFFFF'):
        if kind in ('document','token'):
            self.box(x+w*.23,y,w*.55,h,fill,11,color)
            for i in range(3): self.line([(x+w*.33,y+h*(.28+.23*i)),(x+w*(.66 if i<2 else .54),y+h*(.28+.23*i))],color,3)
        elif kind in ('vector','chart'):
            for i,r in enumerate([.4,.75,.57,1,.65]): self.box(x+i*w/5,y+h*(1-r),w/5-7,h*r,color,4)
        elif kind=='grid':
            for row in range(3):
                for col in range(4): self.box(x+col*w/4,y+row*h/3,w/4-7,h/3-7,color if row==0 else fill,4,color)
        elif kind=='network':
            nodes=[[(x,y+h*.2),(x,y+h*.8)],[(x+w*.5,y),(x+w*.5,y+h*.5),(x+w*.5,y+h)],[(x+w,y+h*.5)]]
            for left,right in zip(nodes,nodes[1:]):
                for a in left:
                    for b in right:self.line([a,b],color,2)
            for layer in nodes:
                for px,py in layer:self.circle(px,py,9,fill,color)
        elif kind=='filter': self.line([(x,y),(x+w,y),(x+w*.6,y+h*.55),(x+w*.6,y+h),(x+w*.4,y+h),(x+w*.4,y+h*.55),(x,y)],color,4)
        elif kind=='loop':
            self.line([(x+w*.2,y),(x+w*.85,y),(x+w*.85,y+h*.8),(x+w*.2,y+h*.8)],color,4)
            self.arrow(x+w*.2,y+h*.8,x+w*.2,y+h*.15,color)
        elif kind=='calculator':
            self.box(x+w*.15,y,w*.7,h,fill,13,color); self.box(x+w*.26,y+h*.16,w*.48,h*.17,color,3)
            for r in range(2):
                for c in range(3):self.circle(x+w*(.31+c*.19),y+h*(.54+r*.24),4,color)
        else:
            self.box(x+w*.13,y,w*.74,h,fill,15,color); self.text('#',x+w*.13,y+7,w*.74,67,True,color,True)

    def diagram(self,visual,y):
        kind=visual['type']
        if kind in ('flow','compare'):
            items=visual['items']; n=len(items)
            if kind=='flow' and n==4:
                for i,item in enumerate(items):
                    color,fill=PALETTE[i%4]; self.box(INNER_X,y,INNER_W,130,fill)
                    self.icon(item.get('icon','number'),110,y+22,70,80,color)
                    self.text(item['label'],214,y+18,730,38,True,color)
                    self.text(item.get('detail',''),214,y+76,730,32,color=MUTED); y+=130
                    if i<n-1:self.arrow(540,y+8,540,y+35); y+=45
            else:
                cols=2 if n==4 else n; gap=28; w=(INNER_W-gap*(cols-1))/cols
                for ri in range(math.ceil(n/cols)):
                    row=items[ri*cols:ri*cols+cols]; heights=[]
                    for ci,item in enumerate(row):
                        idx=ri*cols+ci; x=INNER_X+ci*(w+gap); color,fill=PALETTE[idx%4]
                        start=len(self.commands);self.icon(item.get('icon','document'),x+w/2-45,y+25,90,86,color)
                        bottom=self.text(item['label'],x+14,y+138,w-28,36,True,color,True)
                        bottom=self.text(item.get('detail',''),x+14,bottom+10,w-28,31,color=MUTED,center=True)
                        h=max(242,bottom-y+22);heights.append(h)
                        self.commands.insert(start,('box',(x,y,w,h),fill,22,None))
                        if kind=='flow' and ci<len(row)-1:self.arrow(x+w+3,y+100,x+w+gap-3,y+100)
                    y+=max(heights)+24
        elif kind=='pairing':
            for i,item in enumerate(visual['items']):
                color,fill=PALETTE[i%4]
                left=wrap_text(item['label'],load_font(37),330);right=wrap_text(item.get('detail',''),load_font(37),330)
                h=max(94,max(len(left),len(right))*52+30)
                self.box(86,y,354,h,fill,18);self.box(640,y,354,h,fill,18)
                self.text(item['label'],98,y+22,330,37,True,color,True)
                self.text(item.get('detail',''),652,y+22,330,37,True,color,True)
                self.line([(440,y+h/2),(640,y+h/2)],color,3)
                self.circle(540,y+h/2,7,color);y+=h+24
        elif kind=='matrix':
            self.box(86,y,908,302,'#F3F7F3',22)
            shape_values=visual['shape']
            numeric=all(isinstance(v,int) and v>0 for v in shape_values)
            rows=min(shape_values[-2],5) if numeric and len(shape_values)>1 else (1 if len(shape_values)==1 else 4)
            cols=min(shape_values[-1],10) if numeric else 6
            layers=min(shape_values[0],3) if numeric and len(shape_values)>2 else (2 if len(shape_values)>2 else 1)
            cell_w=min(43,230/cols);cell_h=min(35,154/rows)
            for layer in reversed(range(layers)):
                self.box(116+layer*12,y+37-layer*8,cols*cell_w+20,rows*cell_h+20,'#E4F2EC',8,'#A4CDBE')
                for row in range(rows):
                    for col in range(cols):self.box(126+layer*12+col*cell_w,y+47-layer*8+row*cell_h,cell_w-7,cell_h-7,PALETTE[0][0] if row==0 else '#B9D9CF',3)
            exact=numeric and len(shape_values)<=3 and shape_values[-1]<=10 and (len(shape_values)==1 or shape_values[-2]<=5) and (len(shape_values)<3 or shape_values[0]<=3)
            self.text('배열 구조' if exact else '구조 도식 · 칸 수 축약',111,y+225,300,25,color=MUTED,center=True)
            shape='('+', '.join(str(n) for n in visual['shape'])+(',' if len(visual['shape'])==1 else '')+')'
            end=self.text(shape,435,y+39,530,47,True,PALETTE[0][0],code=True)
            for label in visual.get('labels',[]):end=self.text(label,440,end+10,520,31,color=MUTED)
            if end>y+290:raise ValueError('Matrix axis labels exceed panel; shorten labels')
            y+=326
        else:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import numpy as np
            name=visual['function'];x=np.linspace(-4,4,201)
            vals={'relu':lambda:np.maximum(x,0),'sigmoid':lambda:1/(1+np.exp(-x)),'tanh':lambda:np.tanh(x),'quadratic':lambda:x*x}[name]()
            fig,ax=plt.subplots(figsize=(9.08,3.1),dpi=200)
            fig.set_facecolor('#F3F7F3');ax.set_facecolor('#F3F7F3')
            ax.plot(x,vals,color=PALETTE[0][0],linewidth=3)
            ax.axhline(0,color='#8FA5A0',linewidth=1);ax.axvline(0,color='#8FA5A0',linewidth=1)
            ax.set_xlabel('x',fontsize=16);ax.set_ylabel('f(x)',fontsize=16);ax.tick_params(labelsize=13)
            for edge in ax.spines.values():edge.set_visible(False)
            fig.tight_layout(pad=1.1);buf=io.BytesIO();fig.savefig(buf,format='png',facecolor=fig.get_facecolor());plt.close(fig)
            plot=Image.open(buf).convert('RGB').copy();self.commands.append(('image',(86,y,908,310),plot));y+=334
        if visual.get('caption'):y=self.text(visual['caption'],86,y+3,908,33,color=MUTED,center=True)
        return y+18

    def code(self,example,y):
        lines=example['code'].splitlines();size=37;step=53;face=load_font(size*SCALE,code=True)
        for s in lines:
            if self.measure.textlength(s,font=face)>852*SCALE:raise ValueError('Code line too long; wrap source code explicitly: '+s)
        height=98+len(lines)*step+23;self.box(86,y,908,height,'#21383A',22)
        self.text('PYTHON · '+example.get('title','짧은 예시'),112,y+23,852,28,True,'#AED5C8')
        for i,s in enumerate(lines):self.text(s,114,y+78+i*step,852,size,color='#EDF4EF',code=True,line_height=step)
        colors={tokenize.STRING:'#EBC091',tokenize.NUMBER:'#EBC091',tokenize.COMMENT:'#95AAA5'}
        for tok in tokenize.generate_tokens(io.StringIO(example['code']).readline):
            color=colors.get(tok.type)
            if tok.type==tokenize.NAME and tok.string in ('for','in','if','else','with','True','False','None','import','from'):color='#BAAFEC'
            if color and tok.start[0]<=len(lines):
                before=lines[tok.start[0]-1][:tok.start[1]];x=114+self.measure.textlength(before,font=face)/SCALE
                self.text(tok.string,x,y+78+(tok.start[0]-1)*step,WIDTH-x-60,size,color=color,code=True,line_height=step)
        y+=height
        if example.get('explanation'):y=self.text(example['explanation'],86,y+24,908,33,color=MUTED,center=True)
        return y+18

    def save(self,path,height):
        im=Image.new('RGB',(WIDTH*SCALE,height*SCALE),BG);d=ImageDraw.Draw(im)
        for kind,*p in self.commands:
            if kind=='box':
                (x,y,w,h),fill,r,outline=p;d.rounded_rectangle((x*SCALE,y*SCALE,(x+w)*SCALE,(y+h)*SCALE),radius=r*SCALE,fill=fill,outline=outline,width=2*SCALE)
            elif kind=='text':
                (x,y),s,face,color=p;d.text((x*SCALE,y*SCALE),s,font=face,fill=color,anchor='lt')
            elif kind=='line':
                points,color,width=p;d.line([(x*SCALE,y*SCALE) for x,y in points],fill=color,width=width*SCALE,joint='curve')
            elif kind=='circle':
                (x,y,r),fill,outline=p;d.ellipse(((x-r)*SCALE,(y-r)*SCALE,(x+r)*SCALE,(y+r)*SCALE),fill=fill,outline=outline,width=2*SCALE)
            elif kind=='image':
                (x,y,w,h),plot=p;im.paste(plot.resize((w*SCALE,h*SCALE),Image.Resampling.LANCZOS),(x*SCALE,y*SCALE))
        if any(t['box'][3]>=height for t in self.text_bounds):raise ValueError('Text extends past canvas bottom')
        im.resize((WIDTH,height),Image.Resampling.LANCZOS).save(path,format='PNG',optimize=True)

def render_card(data,output):
    validate(data);c=Canvas()
    c.pill('KANT · DAILY LEARNING',48,46,400,PALETTE[0][1],PALETTE[0][0],28,54)
    c.text(data['date'].replace('-','.'),800,59,232,30,color=MUTED,center=True)
    y=c.text(data['title'],58,142,964,73,True,line_height=96)
    y=c.text(data['summary'],61,y+22,958,38,color=MUTED)+42
    for i,section in enumerate(data['sections'],1):
        start=len(c.commands);top=y;y+=32
        c.pill(f'{i:02d}',78,y,72,PALETTE[0][1],PALETTE[0][0],28,52)
        y=c.text(section['title'],170,y+3,824,48,True,line_height=64)
        for sentence in section['body']:y=c.text(sentence,86,y+13,908,37,color=MUTED)
        y=c.diagram(section['visual'],y+26)
        if section.get('example'):y=c.code(section['example'],y+8)
        y+=24;c.commands.insert(start,('box',(48,top,984,y-top),'#FFFFFF',30,None))
        c.panels.append({'section':section['title'],'top':top,'bottom':y,'visual':section['visual']['type']});y+=28
    start=len(c.commands);top=y;y+=34
    y=c.text('오늘 기억할 한 줄',86,y,908,30,True,'#AAD7C9')
    y=c.text(data['remember'],86,y+22,908,48,True,'#FFFFFF')+40
    c.commands.insert(start,('box',(48,top,984,y-top),INK,30,None))
    y=c.text(data['date'].replace('-','.')+' · AI 학습 카드',58,y+40,964,27,color=MUTED)+45
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);height=math.ceil(y);c.save(output,height)
    result={'path':str(output.resolve()),'date':data['date'],'style':STYLE,'width':WIDTH,'height':height,'bytes':output.stat().st_size,
            'verification_date':data['verification']['checked_at'],'data_sha256':hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
            'image_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'sections':len(data['sections']),'diagrams':len(c.panels)}
    output.with_name('render.json').write_text(json.dumps({**result,'panels':c.panels,'text_bounds':c.text_bounds},ensure_ascii=False,indent=2),encoding='utf-8')
    return result

def main():
    global FONT_PATH,BOLD_PATH
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('inputs',nargs='+',type=Path)
    parser.add_argument('--font');parser.add_argument('--bold-font');args=parser.parse_args()
    FONT_PATH,BOLD_PATH=args.font,args.bold_font;load_font.cache_clear()
    for source in args.inputs:
        data=json.loads(source.read_text(encoding='utf-8-sig'))
        print(json.dumps(render_card(data,source.with_name(f'{data["date"]}-daily-card.png')),ensure_ascii=True),flush=True)

if __name__=='__main__':main()
