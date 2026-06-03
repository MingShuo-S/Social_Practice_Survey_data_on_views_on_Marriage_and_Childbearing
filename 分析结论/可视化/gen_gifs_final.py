"""Final GIF generation: growth for bar/donut/radar/text, emphasis for bubble."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, FancyBboxPatch
import numpy as np
from math import pi
from PIL import Image
import os, warnings, io
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DengXian']
plt.rcParams['axes.unicode_minus'] = False

OUT = r'C:\Users\29548\Desktop\阳关\南京大学\社会实践\思修\可视化'

P = '#FF6B9D'; DP = '#C2185B'; BG = '#1a0a14'; LT = '#fce4ec'
MU = '#AD8A9E'; G = '#FFAB91'; GN = '#4CAF50'; BL = '#42A5F5'

FPS = 16
ANIM_SEC = 2.5; HOLD_SEC = 4.5
AF = int(FPS * ANIM_SEC); HF = int(FPS * HOLD_SEC); TF = AF + HF

def ease(t):
    return t * t * (3 - 2 * t)

def setup(ax, t=''):
    ax.set_facecolor('#2d1225')
    ax.set_title(t, color=P, fontsize=14, fontweight='bold', pad=12)
    ax.tick_params(colors=LT, labelsize=9)
    for s in ax.spines.values(): s.set_color('#4a2a3a')

DPI = 150

def save_gif(frames, name):
    path = os.path.join(OUT, f'{name}.gif')
    dur = int(1000 / FPS)
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=dur, loop=0, optimize=False)
    return path

def render(fig):
    buf = io.BytesIO()
    fig.savefig(buf, dpi=DPI, bbox_inches='tight', pad_inches=0.15,
                facecolor=fig.get_facecolor(), format='png')
    buf.seek(0)
    return Image.open(buf).convert('RGBA')

def anim_progress(f):
    if f < AF: return ease(f / max(1, AF - 1))
    return 1.0

# ═══════════════════════════════════════════════
# GROWTH TYPE (expand/build from zero)
# ═══════════════════════════════════════════════

def c1_growth():
    """Donut: segments sweep in one by one."""
    labels = ['向往\n48%','顺其自然\n35%','不明确\n7%','其他\n10%']
    sizes = [48,35,7,10]; colors = [P,MU,G,BL]; total=sum(sizes); N=len(sizes)
    seg_angles = []; s=0
    for sz in sizes: e=s+sz/total*360; seg_angles.append((s,e)); s=e
    frames = []
    for f in range(TF):
        fig,ax = plt.subplots(figsize=(6,4.8), facecolor=BG)
        setup(ax,'婚姻态度分布')
        ax.set_xlim(-1.6,1.6); ax.set_ylim(-1.6,1.6); ax.set_aspect('equal'); ax.axis('off')
        ep = anim_progress(f)
        for i,((s_deg,e_deg),c) in enumerate(zip(seg_angles,colors)):
            local_p = max(0,min(1,(ep-i/N)*N))
            if local_p>0:
                lep = ease(min(local_p,1))
                w = Wedge((0,0),1,s_deg,s_deg+(e_deg-s_deg)*lep,width=0.45,
                          facecolor=c,edgecolor='white',linewidth=2.5)
                ax.add_patch(w)
        ax.add_patch(plt.Circle((0,0),0.55,fc=BG))
        for i,((s_deg,e_deg),l) in enumerate(zip(seg_angles,labels)):
            if ep > (i+1)/N - 0.1:
                mid=(s_deg+e_deg)/2; r=mid*pi/180
                cx,cy=1.35*np.cos(r),1.35*np.sin(r)
                al = max(0,min(1,(ep-(i+1)/N+0.15)*10))
                ax.text(cx,cy,l,color=LT,fontsize=11,ha='center',va='center',fontweight='bold',alpha=al)
        for i,((s_deg,e_deg),sz) in enumerate(zip(seg_angles,sizes)):
            if ep > (i+1)/N - 0.05:
                mid=(s_deg+e_deg)/2; r=mid*pi/180
                cx,cy=0.78*np.cos(r),0.78*np.sin(r)
                al = max(0,min(1,(ep-(i+1)/N+0.1)*10))
                ax.text(cx,cy,f'{sz}%',color=BG,fontsize=10,ha='center',va='center',fontweight='bold',alpha=al)
        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_1_增长型')

def c2_growth():
    """Bar: bars grow from bottom."""
    cats=['婚恋积极','生育积极']; vals=[3.72,3.15]; cs=[GN,P]
    frames=[]
    for f in range(TF):
        fig,ax=plt.subplots(figsize=(6,4.8),facecolor=BG); setup(ax,'婚恋 vs 生育态度 [p<0.001]')
        ax.set_ylim(0,4.5); ax.set_ylabel('均值',color=LT)
        ep=anim_progress(f); hs=[v*ep for v in vals]
        ax.bar(cats,hs,color=cs,width=0.5,edgecolor='white',linewidth=2)
        for i,h in enumerate(hs):
            if h>0.1: ax.text(i,h+0.07,f'{vals[i]:.2f}',color=LT,fontsize=12,ha='center',fontweight='bold')
        ax.text(0.5,0.95,'p<0.001',transform=ax.transAxes,color=LT,fontsize=9,ha='center',va='top',style='italic')
        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_2_增长型')

def c3_growth():
    """Radar: 3 Likert dimensions (1-5) + annotation for 2 percentage items."""
    dims=['婚姻积极态度','生育态度积极','认同婚姻风险']
    # Likert 1-5 means by gender
    m=[3.92,3.45,3.55]; f=[3.35,2.70,4.25]
    # Percentage items (multi-select mention rate)
    p_labels=['看中经济条件','看重外貌']
    p_m=[9,34]; p_f=[22,12]
    N=len(dims); angles=[(n/float(N)*2*pi + pi/3) for n in range(N)]; angles+=angles[:1]
    m_cl=m+m[:1]; f_cl=f+f[:1]
    frames=[]
    for fr in range(TF):
        ep=anim_progress(fr)
        fig=plt.figure(figsize=(7.5,5.4),facecolor=BG)
        # Radar on left (wider figure, more space)
        ax=fig.add_axes([0.03,0.12,0.48,0.78],polar=True)
        ax.set_facecolor('#2d1225')
        ax.set_title('性别差异雷达 (李克特1-5分)',color=P,fontweight='bold',pad=20,fontsize=12)
        ax.tick_params(colors=LT,labelsize=8)
        ax.set_xticks(angles[:-1]); ax.set_xticklabels(dims,color=LT,fontsize=10)
        ax.set_ylim(0,5); ax.set_yticks([1,2,3,4,5])
        m_cur=[m[i]*min(1,ep*1.2) for i in range(N)]+[m[0]*min(1,ep*1.2)]
        f_cur=[f[i]*min(1,ep*1.2) for i in range(N)]+[f[0]*min(1,ep*1.2)]
        ax.fill(angles,m_cur,alpha=0.12,color=BL)
        ax.fill(angles,f_cur,alpha=0.12,color=P)
        ax.plot(angles,m_cur,'o-',color=BL,linewidth=2.5,label='男生')
        ax.plot(angles,f_cur,'o-',color=P,linewidth=2.5,label='女生')
        ax.legend(loc='upper right',labelcolor=[BL,P],fontsize=9)
        # Percentage items on right as annotation
        ax2=fig.add_axes([0.58,0.15,0.38,0.6])
        ax2.set_facecolor('#2d1225'); ax2.set_xlim(0,50); ax2.set_ylim(-0.5,1.5)
        ax2.set_title('多选提及率',color=P,fontsize=11,fontweight='bold')
        ax2.tick_params(colors=LT,labelsize=7)
        ax2.set_xticks([0,10,20,30,40]); ax2.set_xticklabels(['0','10','20','30','40%'],color=LT,fontsize=7)
        ax2.set_yticks([0,1]); ax2.set_yticklabels(p_labels,color=LT,fontsize=8)
        for s in ax2.spines.values(): s.set_color('#4a2a3a')
        for i in range(2):
            h_m=p_m[i]*min(1,ep*1.2); h_f=p_f[i]*min(1,ep*1.2)
            ax2.barh(i-0.15,h_m,height=0.25,color=BL,edgecolor='white',linewidth=1)
            ax2.barh(i+0.15,h_f,height=0.25,color=P,edgecolor='white',linewidth=1)
            if h_m>3: ax2.text(h_m+0.5,i-0.15,f'{p_m[i]}%',color=LT,fontsize=8,va='center')
            if h_f>3: ax2.text(h_f+0.5,i+0.15,f'{p_f[i]}%',color=LT,fontsize=8,va='center')
        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_3_增长型')

def c5_growth():
    """Grouped bar: bars grow from bottom."""
    cats=['稳定和谐','离异/矛盾']; cs=[GN,DP]; v1=[62,28]; v2=[18,45]
    frames=[]
    for f in range(TF):
        fig,ax=plt.subplots(figsize=(6,4.8),facecolor=BG)
        setup(ax,'父母婚姻质量影响 [\u03c7\u00b2=15.3, p<0.001]')
        x=np.arange(2); w=0.3
        ep=anim_progress(f); h1=[v*ep for v in v1]; h2=[v*ep for v in v2]
        ax.bar(x-w/2,h1,w,color=cs,edgecolor='white',linewidth=2,label='向往婚姻')
        ax.bar(x+w/2,h2,w,color=[c+'88' for c in cs],edgecolor='white',linewidth=2,label='不婚不育倾向')
        ax.set_xticks(x); ax.set_xticklabels(cats,color=LT,fontsize=10)
        ax.set_ylabel('比例 (%)',color=LT); ax.set_ylim(0,75)
        ax.legend(labelcolor=[P,LT],fontsize=9)
        for i,h in enumerate(h1):
            if h>1: ax.text(i-w/2,h+1.5,f'{v1[i]}%',color=LT,fontsize=10,ha='center',fontweight='bold')
        for i,h in enumerate(h2):
            if h>1: ax.text(i+w/2,h+1.5,f'{v2[i]}%',color=LT,fontsize=10,ha='center',fontweight='bold')
        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_5_增长型')

def c6_growth():
    """Bar: bars grow from bottom."""
    labs=['经济压力\n53%','个人发展\n46%','时间精力\n42%','身体伤害\n37%','责任失衡\n31%']
    vals=[53,46,42,37,31]; cs=[P,MU,G,BL,GN]
    frames=[]
    for f in range(TF):
        fig,ax=plt.subplots(figsize=(6.5,4.8),facecolor=BG); setup(ax,'大学生生育顾虑')
        x=np.arange(5)
        ep=anim_progress(f); hs=[v*ep for v in vals]
        ax.bar(x,hs,color=cs,width=0.6,edgecolor='white',linewidth=2)
        ax.set_xticks(x); ax.set_xticklabels(labs,color=LT,fontsize=9); ax.set_ylim(0,65)
        ax.set_ylabel('提及比例 (%)',color=LT)
        for i,h in enumerate(hs):
            if h>1: ax.text(i,h+1.5,f'{vals[i]}%',color=LT,fontsize=10,ha='center',fontweight='bold')
        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_6_增长型')

def c7_growth():
    """Bar: bars grow from bottom."""
    parts=['接触内容\n83%','自报影响\n73%','改变看法\n7%']; vals=[83,73,7]; cs=[P,MU,G]
    frames=[]
    for f in range(TF):
        fig,ax=plt.subplots(figsize=(6,4.8),facecolor=BG); setup(ax,'网络影响真实数据')
        x=np.arange(3)
        ep=anim_progress(f); hs=[v*ep for v in vals]
        ax.bar(x,hs,color=cs,width=0.5,edgecolor='white',linewidth=2)
        ax.set_xticks(x); ax.set_xticklabels(parts,color=LT,fontsize=10); ax.set_ylim(0,95)
        ax.set_ylabel('比例 (%)',color=LT)
        for i,h in enumerate(hs):
            if h>1: ax.text(i,h+2,f'{vals[i]}%',color=LT,fontsize=11,ha='center',fontweight='bold')
        ax.text(0.95,0.05,'*83%+73%+7%≠100%\n因分属不同题目',transform=ax.transAxes,color=MU,fontsize=7,
                ha='right',va='bottom',style='italic')
        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_7_增长型')

def c8_growth():
    """Dual bar: bars grow from bottom."""
    grades=['大一','大二','大三+']; vg=[52,45,35]
    areas=['一线','新一线','三四线','县城','农村']; va=[79,68,60,58,55]
    cg=[P,MU,G]; ca=[P,MU,G,BL,GN]
    frames=[]
    for f in range(TF):
        fig,(ax1,ax2)=plt.subplots(1,2,figsize=(8.5,4.2),facecolor=BG)
        setup(ax1,'年级差异 [\u03c7\u00b2=6.2, p=0.045]')
        setup(ax2,'生源地差异 [\u03c7\u00b2=8.7, p=0.013]')
        ep=anim_progress(f)
        h1=[v*ep for v in vg]; h2=[v*ep for v in va]
        ax1.bar(np.arange(3),h1,color=cg,width=0.5,edgecolor='white',linewidth=2)
        ax2.bar(np.arange(5),h2,color=ca,width=0.5,edgecolor='white',linewidth=2)
        ax1.set_xticks(np.arange(3)); ax1.set_xticklabels(grades,color=LT,fontsize=9)
        ax2.set_xticks(np.arange(5)); ax2.set_xticklabels(areas,color=LT,fontsize=8,rotation=20)
        for ax in (ax1,ax2): ax.set_ylim(0,90); ax.set_ylabel('向往婚姻 (%)',color=LT)
        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_8_增长型')

def c9_reveal():
    """Forest plot: all 3 predictors grow together from 0, no one-by-one."""
    factors=['性别(男=1)','网络影响','学业压力']; beta=[0.32,-0.24,-0.19]
    ci_low=[0.13,-0.38,-0.33]; ci_high=[0.51,-0.10,-0.05]; cols=[P,BL,G]; N=3
    frames=[]
    for f in range(TF):
        fig,ax=plt.subplots(figsize=(6.5,4.8),facecolor=BG)
        setup(ax,'回归模型 [R\u00b2=0.23, p<0.001]')
        y=np.arange(N)
        ax.axvline(0,color='white',linewidth=0.8,linestyle='-',alpha=0.3)
        ax.set_yticks(y); ax.set_yticklabels(factors,color=LT,fontsize=10)
        ax.set_xlim(-0.55,0.7); ax.set_xlabel('标准化系数 \u03b2',color=LT)
        ep=anim_progress(f)

        for i in range(N):
            if ep < 0.05: continue
            lep = ease(min(1, (ep - i*0.05) * 1.2))
            current_beta = beta[i] * lep
            current_low = ci_low[i] * lep
            current_high = ci_high[i] * lep
            ax.plot([current_low,current_high],[y[i],y[i]],color=cols[i],linewidth=3,zorder=4)
            ax.scatter([current_beta],[y[i]],s=100,color=cols[i],
                       edgecolors='white',linewidth=2,zorder=5)
            if lep > 0.8:
                ax.text(beta[i]+0.03,y[i],f'\u03b2={beta[i]:.2f}',color=cols[i],
                        fontsize=10,va='center',fontweight='bold')

        ax.text(0.5,0.9,'p<0.001',transform=ax.transAxes,color=LT,fontsize=9,
                ha='center',style='italic')
        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_9_增长型')

def c10_growth():
    """Text: phase 1 show top text centered, phase 2 top moves up + bottom fades in."""
    t1 = '\u201c\u6211\u4eec\u6709\u8d44\u683c\u8ffd\u5bfb\u81ea\u5df1\u671f\u671b\u7684'
    t2 = '\u604b\u7231\u3001\u5a5a\u59fb\u4e0e\u751f\u80b2\u7ecf\u5386\u3002\u201d'
    b1 = '\u2014\u2014\u8fd9\u4e0d\u662f\u7231\u7684\u6d88\u5931\uff0c'
    b2 = '   \u800c\u662f\u7231\u7684\u7406\u6027\u5316\u3002'
    top = t1 + '\n' + t2
    bot = b1 + '\n' + b2
    P2 = 0.4; CY = 0.5; TY = 0.64; BY = 0.34
    frames=[]
    for f in range(TF):
        fig,ax=plt.subplots(figsize=(7,4),facecolor=BG)
        ax.set_facecolor(BG); ax.axis('off')
        ep = anim_progress(f)
        if ep < P2:
            p1 = ease(ep / P2); a1 = min(1, p1 * 1.5)
            ax.text(0.5, CY, top, color=LT, fontsize=18, ha='center', va='center',
                    fontweight='bold', linespacing=1.8, alpha=a1)
        else:
            p2 = (ep - P2) / (1 - P2)
            y1 = CY + (TY - CY) * ease(p2); a2 = min(1, p2 * 2.0)
            y2 = BY + (CY - BY) * (1 - ease(p2))
            ax.text(0.5, y1, top, color=LT, fontsize=18, ha='center', va='center',
                    fontweight='bold', linespacing=1.8, alpha=1.0)
            ax.text(0.5, y2, bot, color=LT, fontsize=16, ha='center', va='center',
                    fontweight='bold', linespacing=1.8, alpha=a2)
        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_10_增长型')

# ═══════════════════════════════════════════════
# EMPHASIS TYPE (1-2 rounds then pause)
# ═══════════════════════════════════════════════

def c4_emphasis():
    """Bubble: 2 rounds of highlighting then hold all visible."""
    labels=['父母/家庭','同辈/朋友','个人经历','网络/社媒','书籍/影视']
    vals=[40,25,20,10,5]; colors=[P,MU,G,BL,GN]; N=len(vals)
    rounds = 2
    frames_per_item = AF // (N * rounds)
    frames=[]
    for f in range(TF):
        fig,ax=plt.subplots(figsize=(7,4.8),facecolor=BG); setup(ax,'影响来源排序')
        ax.set_xlim(0,50); ax.set_ylim(-0.5,4.5)
        ax.set_yticks(range(N)); ax.set_yticklabels(labels,color=LT,fontsize=10)
        ax.set_xlabel('提及比例 (%)',color=LT)

        if f < AF:
            idx = (f // frames_per_item) % N
        else:
            idx = -1  # hold: all shown

        for i,(v,c) in enumerate(zip(vals,colors)):
            if idx < 0:
                al, sz_mul, lw = 0.9, 1.0, 1.5  # final state
            elif i == idx:
                al, sz_mul, lw = 1.0, 1.2, 2.5
            else:
                al, sz_mul, lw = 0.15, 1.0, 0.5
            sz = ((v * 1.2) ** 2) * sz_mul
            ax.scatter([v],[i],s=sz,color=c,alpha=al,
                       edgecolors='white',linewidth=lw,zorder=3)

        frames.append(render(fig)); plt.close(fig)
    return save_gif(frames,'动画_4_强调型')

if __name__=='__main__':
    funcs = [
        c1_growth, c2_growth, c3_growth, c4_emphasis,
        c5_growth, c6_growth, c7_growth, c8_growth,
        c9_reveal, c10_growth
    ]
    for fn in funcs:
        try:
            p = fn()
            n = os.path.basename(p)
            sz = os.path.getsize(p)//1024
            print(f'OK  {n} ({sz}KB)')
        except Exception as e:
            print(f'ERR {fn.__name__}: {e}')
    print('Done!')
