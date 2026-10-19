"""Generate the required landscape PDF: exactly three code-generated charts."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from analysis import ROOT, load_data, observed, summaries

OUT = ROOT / 'poster'
OUT.mkdir(exist_ok=True)
d = load_data()
s = summaries(d)
peers = observed(d[(d.Pclass == 3) & d.Age.between(18, 25)], 'Sex')
BG, INK, MUTED, GRID = '#F5F1E9', '#152733', '#52616A', '#D2D7D0'
GOLD, CORAL, SLATE = '#987449', '#AE594B', '#617684'
plt.rcParams.update({'font.family':'DejaVu Sans', 'pdf.fonttype':42, 'axes.linewidth':0})
fig = plt.figure(figsize=(16,9), facecolor=BG)
fig.text(.045,.951,'THE JACK FILE  /  GROUP 01',color=GOLD,fontsize=10,weight='bold')
fig.text(.955,.951,'ONE PAGE, ONE FINDING',ha='right',color=MUTED,fontsize=10)
fig.text(.045,.860,'COULD JACK HAVE BEEN SAVED?',fontsize=31,weight='bold',color=INK)
fig.text(.045,.786,'Only 10 of 86 Jack-like men survived; first-class young men fared better',fontsize=18.2,color=INK)
fig.text(.045,.742,'than third-class peers, but class was not a simple survival ladder.',fontsize=18.2,color=INK)
fig.add_artist(Line2D([.045,.955],[.701,.701],transform=fig.transFigure,color=GRID,lw=1))

def pair(row):
    return int(row.survived),int(row.passengers)

charts = [
    ('01 / YOUNG WOMEN FARED BETTER','Third class, known ages 18-25',
     [('Men',*pair(peers.loc['male']),CORAL),('Women',*pair(peers.loc['female']),GOLD)],
     'Same class and age range; women had higher survival.'),
    ('02 / CLASS WAS NOT A LADDER','Men, known ages 18-30',
     [(label,*pair(s['h2'].loc[c]),col) for c,label,col in [(1,'First class',GOLD),(2,'Second class',CORAL),(3,'Third class',SLATE)]],
     'Second class was lower than third in this subgroup.'),
    ('03 / NO CLEAR FAMILY ADVANTAGE','Third-class men, known ages 18-50',
     [('None recorded',*pair(s['h3'].loc[False]),SLATE),('Relatives recorded',*pair(s['h3'].loc[True]),CORAL)],
     'The registered family hypothesis was not supported.')
]
for x,(title,cohort,rows,caption) in zip([.045,.360,.675],charts):
    fig.text(x,.643,title,color=INK,fontsize=11.5,weight='bold')
    fig.text(x,.602,cohort,color=MUTED,fontsize=10.2)
    ax=fig.add_axes([x,.312,.277,.248],facecolor=BG)
    n=len(rows)
    for i,(label,k,total,col) in enumerate(rows):
        y=n-1-i
        ax.barh(y,100*k/total,color=col,height=.25,zorder=3)
        ax.text(0,y+.24,label,color=INK,fontsize=11,va='bottom')
        ax.text(100,y+.24,f'{100*k/total:.1f}%  ({k}/{total})',ha='right',va='bottom',color=INK,fontsize=10.5,weight='bold')
    ax.set(xlim=(0,100),ylim=(-.35,n-.35))
    ax.set_yticks([])
    ax.set_xticks([0,25,50,75,100],['0%','25%','50%','75%','100%'])
    ax.tick_params(axis='x',length=0,pad=7,labelsize=9,colors=MUTED)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.grid(axis='x',color=GRID,lw=.7,zorder=0)
    fig.text(x,.245,caption,fontsize=9.3,color=MUTED)
fig.add_artist(Line2D([.045,.955],[.184,.184],transform=fig.transFigure,color=GRID,lw=1))
fig.text(.045,.140,'WHAT DATA CANNOT TELL US',color=GOLD,fontsize=9.7,weight='bold')
fig.text(.268,.140,"Whether changing Jack's ticket would save him: lifeboat access and evacuation timing are unobserved.",color=INK,fontsize=9.8)
fig.text(.045,.082,'SOURCE: Kaggle Titanic training sample (891 records) | Known ages only in these comparisons.',color=MUTED,fontsize=8.8)
fig.text(.045,.046,'Kleant Laboti  |  Elona Tarja  |  Sarita Koci',color=INK,fontsize=9.2)
fig.text(.955,.046,'GROUP 01  /  19 OCTOBER 2026',ha='right',color=MUTED,fontsize=8.8)
assert len(fig.axes)==3
fig.savefig(OUT/'titanic_jack_poster.pdf',facecolor=BG)
fig.savefig(OUT/'preview.png',dpi=150,facecolor=BG)
plt.close(fig)
print('Poster: one landscape page, exactly three code-generated axes.')
