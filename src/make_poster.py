"""Generate the single-page three-chart research poster from the unmodified data."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from analysis import load_data, observed, summaries, jack_like, young_men, family_group, ROOT

OUT=ROOT/'poster'
OUT.mkdir(exist_ok=True)
D=load_data()
s=summaries(D)

BG='#0F1015'; INK='#FAF5F1'; MUTED='#ACAAB2'; ACCENT='#F15A79'; PALE='#999AA7'; BLUE='#C0CAD3'; GRID='#41434A'
plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'axes.linewidth':0.0})
fig=plt.figure(figsize=(16,9),facecolor=BG)
fig.text(.052,.951,'TITANIC  /  GROUP 01',ha='left',color=ACCENT,fontsize=11,weight='bold')
fig.text(.949,.951,'ONE PAGE. ONE FINDING.',ha='right',color=MUTED,fontsize=10,weight='bold')
fig.text(.052,.868,'COULD JACK HAVE BEEN SAVED?',color=INK,fontsize=31,weight='bold')
fig.text(.052,.792,'Only 10 of 86 Jack-like men survived; first class was associated with better',
         color=INK,fontsize=17.4,weight='bold')
fig.text(.052,.749,'survival for young men, but class was not a simple safety ladder.',
         color=INK,fontsize=17.4,weight='bold')
fig.add_artist(Line2D([.052,.948],[.708,.708],transform=fig.transFigure,color=GRID,lw=1.2))

xs=[.06,.375,.69]
ax_width=.245

def mini_axis(x):
    a=fig.add_axes([x+.075,.305,ax_width-.075,.235])
    a.set_facecolor(BG)
    a.set_xlim(0,100)
    a.set_xticks([0,25,50,75,100],['0','25','50','75','100'])
    a.tick_params(axis='x',length=0,labelsize=9,colors=MUTED,pad=7)
    a.tick_params(axis='y',length=0,labelsize=10,colors=INK,pad=8)
    for k in a.spines: a.spines[k].set_visible(False)
    a.grid(axis='x',color=GRID,lw=.7)
    a.set_axisbelow(True)
    return a

def bars(a,labels,rows,colors):
    # Top-to-bottom: list order. Rows: (survivors, total)
    ys=list(range(len(rows)-1,-1,-1))
    a.barh(ys,[100*s/n for s,n in rows],color=colors,height=.42,zorder=5)
    a.set_ylim(-.7,len(rows)-.3)
    a.set_yticks(ys,labels)
    for y,(n_s,n_p) in zip(ys,rows):
        v=100*n_s/n_p
        a.text(min(v+2.0,100),y,f'{v:.1f}%',ha='left' if v<=82 else 'right',
               color=INK,va='center',fontsize=11,weight='bold')

# Chart 1: sex difference among third-class peers, not conflating classes
peers=observed(D[(D.Pclass==3)&D.Age.between(18,25)],'Sex')
ax1=mini_axis(xs[0])
bars(ax1,['Young men','Young women'],
     [(int(peers.loc['male','survived']),int(peers.loc['male','passengers'])),
      (int(peers.loc['female','survived']),int(peers.loc['female','passengers']))],
     [ACCENT,BLUE])

# Chart 2: expose ALL classes, including the nonmonotonic second-class result
h2=s['h2']
ax2=mini_axis(xs[1])
bars(ax2,['First class','Second class','Third class'],
     [(int(h2.loc[c,'survived']),int(h2.loc[c,'passengers'])) for c in (1,2,3)],
     [BLUE,ACCENT,PALE])

# Chart 3: keep a rejected registered hypothesis visible
h3=s['h3']
ax3=mini_axis(xs[2])
bars(ax3,['No relatives recorded','Relatives recorded'],
     [(int(h3.loc[False,'survived']),int(h3.loc[False,'passengers'])),
      (int(h3.loc[True,'survived']),int(h3.loc[True,'passengers']))],
     [BLUE,ACCENT])

for x,heading,note in zip(xs,[
    '01  /  YOUNG WOMEN FARED BETTER',
    '02  /  CLASS WAS NOT A LADDER',
    '03  /  NO CLEAR FAMILY ADVANTAGE',
],[
    '3rd class, ages 18–25: men 10/86; women 14/30.',
    'Men 18–30: 1st 9/22; 2nd 1/41; 3rd 19/130.',
    '3rd-class men 18–50: none 25/168; yes 3/33.',
]):
    fig.text(x,.642,heading,color=INK,fontsize=12,weight='bold')
    fig.text(x,.245,note,color=MUTED,fontsize=9.7)

fig.add_artist(Line2D([.052,.948],[.166,.166],transform=fig.transFigure,color=GRID,lw=1.2))
fig.text(.052,.124,'WHAT DATA CANNOT TELL US',color=ACCENT,fontsize=10,weight='bold')
fig.text(.258,.124,'Whether changing Jack\'s ticket would save him: lifeboat access and evacuation timing are unobserved.',
         color=INK,fontsize=10)
fig.text(.052,.067,'SOURCE  ·  Kaggle Titanic training set (891 passenger records)',color=MUTED,fontsize=9.5)
fig.text(.948,.067,'GROUP MEMBERS  ·  [ADD NAMES BEFORE SUBMISSION]',color=MUTED,fontsize=9.5,ha='right')

fig.savefig(OUT/'titanic_jack_poster.pdf',facecolor=BG)
fig.savefig(OUT/'preview.png',dpi=160,facecolor=BG)
plt.close(fig)
print('Poster generated with exactly three code-generated axes/charts.')
