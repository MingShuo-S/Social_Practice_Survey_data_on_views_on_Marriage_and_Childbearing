"""Improved growth-type animations with higher FPS and easing."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Wedge
import numpy as np
from math import pi
import os, warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DengXian']
plt.rcParams['axes.unicode_minus'] = False

OUT = r'C:\Users\29548\Desktop\阳关\南京大学\社会实践\思修\可视化'

# Colors
P = '#FF6B9D'; DP = '#C2185B'; BG = '#1a0a14'; LT = '#fce4ec'
MU = '#AD8A9E'; G = '#FFAB91'; GN = '#4CAF50'; BL = '#42A5F5'

def setup(ax, t=''):
    ax.set_facecolor('#2d1225')
    ax.set_title(t, color=P, fontsize=14, fontweight='bold', pad=12)
    ax.tick_params(colors=LT, labelsize=9)
    for s in ax.spines.values(): s.set_color('#4a2a3a')

def ease(t):
    """Smoothstep ease-in-out"""
    return t * t * (3 - 2 * t)

FPS = 10
DUR = 2.5  # seconds per anim
FRAMES = int(FPS * DUR)

def save_gif(fig, anim, name, fps=FPS):
    p = os.path.join(OUT, f'{name}.gif')
    anim.save(p, writer=animation.PillowWriter(fps=fps), dpi=120)
    plt.close(fig)
    return p

# ─── Chart 1: 婚姻态度分布 (Donut) ───
def chart1_growth():
    labels = ['向往\n48%','顺其自然\n35%','不明确\n7%','其他\n10%']
    sizes = [48, 35, 7, 10]; colors = [P, MU, G, BL]
    total = sum(sizes)
    fig, ax = plt.subplots(figsize=(5,4), facecolor=BG)
    setup(ax, '婚姻态度分布')

    # Build wedges manually as Wedge patches with width for donut ring
    ring_wedges = []
    start = 0
    for s, c in zip(sizes, colors):
        end = start + s / total * 360
        w = Wedge((0,0), 1, start, start, width=0.45, facecolor=c,
                  edgecolor='white', linewidth=2)
        ax.add_patch(w)
        ring_wedges.append((w, start, end, c))
        start = end

    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal'); ax.axis('off')

    # Labels
    txts = []
    start = 0
    for l, s, c in zip(labels, sizes, colors):
        mid_deg = start + s / total * 180
        mid_rad = mid_deg * pi / 180
        cx = 1.35 * np.cos(mid_rad)
        cy = 1.35 * np.sin(mid_rad)
        t = ax.text(cx, cy, '', color=LT, fontsize=9, ha='center', va='center', fontweight='bold')
        txts.append((t, start + s / total * 360))
        start += s / total * 360

    n = len(ring_wedges)

    def update(f):
        progress = min(f / (FRAMES - 1), 1)
        ep = ease(progress)
        for i, (w, s_deg, e_deg, c) in enumerate(ring_wedges):
            seg_start_t = i / n
            seg_time = 1 / n
            local_p = max(0, min(1, (ep - seg_start_t) / seg_time))
            if local_p > 0:
                lep = ease(min(local_p, 1))
                w.theta1 = s_deg
                w.theta2 = s_deg + (e_deg - s_deg) * lep
                w.set_visible(True)
            else:
                w.set_visible(False)
        for i, (t, _) in enumerate(txts):
            seg_end = (i + 1) / n
            t.set_alpha(max(0, min(1, (ep - seg_end + 0.1) * 10)))
        return [w for w, _, _, _ in ring_wedges] + [t for t, _ in txts]

    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_1_增长型')

# ─── Chart 2-9: 增长型 (bars/lines with easing) ───
def chart2_growth():
    cats = ['婚恋积极','生育积极']; vals = [3.72, 3.15]; bars = [GN, P]
    fig, ax = plt.subplots(figsize=(5,4), facecolor=BG)
    setup(ax, '婚恋 vs 生育态度 [p<0.001]')
    ax.set_ylim(0,4.5); ax.set_ylabel('均值', color=LT)
    rects = ax.bar(cats, [0,0], color=bars, width=0.5, edgecolor='white')

    def update(f):
        ep = ease(min(f / (FRAMES - 1), 1))
        for r, v in zip(rects, vals):
            r.set_height(v * ep)
        return rects
    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_2_增长型')

def chart3_growth():
    dims = ['婚姻向往','生育意愿','亲密信任','经济独立','家庭观念']
    m = [4.2, 3.8, 4.0, 3.5, 3.6]; f = [3.5, 2.8, 3.8, 4.0, 3.2]
    N = len(dims); angles = [n/float(N)*2*pi for n in range(N)]; angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5,4.5), facecolor=BG, subplot_kw=dict(polar=True))
    ax.set_facecolor('#2d1225'); ax.set_title('性别差异雷达', color=P, fontweight='bold', pad=20)
    ax.tick_params(colors=LT, labelsize=8)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(dims, color=LT, fontsize=9)
    ax.set_ylim(0,5)

    fill1 = ax.fill(angles[:1], [0], alpha=0.1, color=P)[0]
    fill2 = ax.fill(angles[:1], [0], alpha=0.1, color=BL)[0]
    l1, = ax.plot([], [], 'o-', color=P, linewidth=2.5, label='男生')
    l2, = ax.plot([], [], 'o-', color=BL, linewidth=2.5, label='女生')
    ax.legend(loc='upper right', labelcolor=[P, BL], fontsize=9)

    m_full = m + m[:1]; f_full = f + f[:1]

    def update(fr):
        ep = ease(min(fr / (FRAMES - 1), 1))
        n = max(1, int(ep * N))
        m_dat = m_full[:n+1]; f_dat = f_full[:n+1]
        a = angles[:n+1]
        l1.set_data(a, m_dat); l2.set_data(a, f_dat)
        fill1.set_xy(np.c_[a, m_dat])
        fill2.set_xy(np.c_[a, f_dat])
        return l1, l2, fill1, fill2
    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_3_增长型')

def chart4_growth():
    labels = ['父母/家庭','同辈/朋友','个人经历','网络/社媒','书籍/影视']
    vals = [40,25,20,10,5]; colors = [P, MU, G, BL, GN]
    fig, ax = plt.subplots(figsize=(6,4), facecolor=BG); setup(ax, '影响来源排序')
    ax.set_xlim(0,50); ax.set_ylim(-0.5,4.5)
    ax.set_yticks(range(5)); ax.set_yticklabels(labels, color=LT, fontsize=9)
    ax.set_xlabel('提及比例 (%)', color=LT)

    bubbles = []
    for i, (v, c) in enumerate(zip(vals, colors)):
        b = ax.scatter([0], [i], s=[0], color=c, alpha=0.85, edgecolors='white', linewidth=1.5, zorder=3)
        bubbles.append(b)

    def update(f):
        ep = ease(min(f / (FRAMES - 1), 1))
        n = len(vals)
        for i, (v, b) in enumerate(zip(vals, bubbles)):
            local_p = max(0, min(1, (ep * n - i)))
            lep = ease(local_p) if local_p < 1 else 1
            cx = v * lep
            sz = (cx * 1.2) ** 2
            b.set_offsets(np.c_[[cx], [i]])
            b.set_sizes([sz])
        return bubbles
    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_4_增长型')

def chart5_growth():
    cats = ['稳定和谐','离异/矛盾']; colors = [GN, DP]
    val1 = [62,28]; val2 = [18,45]
    fig, ax = plt.subplots(figsize=(5,4), facecolor=BG); setup(ax, '父母婚姻质量影响 [χ²=15.3, p<0.001]')
    x = np.arange(len(cats)); w = 0.3
    r1 = ax.bar(x-w/2, [0,0], w, color=colors, edgecolor='white', label='向往婚姻')
    r2 = ax.bar(x+w/2, [0,0], w, color=[c+'88' for c in colors], edgecolor='white', label='不婚不育倾向')
    ax.set_xticks(x); ax.set_xticklabels(cats, color=LT, fontsize=9)
    ax.set_ylabel('比例 (%)', color=LT); ax.set_ylim(0,75)
    ax.legend(labelcolor=[P, LT], fontsize=8)

    def update(f):
        ep = ease(min(f / (FRAMES - 1), 1))
        for r, v in zip(r1, val1): r.set_height(v * ep)
        for r, v in zip(r2, val2): r.set_height(v * ep)
        return list(r1) + list(r2)
    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_5_增长型')

def chart6_growth():
    labels = ['经济压力\n53%','个人发展\n46%','时间精力\n42%','身体伤害\n37%','责任失衡\n31%']
    vals = [53,46,42,37,31]; colors = [P, MU, G, BL, GN]
    fig, ax = plt.subplots(figsize=(5.5,4), facecolor=BG); setup(ax, '大学生生育顾虑')
    x = np.arange(len(vals))
    rects = ax.bar(x, [0]*len(vals), color=colors, width=0.6, edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(labels, color=LT, fontsize=8); ax.set_ylim(0,65)
    ax.set_ylabel('提及比例 (%)', color=LT)

    def update(f):
        ep = ease(min(f / (FRAMES - 1), 1))
        for r, v in zip(rects, vals):
            r.set_height(v * ep)
        return rects
    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_6_增长型')

def chart7_growth():
    parts = ['接触内容\n83%','自报影响\n73%','改变看法\n7%']; vals = [83,73,7]; colors = [P, MU, G]
    fig, ax = plt.subplots(figsize=(5,4), facecolor=BG); setup(ax, '网络影响真实数据')
    x = np.arange(3); rects = ax.bar(x, [0,0,0], color=colors, width=0.5, edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(parts, color=LT, fontsize=9); ax.set_ylim(0,95)
    ax.set_ylabel('比例 (%)', color=LT)

    def update(f):
        ep = ease(min(f / (FRAMES - 1), 1))
        for r, v in zip(rects, vals):
            r.set_height(v * ep)
        return rects
    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_7_增长型')

def chart8_growth():
    grades = ['大一','大二','大三+']; vals_g = [52,45,35]
    areas = ['一线','新一线','三四线','县城','农村']; vals_a = [79,68,60,58,55]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7,3.5), facecolor=BG)
    setup(ax1, '年级差异 [χ²=6.2, p=0.045]'); setup(ax2, '生源地差异 [χ²=8.7, p=0.013]')
    x1 = np.arange(3); x2 = np.arange(5)
    colors_g = [P, MU, G]; colors_a = [P, MU, G, BL, GN]
    r1 = ax1.bar(x1, [0,0,0], color=colors_g, width=0.5, edgecolor='white')
    r2 = ax2.bar(x2, [0,0,0,0,0], color=colors_a, width=0.5, edgecolor='white')
    ax1.set_xticks(x1); ax1.set_xticklabels(grades, color=LT, fontsize=8)
    ax2.set_xticks(x2); ax2.set_xticklabels(areas, color=LT, fontsize=7, rotation=20)
    for ax in (ax1, ax2): ax.set_ylim(0,90); ax.set_ylabel('向往婚姻 (%)', color=LT)

    def update(f):
        ep = ease(min(f / (FRAMES - 1), 1))
        for r, v in zip(r1, vals_g): r.set_height(v * ep)
        for r, v in zip(r2, vals_a): r.set_height(v * ep)
        return list(r1) + list(r2)
    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_8_增长型')

def chart9_growth():
    factors = ['性别(男=1)','网络影响','学业压力']; beta = [0.32,-0.24,-0.19]
    ci_low = [0.13,-0.38,-0.33]; ci_high = [0.51,-0.10,-0.05]; cols = [P, BL, G]
    fig, ax = plt.subplots(figsize=(5.5,4), facecolor=BG); setup(ax, '回归模型 [R²=0.23, p<0.001]')
    y = np.arange(len(factors))
    ax.axvline(0, color='white', linewidth=0.8, linestyle='-', alpha=0.3)
    ax.set_yticks(y); ax.set_yticklabels(factors, color=LT, fontsize=9)
    ax.set_xlim(-0.5,0.65); ax.set_xlabel('标准化系数 β', color=LT)

    dots = ax.scatter([0]*3, y, s=90, color=[c+'00' for c in cols], edgecolors='white', zorder=5)
    lines = []
    for i in range(3):
        l, = ax.plot([0,0], [y[i],y[i]], color=cols[i], linewidth=3, zorder=4)
        lines.append(l)

    def update(f):
        ep = ease(min(f / (FRAMES - 1), 1))
        n = max(1, int(ep * 3))
        xs = [beta[i] for i in range(min(n, 3))]
        ys_ = [y[i] for i in range(min(n, 3))]
        dots.set_offsets(np.c_[xs, ys_])
        dots.set_color([c for c,_ in zip(cols, range(n))])
        for i in range(3):
            if i < n:
                lines[i].set_data([ci_low[i], ci_high[i]], [y[i], y[i]])
                lines[i].set_alpha(1)
            else:
                lines[i].set_data([], [])
        return [dots] + lines
    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_9_增长型')

def chart10_growth():
    lines_t = [
        '"我们有资格追寻自己期望的',
        '恋爱、婚姻与生育经历。"',
        '',
        '——这不是爱的消失，',
        '   而是爱的理性化。'
    ]
    fig, ax = plt.subplots(figsize=(6,3), facecolor=BG)
    ax.set_facecolor(BG); ax.axis('off')
    txt = ax.text(0.5, 0.5, '', color=LT, fontsize=16,
                  ha='center', va='center', fontweight='bold', linespacing=1.8)

    def update(f):
        ep = ease(min(f / (FRAMES - 1), 1))
        n = max(1, int(ep * len(lines_t)))
        txt.set_text('\n'.join(lines_t[:n]))
        txt.set_alpha(min(1, ep * 1.5))
        return txt,
    return save_gif(fig, animation.FuncAnimation(fig, update, frames=FRAMES, blit=True),
                    '动画_10_增长型')

if __name__ == '__main__':
    funcs = [
        chart1_growth, chart2_growth, chart3_growth, chart4_growth,
        chart5_growth, chart6_growth, chart7_growth, chart8_growth,
        chart9_growth, chart10_growth
    ]
    for fn in funcs:
        try:
            p = fn()
            print(f'OK  {os.path.basename(p)}')
        except Exception as e:
            print(f'ERR {fn.__name__}: {e}')
    print('Done!')
