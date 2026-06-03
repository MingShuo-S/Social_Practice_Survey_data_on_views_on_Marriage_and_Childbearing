"""Growth-type GIFs: per-frame rendering + PIL assembly for reliability."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
from math import pi
from PIL import Image
import os, warnings, io
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DengXian']
plt.rcParams['axes.unicode_minus'] = False

OUT = r'C:\Users\29548\Desktop\阳关\南京大学\社会实践\思修\可视化'

# Colors
P = '#FF6B9D'; DP = '#C2185B'; BG = '#1a0a14'; LT = '#fce4ec'
MU = '#AD8A9E'; G = '#FFAB91'; GN = '#4CAF50'; BL = '#42A5F5'

FPS = 16
ANIM_SEC = 2.5
HOLD_SEC = 4.5
ANIM_FRAMES = int(FPS * ANIM_SEC)
HOLD_FRAMES = int(FPS * HOLD_SEC)
TOTAL_FRAMES = ANIM_FRAMES + HOLD_FRAMES

def ease(t):
    return t * t * (3 - 2 * t)

def setup(ax, t=''):
    ax.set_facecolor('#2d1225')
    ax.set_title(t, color=P, fontsize=14, fontweight='bold', pad=12)
    ax.tick_params(colors=LT, labelsize=9)
    for s in ax.spines.values(): s.set_color('#4a2a3a')

def make_gif(frames, name, fps=FPS):
    """frames: list of PIL Images."""
    path = os.path.join(OUT, f'{name}.gif')
    dur = int(1000 / fps)
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=dur, loop=0, optimize=False)
    return path

def fig_to_pil(fig, dpi=100):
    """Render matplotlib figure to PIL Image (in-memory)."""
    buf = io.BytesIO()
    fig.savefig(buf, dpi=dpi, bbox_inches='tight', pad_inches=0.1,
                facecolor=fig.get_facecolor(), format='png')
    buf.seek(0)
    return Image.open(buf).convert('RGBA')

# ─── Chart 1: 婚姻态度分布 (Donut sweep) ───
def chart1_growth():
    labels = ['向往\n48%','顺其自然\n35%','不明确\n7%','其他\n10%']
    sizes = [48, 35, 7, 10]; colors = [P, MU, G, BL]
    total = sum(sizes)
    N = len(sizes)

    # Precompute segment angles
    seg_angles = []
    start = 0
    for s in sizes:
        end = start + s / total * 360
        seg_angles.append((start, end))
        start = end

    frames = []
    for f in range(TOTAL_FRAMES):
        fig, ax = plt.subplots(figsize=(5,4), facecolor=BG)
        setup(ax, '婚姻态度分布')
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6)
        ax.set_aspect('equal'); ax.axis('off')

        # Determine global progress
        if f < ANIM_FRAMES:
            progress = f / max(1, ANIM_FRAMES - 1)
            ep = ease(progress)
        else:
            ep = 1.0  # hold at final state

        # Draw each segment
        for i, ((s, e), c) in enumerate(zip(seg_angles, colors)):
            seg_start_t = i / N
            seg_time = 1 / N
            local_p = max(0, min(1, (ep - seg_start_t) / seg_time))
            if local_p > 0:
                lep = ease(min(local_p, 1))
                current_end = s + (e - s) * lep
                w = Wedge((0,0), 1, s, current_end, width=0.45,
                          facecolor=c, edgecolor='white', linewidth=2)
                ax.add_patch(w)

        # Center hole
        centre = plt.Circle((0,0), 0.55, fc=BG)
        ax.add_patch(centre)

        # Labels with fade-in
        for i, ((s, e), l) in enumerate(zip(seg_angles, labels)):
            seg_end_t = (i + 1) / N
            label_alpha = max(0, min(1, (ep - seg_end_t + 0.15) * 8))
            if label_alpha > 0.01:
                mid_deg = (s + e) / 2
                mid_rad = mid_deg * pi / 180
                cx = 1.35 * np.cos(mid_rad)
                cy = 1.35 * np.sin(mid_rad)
                ax.text(cx, cy, l, color=LT, fontsize=9, ha='center',
                        va='center', fontweight='bold', alpha=label_alpha)

        frames.append(fig_to_pil(fig))
        plt.close(fig)

    return make_gif(frames, '动画_1_增长型')

# ─── Chart 2: 生育态度与对比 (Bar growth) ───
def chart2_growth():
    cats = ['婚恋积极','生育积极']; vals = [3.72, 3.15]; bar_colors = [GN, P]
    frames = []
    for f in range(TOTAL_FRAMES):
        fig, ax = plt.subplots(figsize=(5,4), facecolor=BG)
        setup(ax, '婚恋 vs 生育态度 [p<0.001]')
        ax.set_ylim(0,4.5); ax.set_ylabel('均值', color=LT)

        ep = ease(min(f / max(1, ANIM_FRAMES - 1), 1)) if f < ANIM_FRAMES else 1
        heights = [v * ep for v in vals]
        ax.bar(cats, heights, color=bar_colors, width=0.5, edgecolor='white')

        # Value labels on bars
        for i, (h, v) in enumerate(zip(heights, vals)):
            if h > 0.1:
                ax.text(i, h + 0.08, f'{v:.2f}', color=LT, fontsize=10,
                        ha='center', fontweight='bold')

        frames.append(fig_to_pil(fig))
        plt.close(fig)
    return make_gif(frames, '动画_2_增长型')

# ─── Chart 3: 性别差异雷达 ───
def chart3_growth():
    dims = ['婚姻向往','生育意愿','亲密信任','经济独立','家庭观念']
    m = [4.2, 3.8, 4.0, 3.5, 3.6]; f = [3.5, 2.8, 3.8, 4.0, 3.2]
    N = len(dims); angles = [n/float(N)*2*pi for n in range(N)]; angles += angles[:1]
    m_closed = m + m[:1]; f_closed = f + f[:1]

    frames = []
    for fr in range(TOTAL_FRAMES):
        fig, ax = plt.subplots(figsize=(5,4.5), facecolor=BG, subplot_kw=dict(polar=True))
        ax.set_facecolor('#2d1225')
        ax.set_title('性别差异雷达', color=P, fontweight='bold', pad=20)
        ax.tick_params(colors=LT, labelsize=8)
        ax.set_xticks(angles[:-1]); ax.set_xticklabels(dims, color=LT, fontsize=9)
        ax.set_ylim(0,5)

        ep = ease(min(fr / max(1, ANIM_FRAMES - 1), 1)) if fr < ANIM_FRAMES else 1
        n_visible = max(1, int(ep * N))
        m_show = m_closed[:n_visible+1]; f_show = f_closed[:n_visible+1]
        a_show = angles[:n_visible+1]

        ax.fill(a_show, m_show, alpha=0.1, color=P)
        ax.fill(a_show, f_show, alpha=0.1, color=BL)
        ax.plot(a_show, m_show, 'o-', color=P, linewidth=2.5, label='男生')
        ax.plot(a_show, f_show, 'o-', color=BL, linewidth=2.5, label='女生')
        ax.legend(loc='upper right', labelcolor=[P, BL], fontsize=9)

        frames.append(fig_to_pil(fig))
        plt.close(fig)
    return make_gif(frames, '动画_3_增长型')

# ─── Chart 4: 影响来源气泡 ───
def chart4_growth():
    labels = ['父母/家庭','同辈/朋友','个人经历','网络/社媒','书籍/影视']
    vals = [40,25,20,10,5]; colors = [P, MU, G, BL, GN]
    N = len(vals)

    frames = []
    for f in range(TOTAL_FRAMES):
        fig, ax = plt.subplots(figsize=(6,4), facecolor=BG)
        setup(ax, '影响来源排序')
        ax.set_xlim(0,50); ax.set_ylim(-0.5,4.5)
        ax.set_yticks(range(N)); ax.set_yticklabels(labels, color=LT, fontsize=9)
        ax.set_xlabel('提及比例 (%)', color=LT)

        ep = ease(min(f / max(1, ANIM_FRAMES - 1), 1)) if f < ANIM_FRAMES else 1

        for i, (v, c, l) in enumerate(zip(vals, colors, labels)):
            seg_end = (i + 1) / N
            local_p = max(0, min(1, (ep - i / N) * N))
            lep = ease(local_p) if local_p < 1 else 1
            cx = v * lep
            sz = max(5, (cx * 1.2) ** 2)
            ax.scatter([cx], [i], s=sz, color=c, alpha=0.85,
                       edgecolors='white', linewidth=1.5, zorder=3)

        frames.append(fig_to_pil(fig))
        plt.close(fig)
    return make_gif(frames, '动画_4_增长型')

# ─── Chart 5: 父母婚姻质量影响 ───
def chart5_growth():
    cats = ['稳定和谐','离异/矛盾']; colors = [GN, DP]
    val1 = [62,28]; val2 = [18,45]
    frames = []
    for f in range(TOTAL_FRAMES):
        fig, ax = plt.subplots(figsize=(5,4), facecolor=BG)
        setup(ax, '父母婚姻质量影响 [\u03c7\u00b2=15.3, p<0.001]')
        x = np.arange(len(cats)); w = 0.3

        ep = ease(min(f / max(1, ANIM_FRAMES - 1), 1)) if f < ANIM_FRAMES else 1
        h1 = [v * ep for v in val1]
        h2 = [v * ep for v in val2]

        ax.bar(x-w/2, h1, w, color=colors, edgecolor='white', label='向往婚姻')
        ax.bar(x+w/2, h2, w, color=[c+'88' for c in colors], edgecolor='white', label='不婚不育倾向')
        ax.set_xticks(x); ax.set_xticklabels(cats, color=LT, fontsize=9)
        ax.set_ylabel('比例 (%)', color=LT); ax.set_ylim(0,75)
        ax.legend(labelcolor=[P, LT], fontsize=8)

        # Value labels
        for i, h in enumerate(h1):
            if h > 1: ax.text(i-w/2, h+1, f'{val1[i]}%', color=LT, fontsize=9, ha='center')
        for i, h in enumerate(h2):
            if h > 1: ax.text(i+w/2, h+1, f'{val2[i]}%', color=LT, fontsize=9, ha='center')

        frames.append(fig_to_pil(fig))
        plt.close(fig)
    return make_gif(frames, '动画_5_增长型')

# ─── Chart 6: 生育顾虑瀑布 ───
def chart6_growth():
    labels = ['经济压力\n53%','个人发展\n46%','时间精力\n42%','身体伤害\n37%','责任失衡\n31%']
    vals = [53,46,42,37,31]; colors = [P, MU, G, BL, GN]
    frames = []
    for f in range(TOTAL_FRAMES):
        fig, ax = plt.subplots(figsize=(5.5,4), facecolor=BG)
        setup(ax, '大学生生育顾虑')
        x = np.arange(len(vals))

        ep = ease(min(f / max(1, ANIM_FRAMES - 1), 1)) if f < ANIM_FRAMES else 1
        heights = [v * ep for v in vals]

        ax.bar(x, heights, color=colors, width=0.6, edgecolor='white')
        ax.set_xticks(x); ax.set_xticklabels(labels, color=LT, fontsize=8)
        ax.set_ylim(0,65); ax.set_ylabel('提及比例 (%)', color=LT)

        for i, h in enumerate(heights):
            if h > 1: ax.text(i, h+1, f'{vals[i]}%', color=LT, fontsize=9, ha='center')

        frames.append(fig_to_pil(fig))
        plt.close(fig)
    return make_gif(frames, '动画_6_增长型')

# ─── Chart 7: 网络影响真实数据 ───
def chart7_growth():
    parts = ['接触内容\n83%','自报影响\n73%','改变看法\n7%']; vals = [83,73,7]; colors = [P, MU, G]
    frames = []
    for f in range(TOTAL_FRAMES):
        fig, ax = plt.subplots(figsize=(5,4), facecolor=BG)
        setup(ax, '网络影响真实数据')
        x = np.arange(3)

        ep = ease(min(f / max(1, ANIM_FRAMES - 1), 1)) if f < ANIM_FRAMES else 1
        heights = [v * ep for v in vals]

        ax.bar(x, heights, color=colors, width=0.5, edgecolor='white')
        ax.set_xticks(x); ax.set_xticklabels(parts, color=LT, fontsize=9)
        ax.set_ylim(0,95); ax.set_ylabel('比例 (%)', color=LT)

        for i, h in enumerate(heights):
            if h > 1: ax.text(i, h+1, f'{vals[i]}%', color=LT, fontsize=9, ha='center')

        frames.append(fig_to_pil(fig))
        plt.close(fig)
    return make_gif(frames, '动画_7_增长型')

# ─── Chart 8: 年级与生源地 ───
def chart8_growth():
    grades = ['大一','大二','大三+']; vals_g = [52,45,35]
    areas = ['一线','新一线','三四线','县城','农村']; vals_a = [79,68,60,58,55]
    colors_g = [P, MU, G]; colors_a = [P, MU, G, BL, GN]
    frames = []
    for f in range(TOTAL_FRAMES):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7,3.5), facecolor=BG)
        setup(ax1, '年级差异 [\u03c7\u00b2=6.2, p=0.045]')
        setup(ax2, '生源地差异 [\u03c7\u00b2=8.7, p=0.013]')
        x1 = np.arange(3); x2 = np.arange(5)

        ep = ease(min(f / max(1, ANIM_FRAMES - 1), 1)) if f < ANIM_FRAMES else 1

        h1 = [v * ep for v in vals_g]; h2 = [v * ep for v in vals_a]
        ax1.bar(x1, h1, color=colors_g, width=0.5, edgecolor='white')
        ax2.bar(x2, h2, color=colors_a, width=0.5, edgecolor='white')
        ax1.set_xticks(x1); ax1.set_xticklabels(grades, color=LT, fontsize=8)
        ax2.set_xticks(x2); ax2.set_xticklabels(areas, color=LT, fontsize=7, rotation=20)
        for ax in (ax1, ax2): ax.set_ylim(0,90); ax.set_ylabel('向往婚姻 (%)', color=LT)

        frames.append(fig_to_pil(fig))
        plt.close(fig)
    return make_gif(frames, '动画_8_增长型')

# ─── Chart 9: 回归森林图 ───
def chart9_growth():
    factors = ['性别(男=1)','网络影响','学业压力']; beta = [0.32,-0.24,-0.19]
    ci_low = [0.13,-0.38,-0.33]; ci_high = [0.51,-0.10,-0.05]; cols = [P, BL, G]
    frames = []
    for f in range(TOTAL_FRAMES):
        fig, ax = plt.subplots(figsize=(5.5,4), facecolor=BG)
        setup(ax, '回归模型 [R\u00b2=0.23, p<0.001]')
        y = np.arange(len(factors))
        ax.axvline(0, color='white', linewidth=0.8, linestyle='-', alpha=0.3)
        ax.set_yticks(y); ax.set_yticklabels(factors, color=LT, fontsize=9)
        ax.set_xlim(-0.5,0.65); ax.set_xlabel('标准化系数 \u03b2', color=LT)

        ep = ease(min(f / max(1, ANIM_FRAMES - 1), 1)) if f < ANIM_FRAMES else 1
        n = max(1, int(ep * 3))

        for i in range(min(n, 3)):
            ax.plot([ci_low[i], ci_high[i]], [y[i], y[i]], color=cols[i],
                    linewidth=3, zorder=4)
            ax.scatter([beta[i]], [y[i]], s=90, color=cols[i],
                       edgecolors='white', zorder=5)

        # Annotations for beta values
        for i in range(min(n, 3)):
            ax.text(beta[i] + 0.03, y[i], f'\u03b2={beta[i]:.2f}',
                    color=cols[i], fontsize=8, va='center')

        frames.append(fig_to_pil(fig))
        plt.close(fig)
    return make_gif(frames, '动画_9_增长型')

# ─── Chart 10: 金句引用 ───
def chart10_growth():
    lines_t = [
        '"我们有资格追寻自己期望的',
        '恋爱、婚姻与生育经历。"',
        '',
        '——这不是爱的消失，',
        '   而是爱的理性化。'
    ]
    N = len(lines_t)
    frames = []
    for f in range(TOTAL_FRAMES):
        fig, ax = plt.subplots(figsize=(6,3), facecolor=BG)
        ax.set_facecolor(BG); ax.axis('off')

        ep = ease(min(f / max(1, ANIM_FRAMES - 1), 1)) if f < ANIM_FRAMES else 1
        n = max(1, int(ep * N))
        txt = '\n'.join(lines_t[:n])
        # alpha fade-in
        alpha = min(1, ep * 1.5)
        ax.text(0.5, 0.5, txt, color=LT, fontsize=16,
                ha='center', va='center', fontweight='bold',
                linespacing=1.8, alpha=alpha)

        frames.append(fig_to_pil(fig))
        plt.close(fig)
    return make_gif(frames, '动画_10_增长型')

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
