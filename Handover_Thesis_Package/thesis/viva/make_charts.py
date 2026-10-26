"""Viva charts in the deck palette (black / grey / red on white)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'stats', 'data')
OUT = os.path.join(HERE, 'charts')
BLACK, GREY, LIGHT, RED = '#1A1A1A', '#8C8C8C', '#D0D0D0', '#C00000'
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 13, 'axes.edgecolor': GREY,
                     'axes.labelcolor': BLACK, 'xtick.color': BLACK, 'ytick.color': BLACK,
                     'axes.spines.top': False, 'axes.spines.right': False})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# Questionnaire construct means and key items
fig, ax = plt.subplots(figsize=(7.5, 4.6))
labels = ['A Usefulness', 'B Ease of use', 'C Trust', 'D Replaceability concern',
          'E Skills & reskilling', 'F Oversight', 'G Organisational response']
vals = [3.58, 4.00, 3.87, 3.89, 3.75, 3.83, 3.58]
ax.barh(labels[::-1], vals[::-1], color=GREY, height=0.6)
ax.axvline(3, color=BLACK, ls='--', lw=1)
ax.text(3.02, 6.45, 'neutral = 3', color=BLACK, fontsize=11)
for y, v in enumerate(vals[::-1]):
    ax.text(v + 0.04, y, f'{v:.2f}', va='center', fontsize=12)
ax.set_xlim(1, 5)
ax.set_xlabel('Mean (1 = strongly disagree, 5 = strongly agree)')
save(fig, 'q_constructs.png')

fig, ax = plt.subplots(figsize=(6.5, 3.6))
items = ['Easy to use (11)', 'Understand what\ntool is doing (12)', 'Skills more\nimportant (24)',
         'Training adequate (23)']
iv = [4.33, 3.33, 4.00, 3.33]
cols = [GREY, RED, GREY, RED]
ax.bar(items, iv, color=cols, width=0.6)
ax.axhline(3, color=BLACK, ls='--', lw=1)
for x, v in enumerate(iv):
    ax.text(x, v + 0.06, f'{v:.2f}', ha='center', fontsize=13, fontweight='bold',
            color=RED if cols[x] == RED else BLACK)
ax.set_ylim(1, 5)
ax.tick_params(axis='x', labelsize=11)
save(fig, 'q_gaps.png')

# D1 EU adoption
fig, ax = plt.subplots(figsize=(6.5, 4))
yrs = [2021, 2023, 2024, 2025]
ax.plot(yrs, [27.5, 30.2, 41.2, 53.6], color=RED, lw=3, marker='o', label='250+ employees')
ax.plot(yrs, [7.7, 8.2, 14.3, 20.7], color=GREY, lw=3, marker='o', label='10+ employees')
for x, y in ((2021, 27.5), (2025, 53.6)):
    ax.text(x, y + 2.5, f'{y}%', ha='center', color=RED, fontsize=14, fontweight='bold')
ax.set_xticks(yrs)
ax.set_ylabel('% of enterprises using AI (EU27 mean)')
ax.set_ylim(0, 62)
ax.legend(frameon=False, loc='upper left')
save(fig, 'd1_adoption.png')

# D2 slope chart, AI density per bank
d2 = pd.read_csv(os.path.join(DATA, 'D2_bank_reports.csv'))
d2 = d2.dropna(subset=['ai_d'])
pv = d2.pivot_table(index='bank_code', columns='fy', values='ai_d').dropna()
fig, ax = plt.subplots(figsize=(5.2, 4.6))
for _, r in pv.iterrows():
    ax.plot([0, 1], [r[2022], r[2025]], color=LIGHT, lw=1.5)
ax.plot([0, 1], [pv[2022].median(), pv[2025].median()], color=RED, lw=4, marker='o')
ax.text(1.05, pv[2025].median(), f'median {pv[2025].median():.2f}', color=RED, va='center',
        fontsize=12, fontweight='bold')
ax.text(-0.05, pv[2022].median(), f'{pv[2022].median():.2f}', color=RED, va='center', ha='right',
        fontsize=12, fontweight='bold')
ax.set_xticks([0, 1])
ax.set_xticklabels(['FY2022', 'FY2025'])
ax.set_xlim(-0.35, 1.5)
ax.set_ylabel('AI mentions per 10,000 words')
ax.set_title(f'{len(pv)} of {len(pv)} banks rose', color=BLACK, fontsize=13)
save(fig, 'd2_slope.png')

# D2 governance bodies
fig, ax = plt.subplots(figsize=(4.2, 4))
ax.bar(['FY2022', 'FY2025'], [5, 42], color=[GREY, RED], width=0.55)
for x, v in enumerate([5, 42]):
    ax.text(x, v + 1.5, f'{v}%', ha='center', fontsize=16, fontweight='bold',
            color=RED if x else BLACK)
ax.set_ylim(0, 50)
ax.set_ylabel('% of paired banks naming an\nAI governance body')
save(fig, 'd2_govbody.png')

# D3 skills
fig, ax = plt.subplots(figsize=(7, 4))
sk = ['Data', 'Automation', 'Cyber', 'Regulatory']
ai = [51.4, 48.6, 19.4, 40.3]
oth = [25.3, 13.2, 5.5, 78.0]
x = range(len(sk))
ax.bar([i - 0.2 for i in x], oth, width=0.4, color=GREY, label='Other adverts')
ax.bar([i + 0.2 for i in x], ai, width=0.4, color=RED, label='AI-exposed adverts')
for i in x:
    ax.text(i - 0.2, oth[i] + 1.5, f'{oth[i]:.0f}%', ha='center', fontsize=11)
    ax.text(i + 0.2, ai[i] + 1.5, f'{ai[i]:.0f}%', ha='center', fontsize=11, color=RED,
            fontweight='bold')
ax.set_xticks(list(x))
ax.set_xticklabels(sk)
ax.set_ylabel('% of adverts asking for the skill')
ax.set_ylim(0, 90)
ax.legend(frameon=False, loc='upper left')
save(fig, 'd3_skills.png')
print(sorted(os.listdir(OUT)))
