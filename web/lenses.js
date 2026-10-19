'use strict';
(() => {
  const g = window.JACK_GUIDE;
  if (!g) throw new Error('Feature-guide evidence was not built.');
  const panel = document.getElementById('lens-panel');
  const content = document.getElementById('lens-content');
  const tabs = Array.from(document.querySelectorAll('[data-lens]'));
  const esc = v => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const pct = r => r.n ? (100*r.k/r.n).toFixed(1) : '—';
  const stat = r => `<div class="lens-stat"><span>${esc(r.label)}</span><strong>${pct(r)}%</strong><small>${r.k} survivors / ${r.n} passengers</small><div class="lens-bar" aria-hidden="true"><i style="width:${r.n?100*r.k/r.n:0}%"></i></div></div>`;
  const intro = (title,fields,question,context) => `<div class="lens-intro"><div><h3>${title}</h3><span class="lens-fields">${fields}</span></div><div class="lens-question"><b>THE QUESTION</b><p>${question}</p></div></div><p class="lens-context">${context}</p>`;
  const boundary = s => `<div class="lens-boundary"><b>DO NOT INFER</b><p>${s}</p></div>`;
  let active='class';
  let classView='all';
  function classLens(){
    const rows=classView==='all'?g.classes:g.young_men;
    return intro('A ticket records class.<br>It does not measure a life.','Pclass · Fare · Ticket','Was social position associated with survival—and does the pattern remain among similar passengers?','Ticket class represents a social and economic division. Fare adds information about recorded ticket costs, but it is not personal wealth. These fields can suggest questions about resources and access; they do not record who reached a lifeboat.')+
      `<div class="lens-switch" role="group" aria-label="Class comparison population"><button data-class-view="all" aria-pressed="${classView==='all'}">All 891 passengers</button><button data-class-view="young" aria-pressed="${classView==='young'}">Men with known ages 18–30</button></div><p class="source-note">${classView==='all'?'All training records, including missing ages.':'Known-age men only. This is the original H2 age window.'} Common scale: 0–100%.</p><div class="lens-stats">${rows.map(stat).join('')}</div>`+
      boundary('Buying a first-class ticket is not shown to cause rescue. Class groups differ in other ways. A shared ticket does not make two people duplicate records; zero fare does not prove poverty. Median recorded fare: '+g.fare.median.toFixed(2)+'; maximum: '+g.fare.max.toFixed(2)+'.');
  }
  function sexLens(){
    return intro('A social question.<br>Not a biological verdict.','Sex · Pclass · Survived','Did female and male passengers have different outcomes, including within the same class?','The recorded sex categories help investigate unequal outcomes that may reflect social evacuation practices, opportunities, or group composition. The table does not observe an individual decision by a crew member.')+
      `<p class="source-note">Whole training sample; all ages, including unknown ages. Common scale: 0–100%.</p><div class="lens-stats">${g.sexes.map(stat).join('')}</div>`+
      boundary('A sex gap is not proof of a biological cause or a guarantee that every woman was rescued. For H1 we compare adults aged 18–50 within each class, rather than relying on the overall gap.');
  }
  function ageLens(){
    return intro('“Young” is a definition.<br>Make yours visible.','Age · Sex · Survived','Do children, younger adults and older passengers show different recorded survival?','Age could relate to priority, dependence on others, or physical circumstances. Those explanations are not directly measured. For Jack, we use a fixed 18–25 proxy instead of searching for the age window with the most dramatic result.')+
      `<p class="source-note">All sexes and classes. The five non-overlapping groups include ${g.age_known} recorded ages; ${g.age_missing} unknown ages are excluded. Common scale: 0–100%.</p><div class="age-bars">${g.age_bands.map(r=>`<div class="age-line"><span>${esc(r.label)}</span><div class="lens-bar" aria-hidden="true"><i style="width:${100*r.k/r.n}%"></i></div><strong>${pct(r)}%<br><small>${r.k}/${r.n}</small></strong></div>`).join('')}</div>`+
      boundary('This is not a causal age effect: the groups mix different sexes and classes. Missingness also matters. Mean known age '+g.age_mean.toFixed(1)+'; median '+g.age_median.toFixed(0)+'. Unknown ages cannot be silently assigned to Jack’s group.');
  }
  function familyLens(){
    return intro('No relatives recorded<br>does not mean alone.','SibSp · Parch','Could travelling with recorded close relatives be associated with better survival?','SibSp counts siblings/spouses and Parch counts parents/children aboard. We use SibSp + Parch > 0 as a transparent recorded-relative flag. Companions might help, or create obligations, but those actions are not in the table.')+
      `<p class="source-note">Registered H3: third-class men with known ages 18–50. Common scale: 0–100%.</p><div class="lens-stats">${g.family_h3.map(stat).join('')}</div>`+
      boundary('Friends, an unmarried romantic partner, and all possible travelling companions are not measured by this flag. “Family saved him” is not established. Narrowing the age window to 18–25 reverses the observed direction, so the original H3 remains unchanged.');
  }
  function geographyLens(){
    return intro('A boarding port is not<br>a nationality.','Embarked · Cabin','What geography is actually recorded—and what location information is missing?','Embarked records the boarding port. It does not identify birthplace, nationality, language, or location at the time of the sinking. The route below is a schematic sequence, not a geographic map.')+
      `<div class="port-route">${g.ports.map(r=>`<div class="port-stop"><span>${esc(r.code)}</span><strong>${esc(r.label)}</strong><small>${r.n} passengers · ${r.k} survivors (${pct(r)}%)</small></div>`).join('')}</div><div class="port-warning">The ${g.ports_missing} missing ports are excluded. Port rates mix different class, age, and sex compositions: a boarding city is not a rescue mechanism.</div><p class="source-note">Cabin missingness by class: ${g.cabins.map(r=>`${esc(r.label)} ${(100*r.missing/r.n).toFixed(1)}% (${r.missing}/${r.n})`).join('; ')}.</p>`+
      boundary('Cabin may contain room labels, sometimes several per record, but it does not record evacuation-time position or a route to safety. Do not turn a missing cabin into a lower-deck assignment, and do not invent a map of Jack’s movements.');
  }
  function columnsLens(){
    const rows=[
      ['PassengerId','A passenger identifier.','A key, not a reason for survival.'],
      ['Survived','Recorded outcome: 0 = did not survive; 1 = survived.','The outcome we summarize—not a prediction.'],
      ['Pclass','Ticket class: first, second or third.','An ordered category, not continuous wealth.'],
      ['Name','Recorded passenger name and sometimes title.','Real people; no Jack Dawson film record is inserted.'],
      ['Sex','Recorded male/female category.','Use for transparent comparisons, not biological claims.'],
      ['Age','Age in years; fractional values can describe infants.','177 values are missing.'],
      ['SibSp','Number of siblings/spouses aboard.','Not a count of all companions.'],
      ['Parch','Number of parents/children aboard.','Combine with SibSp only with a stated definition.'],
      ['Ticket','Ticket reference.','May be shared by several genuine passengers.'],
      ['Fare','Recorded passenger fare.','Not income; shared tickets complicate interpretation.'],
      ['Cabin','Recorded cabin label or labels.','687 missing; no evacuation-time location.'],
      ['Embarked','C = Cherbourg; Q = Queenstown; S = Southampton.','2 missing; port does not mean nationality.']
    ];
    return intro('Twelve columns.<br>One row per passenger.','891 rows · 12 original columns','What do we have, what can we derive, and what should we leave unknown?','This dictionary follows Kaggle’s field definitions. Derived groups never replace the unchanged raw file. The survival rate is the sum of Survived divided by the number of passengers in the stated group.')+`<div class="dictionary">${rows.map(([name,meaning,caution])=>`<article><code>${name}</code><p>${meaning}<small>${caution}</small></p></article>`).join('')}</div>`;
  }
  const renderers={class:classLens,sex:sexLens,age:ageLens,family:familyLens,geography:geographyLens,columns:columnsLens};
  function render(){
    content.innerHTML=renderers[active]();
    panel.setAttribute('aria-labelledby','tab-'+active);
    tabs.forEach(t=>{const selected=t.dataset.lens===active;t.setAttribute('aria-selected',String(selected));t.tabIndex=selected?0:-1;});
    content.querySelectorAll('[data-class-view]').forEach(b=>b.addEventListener('click',()=>{classView=b.dataset.classView;render();content.querySelector(`[data-class-view="${classView}"]`).focus({preventScroll:true});}));
  }
  tabs.forEach((t,i)=>{
    t.addEventListener('click',()=>{active=t.dataset.lens;render();});
    t.addEventListener('keydown',e=>{
      let target=null;
      if(e.key==='ArrowRight') target=(i+1)%tabs.length;
      if(e.key==='ArrowLeft') target=(i+tabs.length-1)%tabs.length;
      if(e.key==='Home') target=0;
      if(e.key==='End') target=tabs.length-1;
      if(target!==null){e.preventDefault();active=tabs[target].dataset.lens;render();tabs[target].focus({preventScroll:true});}
    });
  });
  render();
})();
