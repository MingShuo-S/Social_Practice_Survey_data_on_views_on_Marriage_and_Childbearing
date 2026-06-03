import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
from math import pi
import os, warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DengXian']
plt.rcParams['axes.unicode_minus'] = False

OUT = r'C:\Users\29548\Desktop\阳关\南京大学\社会实践\思修\可视化'
os.makedirs(OUT, exist_ok=True)

# Colors
P = '#FF6B9D'
DP = '#C2185B'
BG = '#1a0a14'
LT = '#fce4ec'
MU = '#AD8A9E'
G = '#FFAB91'
GN = '#4CAF50'
BL = '#42A5F5'
C1 = '#FF6B9D'
C2 = '#AD8A9E'
C3 = '#FFAB91'
C4 = '#42A5F5'
C5 = '#4CAF50'
C6 = '#CE93D8'

SW = ['#FF6B9D','#AD8A9E','#FFAB91','#42A5F5','#4CAF50','#CE93D8','#EF5350','#FFA726']

def setup(ax, t=''):
    ax.set_facecolor('#2d1225')
    ax.set_title(t, color=P, fontsize=14, fontweight='bold', pad=12)
    ax.tick_params(colors=LT, labelsize=9)
    for s in ax.spines.values():
        s.set_color('#4a2a3a')

def save_gif(fig, anim, name):
    p = os.path.join(OUT, f'{name}.gif')
    anim.save(p, writer=animation.PillowWriter(fps=4), dpi=100)
    plt.close(fig)
    return p

# ─── Chart 1: 婚姻态度分布 (Donut) ───
def chart1_growth():
    labels = ['向往\n48%','顺其自然\n35%','不明确\n7%','其他\n10%']
    sizes  = [48,35,7,10]; colors=[P, MU, G, BL]
    fig, ax = plt.subplots(figsize=(5,4), facecolor=BG)
    setup(ax,'婚姻态度分布')
    
    wedges, _ = ax.pie(sizes, labels=labels, colors=colors,
        startangle=90, textprops={'color':LT,'fontsize':9},
        wedgeprops={'linewidth':2,'edgecolor':'white'})
    for w in wedges:
        w.set_visible(False)
    
    def update(f):
        n = min(max(0,int(f/5))+1, len(wedges))
        for i,w in enumerate(wedges):
            w.set_visible(i < n)
        return wedges
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=25,blit=True),'动画_1_增长型')

def chart1_emphasis():
    labels = ['向往\n48%','顺其自然\n35%','不明确\n7%','其他\n10%']
    sizes=[48,35,7,10]; colors=[P, MU, G, BL]; cols_dim=[c+'44' for c in colors]
    fig, ax = plt.subplots(figsize=(5,4), facecolor=BG)
    setup(ax,'婚姻态度分布')
    
    wedges, _ = ax.pie(sizes, labels=labels, colors=cols_dim,
        startangle=90, textprops={'color':LT,'fontsize':9},
        wedgeprops={'linewidth':2,'edgecolor':'white'})
    
    def update(f):
        idx = int(f/8) % len(wedges)
        for i,w in enumerate(wedges):
            w.set_facecolor(colors[i] if i==idx else cols_dim[i])
            w.set_linewidth(4 if i==idx else 2)
        return wedges
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=40,blit=True),'动画_1_强调型')

# ─── Chart 2: 生育态度与对比 (Grouped Bar) ───
def chart2_growth():
    cats = ['婚恋积极','生育积极']; vals = [3.72, 3.15]; bars = [GN, P]
    fig, ax = plt.subplots(figsize=(5,4), facecolor=BG)
    setup(ax,'婚恋 vs 生育态度')
    ax.set_ylim(0,4.5); ax.set_ylabel('均值', color=LT)
    rects = ax.bar(cats, [0,0], color=bars, width=0.5, edgecolor='white')
    
    def update(f):
        frac = min(f/12, 1)
        for i,r in enumerate(rects):
            r.set_height(vals[i]*frac)
        return rects
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=15,blit=True),'动画_2_增长型')

def chart2_emphasis():
    cats=['婚恋积极','生育积极']; vals=[3.72,3.15]; bars=[GN, P]
    fig,ax=plt.subplots(figsize=(5,4),facecolor=BG)
    setup(ax,'婚恋 vs 生育态度'); ax.set_ylim(0,4.5); ax.set_ylabel('均值',color=LT)
    rects=ax.bar(cats, vals, color=[c+'44' for c in bars], width=0.5, edgecolor='white')
    
    def update(f):
        idx=int(f/8)%len(rects)
        for i,r in enumerate(rects):
            r.set_facecolor(bars[i] if i==idx else bars[i]+'44')
            r.set_linewidth(4 if i==idx else 2)
        return rects
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=24,blit=True),'动画_2_强调型')

# ─── Chart 3: 性别差异雷达 ───
def chart3_growth():
    dims = ['婚姻向往','生育意愿','亲密信任','经济独立','家庭观念']
    m = [4.2, 3.8, 4.0, 3.5, 3.6]; f = [3.5, 2.8, 3.8, 4.0, 3.2]
    N=len(dims); angles=[n/float(N)*2*pi for n in range(N)]; angles+=angles[:1]
    
    fig,ax=plt.subplots(figsize=(5,4.5),facecolor=BG,subplot_kw=dict(polar=True))
    ax.set_facecolor('#2d1225'); ax.set_title('性别差异',color=P,fontweight='bold',pad=20)
    ax.tick_params(colors=LT,labelsize=8)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(dims,color=LT,fontsize=9)
    ax.set_ylim(0,5)
    
    fill1=ax.fill(angles[:1],[0],alpha=0.1,color=P)[0]
    fill2=ax.fill(angles[:1],[0],alpha=0.1,color=BL)[0]
    l1,=ax.plot([],[],'o-',color=P,linewidth=2,label='男生')
    l2,=ax.plot([],[],'o-',color=BL,linewidth=2,label='女生')
    ax.legend(loc='upper right',labelcolor=[P,BL],fontsize=9)
    
    def update(fr):
        frac=min(fr/12,1)
        n=max(1,int(frac*N))
        m_dat=m[:n]+[m[n-1]]; f_dat=f[:n]+[f[n-1]]
        a=angles[:n+1]
        l1.set_data(a,m_dat); l2.set_data(a,f_dat)
        fill1.set_xy(np.c_[a,m_dat])
        fill2.set_xy(np.c_[a,f_dat])
        return l1,l2,fill1,fill2
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=15,blit=True),'动画_3_增长型')

def chart3_emphasis():
    dims=['婚姻向往','生育意愿','亲密信任','经济独立','家庭观念']
    m=[4.2,3.8,4.0,3.5,3.6]; f=[3.5,2.8,3.8,4.0,3.2]
    N=len(dims); angles=[n/float(N)*2*pi for n in range(N)]; angles+=angles[:1]
    m+=m[:1]; f+=f[:1]
    
    fig,ax=plt.subplots(figsize=(5,4.5),facecolor=BG,subplot_kw=dict(polar=True))
    ax.set_facecolor('#2d1225')
    ax.set_title('性别差异',color=P,fontweight='bold',pad=20)
    ax.tick_params(colors=LT,labelsize=8)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(dims,color=LT,fontsize=9); ax.set_ylim(0,5)
    l1,=ax.plot(angles,m,'o-',color=P,linewidth=2.5,label='男生')
    l2,=ax.plot(angles,f,'o-',color=BL,linewidth=2.5,label='女生')
    ax.fill(angles,m,alpha=0.1,color=P); ax.fill(angles,f,alpha=0.1,color=BL)
    ax.legend(loc='upper right',labelcolor=[P,BL],fontsize=9)
    dots=ax.scatter([],[],s=120,color=DP,edgecolors='white',zorder=5)
    
    def update(fr):
        idx=int(fr/8)%N
        x=[angles[idx]]; y=[m[idx]]
        dots.set_offsets(np.c_[x,y])
        return dots,
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=40,blit=True),'动画_3_强调型')

# ─── Chart 4: 影响来源气泡 ───
def chart4_growth():
    labels=['父母/家庭','同辈/朋友','个人经历','网络/社媒','书籍/影视']
    vals=[40,25,20,10,5]; colors=[P, MU, G, BL, GN]
    fig,ax=plt.subplots(figsize=(6,4),facecolor=BG); setup(ax,'影响来源排序')
    ax.set_xlim(0,50); ax.set_ylim(-0.5,4.5); ax.set_yticks(range(5)); ax.set_yticklabels(labels,color=LT,fontsize=9)
    ax.set_xlabel('提及比例 (%)',color=LT)
    
    bubbles=[]
    for i,(v,c) in enumerate(zip(vals,colors)):
        b=ax.scatter([],[],s=[],color=c,alpha=0.8,edgecolors='white',zorder=3)
        bubbles.append(b)
    
    def update(f):
        frac=min(f/12,1)
        n=max(1,int(frac*len(vals)))
        for i,(v,c) in enumerate(zip(vals,colors)):
            if i<n:
                size=(v*20)**2
                bubbles[i].set_offsets(np.c_[[v],[i]])
                bubbles[i].set_sizes([size])
            else:
                bubbles[i].set_offsets(np.c_[[0],[i]])
                bubbles[i].set_sizes([0])
        return bubbles
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=15,blit=True),'动画_4_增长型')

def chart4_emphasis():
    labels=['父母/家庭','同辈/朋友','个人经历','网络/社媒','书籍/影视']
    vals=[40,25,20,10,5]; colors=[P, MU, G, BL, GN]
    fig,ax=plt.subplots(figsize=(6,4),facecolor=BG); setup(ax,'影响来源排序')
    ax.set_xlim(0,50); ax.set_ylim(-0.5,4.5)
    ax.set_yticks(range(5)); ax.set_yticklabels(labels,color=LT,fontsize=9)
    ax.set_xlabel('提及比例 (%)',color=LT)
    
    bubbles=[]
    for v,c in zip(vals,colors):
        b=ax.scatter([v],[0],s=[(v*20)**2],color=c,alpha=0.4,edgecolors='white',zorder=3)
        bubbles.append(b)
    
    def update(f):
        idx=int(f/8)%len(vals)
        for i,b in enumerate(bubbles):
            b.set_alpha(0.9 if i==idx else 0.25)
            b.set_sizes([(vals[i]*20)**2 * (1.15 if i==idx else 1)])
        return bubbles
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=40,blit=True),'动画_4_强调型')

# ─── Chart 5: 父母婚姻质量影响 ───
def chart5_growth():
    cats=['稳定和谐','离异/矛盾']; colors=[GN, DP]
    val1=[62,28]; val2=[18,45]
    fig,ax=plt.subplots(figsize=(5,4),facecolor=BG); setup(ax,'父母婚姻质量影响')
    x=np.arange(len(cats)); w=0.3
    r1=ax.bar(x-w/2,[0,0],w,color=colors,edgecolor='white',label='向往婚姻')
    r2=ax.bar(x+w/2,[0,0],w,color=[c+'66' for c in colors],edgecolor='white',label='不婚不育倾向')
    ax.set_xticks(x); ax.set_xticklabels(cats,color=LT,fontsize=9)
    ax.set_ylabel('比例 (%)',color=LT); ax.set_ylim(0,75)
    ax.legend(labelcolor=[P,LT],fontsize=8)
    
    def update(f):
        frac=min(f/12,1)
        for r,v in zip(r1,val1): r.set_height(v*frac)
        for r,v in zip(r2,val2): r.set_height(v*frac)
        return r1+r2
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=15,blit=True),'动画_5_增长型')

def chart5_emphasis():
    cats=['稳定和谐','离异/矛盾']; colors=[GN, DP]
    val1=[62,28]; val2=[18,45]
    fig,ax=plt.subplots(figsize=(5,4),facecolor=BG); setup(ax,'父母婚姻质量影响')
    x=np.arange(len(cats)); w=0.3
    r1=ax.bar(x-w/2,val1,w,color=[c+'44' for c in colors],edgecolor='white',label='向往婚姻')
    r2=ax.bar(x+w/2,val2,w,color=[c+'44' for c in colors],edgecolor='white',label='不婚不育倾向')
    ax.set_xticks(x); ax.set_xticklabels(cats,color=LT,fontsize=9)
    ax.set_ylabel('比例 (%)',color=LT); ax.set_ylim(0,75)
    ax.legend(labelcolor=[P,LT],fontsize=8)
    
    def update(f):
        idx=int(f/8)%len(cats)
        for i,(rr1,rr2) in enumerate(zip(r1,r2)):
            fc1=colors[i] if i==idx else colors[i]+'44'
            fc2=colors[i] if i==idx else colors[i]+'44'
            rr1.set_facecolor(fc1); rr2.set_facecolor(fc2)
            rr1.set_linewidth(4 if i==idx else 2)
            rr2.set_linewidth(4 if i==idx else 2)
        return r1+r2
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=24,blit=True),'动画_5_强调型')

# ─── Chart 6: 生育顾虑瀑布 ───
def chart6_growth():
    labels=['经济压力\n53%','个人发展\n46%','时间精力\n42%','身体伤害\n37%','责任失衡\n31%']
    vals=[53,46,42,37,31]; colors=[P, MU, G, BL, GN]
    fig,ax=plt.subplots(figsize=(5.5,4),facecolor=BG); setup(ax,'大学生生育顾虑')
    x=np.arange(len(vals))
    rects=ax.bar(x,[0]*len(vals),color=colors,width=0.6,edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(labels,color=LT,fontsize=8); ax.set_ylim(0,65)
    ax.set_ylabel('提及比例 (%)',color=LT)
    
    def update(f):
        frac=min(f/12,1)
        for r,v in zip(rects,vals):
            r.set_height(v*frac)
        return rects
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=15,blit=True),'动画_6_增长型')

def chart6_emphasis():
    labels=['经济压力\n53%','个人发展\n46%','时间精力\n42%','身体伤害\n37%','责任失衡\n31%']
    vals=[53,46,42,37,31]; colors=[P, MU, G, BL, GN]
    fig,ax=plt.subplots(figsize=(5.5,4),facecolor=BG); setup(ax,'大学生生育顾虑')
    x=np.arange(len(vals))
    rects=ax.bar(x,vals,color=[c+'44' for c in colors],width=0.6,edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(labels,color=LT,fontsize=8); ax.set_ylim(0,65)
    ax.set_ylabel('提及比例 (%)',color=LT)
    
    def update(f):
        idx=int(f/8)%len(vals)
        for i,r in enumerate(rects):
            r.set_facecolor(colors[i] if i==idx else colors[i]+'44')
            r.set_linewidth(4 if i==idx else 2)
        return rects
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=40,blit=True),'动画_6_强调型')

# ─── Chart 7: 网络影响真实数据 ───
def chart7_growth():
    parts=['接触内容\n83%','自报影响\n73%','改变看法\n7%']; vals=[83,73,7]; colors=[P, MU, G]
    fig,ax=plt.subplots(figsize=(5,4),facecolor=BG); setup(ax,'网络影响真实数据')
    x=np.arange(3); rects=ax.bar(x,[0,0,0],color=colors,width=0.5,edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(parts,color=LT,fontsize=9); ax.set_ylim(0,95)
    ax.set_ylabel('比例 (%)',color=LT)
    
    def update(f):
        frac=min(f/12,1)
        for r,v in zip(rects,vals):
            r.set_height(v*frac)
        return rects
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=15,blit=True),'动画_7_增长型')

def chart7_emphasis():
    parts=['接触内容\n83%','自报影响\n73%','改变看法\n7%']; vals=[83,73,7]; colors=[P, MU, G]
    fig,ax=plt.subplots(figsize=(5,4),facecolor=BG); setup(ax,'网络影响真实数据')
    x=np.arange(3)
    rects=ax.bar(x,vals,color=[c+'44' for c in colors],width=0.5,edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(parts,color=LT,fontsize=9); ax.set_ylim(0,95)
    ax.set_ylabel('比例 (%)',color=LT)
    
    def update(f):
        idx=int(f/8)%len(vals)
        for i,r in enumerate(rects):
            r.set_facecolor(colors[i] if i==idx else colors[i]+'44')
            r.set_linewidth(4 if i==idx else 2)
        return rects
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=24,blit=True),'动画_7_强调型')

# ─── Chart 8: 年级与生源地 ───
def chart8_growth():
    grades=['大一','大二','大三+']; vals_g=[52,45,35]
    areas=['一线','新一线','三四线','县城','农村']; vals_a=[79,68,60,58,55]
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(7,3.5),facecolor=BG)
    setup(ax1,'年级差异'); setup(ax2,'生源地差异')
    x1=np.arange(3); x2=np.arange(5)
    colors_g=[P, MU, G]; colors_a=[P, MU, G, BL, GN]
    
    r1=ax1.bar(x1,[0,0,0],color=colors_g,width=0.5,edgecolor='white')
    r2=ax2.bar(x2,[0,0,0,0,0],color=colors_a,width=0.5,edgecolor='white')
    ax1.set_xticks(x1); ax1.set_xticklabels(grades,color=LT,fontsize=8)
    ax2.set_xticks(x2); ax2.set_xticklabels(areas,color=LT,fontsize=7,rotation=20)
    for ax in (ax1,ax2): ax.set_ylim(0,90), ax.set_ylabel('向往婚姻 (%)',color=LT)
    
    def update(f):
        frac=min(f/12,1)
        for r,v in zip(r1,vals_g): r.set_height(v*frac)
        for r,v in zip(r2,vals_a): r.set_height(v*frac)
        return r1+r2
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=15,blit=True),'动画_8_增长型')

def chart8_emphasis():
    grades=['大一','大二','大三+']; vals_g=[52,45,35]
    areas=['一线','新一线','三四线','县城','农村']; vals_a=[79,68,60,58,55]
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(7,3.5),facecolor=BG)
    setup(ax1,'年级差异'); setup(ax2,'生源地差异')
    x1=np.arange(3); x2=np.arange(5)
    colors_g=[P, MU, G]; colors_a=[P, MU, G, BL, GN]
    
    r1=ax1.bar(x1,vals_g,color=[c+'44' for c in colors_g],width=0.5,edgecolor='white')
    r2=ax2.bar(x2,vals_a,color=[c+'44' for c in colors_a],width=0.5,edgecolor='white')
    ax1.set_xticks(x1); ax1.set_xticklabels(grades,color=LT,fontsize=8)
    ax2.set_xticks(x2); ax2.set_xticklabels(areas,color=LT,fontsize=7,rotation=20)
    for ax in (ax1,ax2): ax.set_ylim(0,90), ax.set_ylabel('向往婚姻 (%)',color=LT)
    
    def update(f):
        idx=int(f/8)%len(vals_g)
        for i,r in enumerate(r1):
            r.set_facecolor(colors_g[i] if i==idx else colors_g[i]+'44')
            r.set_linewidth(4 if i==idx else 2)
        idx2=int(f/8)%len(vals_a)
        for i,r in enumerate(r2):
            r.set_facecolor(colors_a[i] if i==idx2 else colors_a[i]+'44')
            r.set_linewidth(4 if i==idx2 else 2)
        return r1+r2
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=40,blit=True),'动画_8_强调型')

# ─── Chart 9: 回归森林图 ───
def chart9_growth():
    factors=['性别(男=1)','网络影响','学业压力']; beta=[0.32,-0.24,-0.19]
    ci_low=[0.13,-0.38,-0.33]; ci_high=[0.51,-0.10,-0.05]; cols=[P, BL, G]
    
    fig,ax=plt.subplots(figsize=(5.5,4),facecolor=BG); setup(ax,'回归模型 (R²=0.23)')
    y=np.arange(len(factors))
    
    ax.axvline(0,color='white',linewidth=0.8,linestyle='-',alpha=0.3)
    dots=ax.scatter([0]*3,y,s=[80]*3,color=[c+'00' for c in cols],edgecolors='white',zorder=5)
    lines=[]
    for i in range(3):
        l=ax.plot([0,0],[y[i],y[i]],color=cols[i]+'00',linewidth=3,zorder=4)[0]
        lines.append(l)
    
    ax.set_yticks(y); ax.set_yticklabels(factors,color=LT,fontsize=9)
    ax.set_xlim(-0.5,0.65); ax.set_xlabel('标准化系数 β',color=LT)
    ax.axvline(0,color='white',linewidth=0.8,linestyle='-',alpha=0.3)
    
    def update(f):
        frac=min(f/12,1)
        n=max(1,int(frac*3))
        xs=[beta[i] for i in range(n)]
        ys=[y[i] for i in range(n)]
        dots.set_offsets(np.c_[xs,ys])
        for i in range(3):
            if i<n:
                lines[i].set_data([ci_low[i],ci_high[i]],[y[i],y[i]])
            else:
                lines[i].set_data([],[])
        return [dots]+lines
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=15,blit=True),'动画_9_增长型')

def chart9_emphasis():
    factors=['性别(男=1)','网络影响','学业压力']; beta=[0.32,-0.24,-0.19]
    ci_low=[0.13,-0.38,-0.33]; ci_high=[0.51,-0.10,-0.05]; cols=[P, BL, G]
    
    fig,ax=plt.subplots(figsize=(5.5,4),facecolor=BG); setup(ax,'回归模型 (R²=0.23)')
    y=np.arange(len(factors))
    ax.axvline(0,color='white',linewidth=0.8,linestyle='-',alpha=0.3)
    
    dots=ax.scatter(beta,y,s=80,color=[c+'44' for c in cols],edgecolors='white',zorder=5)
    lines=[]
    for i in range(3):
        l=ax.plot([ci_low[i],ci_high[i]],[y[i],y[i]],color=cols[i]+'44',linewidth=3,zorder=4)[0]
        lines.append(l)
    
    ax.set_yticks(y); ax.set_yticklabels(factors,color=LT,fontsize=9)
    ax.set_xlim(-0.5,0.65); ax.set_xlabel('标准化系数 β',color=LT)
    
    def update(f):
        idx=int(f/8)%len(beta)
        dots.set_color(cols[idx])
        dots.set_alpha(1)
        dots.set_offsets(np.c_[[beta[idx]],[y[idx]]])
        return dots,
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=24,blit=True),'动画_9_强调型')

# ─── Chart 10: 金句引用 ───
def chart10_growth():
    lines_t = [
        '"我们有资格追寻自己期望的',
        '恋爱、婚姻与生育经历。"',
        '',
        '——这不是爱的消失，',
        '   而是爱的理性化。'
    ]
    fig,ax=plt.subplots(figsize=(6,3),facecolor=BG)
    ax.set_facecolor(BG); ax.axis('off')
    txt=ax.text(0.5,0.5,'',color=LT,fontsize=15,
        ha='center',va='center',fontweight='bold',linespacing=1.8)
    
    def update(f):
        n=max(1,int(f/4))
        t='\n'.join(lines_t[:n])
        txt.set_text(t)
        return txt,
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=24,blit=True),'动画_10_增长型')

def chart10_emphasis():
    fig,ax=plt.subplots(figsize=(6,3),facecolor=BG)
    ax.set_facecolor(BG); ax.axis('off')
    full = '"我们有资格追寻自己期望的\n恋爱、婚姻与生育经历。"\n\n——这不是爱的消失，\n   而是爱的理性化。'
    txt=ax.text(0.5,0.5,full,color=LT,fontsize=15,
        ha='center',va='center',fontweight='bold',linespacing=1.8)
    
    # flash each line
    lines=full.split('\n')
    
    def update(f):
        idx=int(f/8)%len(lines)
        colored=[]
        for i,l in enumerate(lines):
            if i==idx:
                colored.append(f'<color={P}>{l}</color>')
            elif i==idx-1 or (idx==0 and i==len(lines)-1):
                colored.append(f'<color={G}>{l}</color>')
            else:
                colored.append(l)
        txt.set_text('\n'.join(colored))
        return txt,
    return save_gif(fig, animation.FuncAnimation(fig,update,frames=32,blit=True),'动画_10_强调型')

# ═══ Run all ═══
if __name__=='__main__':
    funcs = [
        chart1_growth, chart1_emphasis,
        chart2_growth, chart2_emphasis,
        chart3_growth, chart3_emphasis,
        chart4_growth, chart4_emphasis,
        chart5_growth, chart5_emphasis,
        chart6_growth, chart6_emphasis,
        chart7_growth, chart7_emphasis,
        chart8_growth, chart8_emphasis,
        chart9_growth, chart9_emphasis,
        chart10_growth, chart10_emphasis,
    ]
    for fn in funcs:
        try:
            p = fn()
            print(f'OK  {os.path.basename(p)}')
        except Exception as e:
            print(f'ERR {fn.__name__}: {e}')
    print('Done!')
