'use strict';
(() => {
  const d = window.JACK_DATA;
  if (!d) throw new Error('Missing generated evidence. Run python src/build_exhibit.py.');
  const $ = id => document.getElementById(id);
  const percent = (k, n) => n ? (100 * k / n).toFixed(1) : null;
  const escape = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const grid = $('people-grid');
  for (let i = 0; i < d.jack.n; i++) {
    const dot = document.createElement('i');
    dot.className = i < d.jack.k ? 'alive' : '';
    dot.setAttribute('aria-hidden', 'true'); grid.append(dot);
  }
  $('poster-charts').innerHTML = d.charts.map((c, i) => {
    const bars = c.rows.map(r => `<div class="bar-group"><div class="bar-label"><span>${escape(r.label)}</span><strong>${percent(r.k,r.n)}% <small>(${r.k}/${r.n})</small></strong></div><div class="bar-track" aria-hidden="true"><i class="${escape(r.style)}" style="width:${percent(r.k,r.n)}%"></i></div></div>`).join('');
    return `<article class="chart-card"><div class="chart-meta">0${i+1} / ${escape(c.topic)}</div><h4>${escape(c.title)}</h4><p class="chart-sub">${escape(c.cohort)}</p><div class="chart-bars">${bars}</div><div class="axis" aria-hidden="true"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div><p class="chart-caption">${escape(c.caption)}</p></article>`;
  }).join('');
  const h1 = d.h1.map(r => `class ${r.class}: women ${r.fk}/${r.fn} (${percent(r.fk,r.fn)}%) vs men ${r.mk}/${r.mn} (${percent(r.mk,r.mn)}%)`).join('; ');
  const hypotheses = [
    ['H1','Women have higher observed survival than men within each class.','Ages 18-50. '+h1+'.','SURVIVED'],
    ['H2','First-class young men have higher observed survival than third-class young men.','Men ages 18-30. First class: 9/22 (40.9%); third: 19/130 (14.6%). The observed direction agrees; this is not an individual or causal prediction.','SURVIVED IN SAMPLE'],
    ['H3','Recorded close relatives are associated with higher survival for third-class men.','Men ages 18-50. Recorded relatives: 3/33 (9.1%); none recorded: 25/168 (14.9%). The observed direction opposes the hypothesis. Small groups prevent a confident broader conclusion.','NOT SUPPORTED']
  ];
  $('hypothesis-rows').innerHTML = hypotheses.map(([id,title,note,status]) => `<article class="hypothesis"><div class="hypothesis-code">${id}</div><div><h3>${escape(title)}</h3><p>${escape(note)}</p></div><span class="status ${id==='H3'?'no':''}">${status}</span></article>`).join('');
  const controls = ['sex','class','age','family'];
  function updateProfile() {
    const [sex, cl, age, family] = controls.map(id => $(id).value);
    const row = d.profiles[[sex,cl,age,family].join(':')];
    if (!row) throw new Error('Unknown profile key');
    const rate = percent(row.k,row.n);
    $('result-profile').textContent = `${['','First','Second','Third'][+cl]} class / ${sex==='male'?'men':'women'} / ages 18-${age}` + (family==='all'?'':` / ${family==='yes'?'relatives recorded':'none recorded'}`);
    $('result-rate').innerHTML = row.n ? `${rate}<small>%</small>` : '<small>No observations</small>';
    $('result-meter').style.width = (rate || 0) + '%';
    $('result-count').textContent = `${row.k} survivor${row.k===1?'':'s'} out of ${row.n} passenger${row.n===1?'':'s'}`;
    $('result-interval').textContent = row.n ? `${(100*row.lo).toFixed(1)}%-${(100*row.hi).toFixed(1)}%` : 'Not defined';
    $('small-warning').textContent = !row.n ? 'No recorded passengers match these filters. Do not treat an empty group as 0% survival.' : row.n < 30 ? `Small group (n=${row.n}): one outcome changes the rate by ${(100/row.n).toFixed(1)} percentage points.` : 'The interval describes sampling uncertainty under a binomial model, not all uncertainty.';
  }
  controls.forEach(id => $(id).addEventListener('change', updateProfile));
  $('reset').addEventListener('click', () => {
    ['male','3','25','all'].forEach((v,i) => $(controls[i]).value = v); updateProfile();
  });
  updateProfile();
  const menu = $('menu-button'), nav = $('navigation');
  function closeMenu(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');}
  menu.addEventListener('click', () => {const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => {if(e.key==='Escape')closeMenu();});
  let scrolling=false;
  const track = () => {const height=document.documentElement.scrollHeight-innerHeight;$('read-progress').style.width=(height>0?Math.min(100,100*scrollY/height):0)+'%';scrolling=false;};
  addEventListener('scroll',()=>{if(!scrolling){scrolling=true;requestAnimationFrame(track);}},{passive:true});
  addEventListener('resize',track);track();
  const scenes = [
    ['The ending we know.','In the film, Jack remains in the freezing water while Rose waits for rescue. Their future together disappears.'],
    ['Imagine a boat returning sooner.','A light finds them. Someone reaches into the water before it is too late. This is an invented rescue, not a historical claim.'],
    ['Two lives, after the Atlantic.','In this alternate story, Jack lives. But inventing a different ending is much easier than showing what would have caused it.'],
    ['Now close the screenplay.','The dataset has no rescue clock or lifeboat access variable. We cannot test this ending. We can study the people who actually survived.']
  ];
  const dialog=$('story-dialog');let scene=0,timer=null,opener=null;
  function stop(){if(timer){clearInterval(timer);timer=null;}$('play-scenes').textContent='\u25b6 PLAY';}
  function renderScene(){
    $('motion-stage').dataset.scene=String(scene);
    $('scene-counter').textContent=`SCENE 0${scene+1} / 04`;
    $('scene-title').textContent=scenes[scene][0];$('scene-copy').textContent=scenes[scene][1];
    $('previous-scene').disabled=scene===0;$('next-scene').disabled=scene===scenes.length-1;
  }
  document.querySelectorAll('[data-open-story]').forEach(button=>button.addEventListener('click',()=>{
    opener=button;scene=0;stop();renderScene();dialog.showModal();document.body.classList.add('no-scroll');$('close-dialog').focus();
  }));
  $('close-dialog').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',()=>{stop();document.body.classList.remove('no-scroll');if(opener)opener.focus();});
  dialog.addEventListener('click',e=>{if(e.target===dialog){const b=dialog.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)dialog.close();}});
  $('previous-scene').addEventListener('click',()=>{stop();scene=Math.max(0,scene-1);renderScene();});
  $('next-scene').addEventListener('click',()=>{stop();scene=Math.min(scenes.length-1,scene+1);renderScene();});
  $('play-scenes').addEventListener('click',()=>{
    if(timer){stop();return;}if(scene===scenes.length-1){scene=0;renderScene();}
    $('play-scenes').textContent='\u275a\u275a PAUSE';timer=setInterval(()=>{if(scene<scenes.length-1){scene++;renderScene();}else stop();},6500);
  });
  dialog.addEventListener('keydown',e=>{if(e.key==='ArrowRight'&&scene<3){e.preventDefault();stop();scene++;renderScene();}if(e.key==='ArrowLeft'&&scene>0){e.preventDefault();stop();scene--;renderScene();}});
  renderScene();
})();
