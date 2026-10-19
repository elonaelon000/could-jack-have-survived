# Notebook-u i Titanic, i shpjeguar nga fillimi

**Udhëzues në shqip · Group 1 · The Jack File**

Ky është një shpjegim mësimor i notebook-ut kryesor `notebooks/titanic_jack_analysis.ipynb`, jo një analizë tjetër. Shembujt e shkurtuar më poshtë shpjegojnë kodin; nuk zëvendësojnë qelizat origjinale. Numërimi 1–13 u referohet vetëm qelizave me kod, jo qelizave me tekst. Lexoje krahas [notebook-ut të ekzekutuar](notebook.html).

## 0. Çfarë po bëjmë në të vërtetë?

Nuk po ndërtojmë një program që parashikon nëse Jack-u do të jetonte. Po analizojmë të dhëna të regjistruara: kush mbijetoi dhe cilat karakteristika kishin grupe të ndryshme pasagjerësh.

Pyetja është: **çfarë ndodhi me pasagjerë realë që i ngjanin profilit të Jack-ut?** Ai është personazh imagjinar, prandaj nuk ka rresht në tabelë. Përkufizojmë një grup krahasimi: burra, klasë e tretë, moshë e njohur 18–25. Në atë grup janë 86 pasagjerë dhe 10 mbijetuan. Burimi është `data/train.csv` i pandryshuar; origjina dokumentohet në [Kaggle](https://www.kaggle.com/competitions/titanic/data).

Një notebook është dokument që bashkon tekst, kod dhe rezultatet e ekzekutimit. Qelizat Markdown shpjegojnë; qelizat Python llogarisin. Një tabelë ose grafik poshtë kodit është rezultati, jo diçka e shkruar automatikisht nga filmi. Qelizat duhen ekzekutuar nga lart poshtë, sepse njëra krijon variabla që i përdor tjetra.

## 1. Struktura me shtatë pjesë

| Pjesa | Pyetja që zgjidh |
|---|---|
| 1. Load and profile | Çfarë kemi marrë dhe sa e plotë është tabela? |
| 2. Three hypotheses | Çfarë prisnim të shihnim përpara analizës së rezultateve? |
| 3. Cleaning | Çfarë ruajmë, çfarë kontrollojmë dhe çfarë nuk shpikim? |
| 4. Explore | Si shpërndahen pasagjerët dhe si ndryshojnë normat? |
| 5. Test | A përputhen drejtimet e vëzhguara me hipotezat fillestare? |
| 6. Three problems | Cilat dobësi mund t'i tregojmë me numra dhe kod? |
| 7. Conclusion | Çfarë mbështesin të dhënat dhe çfarë jo? |

Faqja e projektit shërben si prezantim. Notebook-u shërben si provë: lejon dikë tjetër të ndjekë llogaritjet.

## 2. Fjalori që na duhet përpara kodit

**`df`** është thjesht një emër variabli, shkurt për DataFrame. Një DataFrame është tabelë me rreshta dhe kolona. Këtu një rresht është një pasagjer. **`clean`** është kopja ku krijojmë kolona ndihmëse. **`jack`** është nën-tabela e pasagjerëve që kalojnë filtrat e Jack-ut.

**`pd`** është emri i shkurtër që i japim pandas. **`np`** është emri i shkurtër i NumPy. **`plt`** është emri i shkurtër i pjesës së Matplotlib që përdorim për grafikë. Këto nuk janë modele të trajnuara.

**`True` dhe `False`** janë përgjigje logjike: kushti plotësohet ose jo. **`NaN`** tregon vlerë të munguar; nuk do të thotë moshë zero. **`n`** është numri i pasagjerëve në grup, kurse **`k`** numri i të mbijetuarve. Në tabelat tona shfaqen shpesh si `passengers` dhe `survived`.

## 3. Qeliza e kodit 1 — hapja, paketimi dhe kontrollet

Qeliza e parë duket shumë e gjatë sepse notebook-u është bërë i përdorshëm pa shkarkuar të gjithë repository-n. Brenda saj është një kopje e kompresuar e CSV-së origjinale.

`base64.b64decode(...)` kthen tekstin e paketuar në byte. `gzip.decompress(...)` shpaketon ato byte. `hashlib.sha256(...)` llogarit një gjurmë të skedarit dhe e krahason me gjurmën e kopjes origjinale. **Ky kontroll tregon që përdorim të njëjtin skedar; nuk provon që çdo regjistrim historik është pa gabime.** Kodimi nuk është enkriptim, të dhëna të simuluara apo trajnim modeli.

Pjesa analitike që duhet të kuptosh është shumë më e thjeshtë:

```python
df = load_data()
print(df.shape)
df.info()
display(df.isna().sum().rename('missing').to_frame())
display(df.head())
```

`load_data()` lexon CSV-në dhe kthen DataFrame. `df.shape` jep `(891, 12)`: 891 rreshta dhe 12 kolona. `df.info()` tregon tipet e kolonave dhe sa vlera jo të munguara kanë. `df.head()` tregon pesë rreshtat e parë, jo të gjithë dataset-in.

Te `df.isna().sum()`, fillimisht `isna()` shënon boshllëqet me `True`. Pastaj `sum()` i numëron për çdo kolonë. Rezultati është 177 mosha, 687 kabina dhe 2 porte të munguar. `rename('missing')` emërton rezultatin; `to_frame()` e paraqet si tabelë me një kolonë.

`assert` kontrollon një kusht dhe e ndalon kodin kur kushti është i gabuar. Për shembull, kontrollojmë që madhësia të jetë `(891, 12)`, ID-të të jenë unike dhe `Survived` të përmbajë vetëm 0 ose 1. Kjo na mbron nga përdorimi pa dashje i një skedari tjetër.

Në prezantim: **“Fillimisht kontrolluam strukturën, tipet dhe mungesat, pa nxjerrë përfundime për mbijetesën e grupeve.”**

## 4. Çfarë përfaqëson secila kolonë?

| Kolona | Kuptimi | Çfarë nuk duhet të supozojmë |
|---|---|---|
| PassengerId | Identifikues i pasagjerit | ID më e lartë nuk do të thotë pozitë më e mirë. |
| Survived | 0 = nuk mbijetoi, 1 = mbijetoi | Është rezultat i regjistruar, jo parashikim. |
| Pclass | Klasa e biletës: 1, 2 ose 3 | Nuk mat e vetme pasurinë ose aksesin në varkë. |
| Name | Emri i pasagjerit | Nuk mund të gjejmë personazhin imagjinar Jack këtu. |
| Sex | Kategoria e seksit e regjistruar | Nuk regjistron vendimin e ekuipazhit për çdo njeri. |
| Age | Mosha në vite | Një vlerë bosh nuk është zero. Ka edhe mosha fraksionare. |
| SibSp | Vëllezër/motra ose bashkëshort/e në bord | Nuk numëron çdo mik apo bashkudhëtar. |
| Parch | Prindër ose fëmijë në bord | Nuk përshkruan gjithë rrjetin shoqëror. |
| Ticket | Numri ose kodi i biletës | Bileta e përbashkët nuk është ID e dyfishtë pasagjeri. |
| Fare | Tarifa e regjistruar | Nuk është automatikisht paga ose pasuria individuale. |
| Cabin | Etiketa e kabinës | Nuk na tregon ku ishte personi gjatë evakuimit. |
| Embarked | S, C, Q: Southampton, Cherbourg, Queenstown | Porti i hipjes nuk është kombësia ose vendi i lindjes. |

Kuptimet vijnë nga fjalori i Kaggle dhe dokumentimi i projektit. Kolonat si `Pclass` kanë kode numerike, por mesatarja e tyre nuk interpretohet si një “klasë mesatare” fizike.

## 5. Funksionet ndihmëse — përkufizime që ripërdoren

Qeliza e parë përkufizon disa funksione. `def` krijon një funksion; `return` jep rezultatin. Përkufizimi nuk do të thotë se analiza është kryer: duhet ta thërrasim funksionin me të dhëna.

`jack_like(data)` zgjedh burra të klasës së tretë me moshë 18–25. `young_men(data, low=18, high=30)` zgjedh burra me moshë brenda kufijve, pa kufizim klase. `adults(data)` në këtë projekt zgjedh vetëm 18–50, jo çdo të rritur. `family_group(data)` zgjedh burra të klasës së tretë 18–50 dhe krijon treguesin e të afërmve. `wilson(k, n)` kthen kufirin e poshtëm dhe të sipërm të intervalit të normës.

Funksioni më i përdorur është:

```python
def observed(data, keys):
    return data.groupby(keys, observed=True, dropna=False).Survived.agg(
        survived='sum',
        passengers='count',
        rate='mean'
    )
```

`keys` tregon sipas cilave kolona ndahet tabela. `groupby` krijon grupet; `Survived` zgjedh rezultatin që matim; `agg` kryen tri llogaritje në çdo grup. Meqë nuk mungon asnjë `Survived`, `count` këtu është numri i pasagjerëve. `sum` numëron njëshat, pra të mbijetuarit. `mean` jep normën sepse mesatarja e një kolone 0/1 është shuma e njëshave pjesëtuar me numrin e vlerave.

`observed=True` shmang kategoritë pa vëzhgime kur grupojmë kategori; nuk do të thotë “rezultate të provuara”. `dropna=False` lejon edhe grup për çelësa të munguar. Kjo është veçanërisht e rëndësishme kur lexojmë grupet e moshës.

## 6. Hipotezat dhe intervalet e moshës

Hipoteza është pritshmëri e shprehur përpara se të shohim krahasimin e rezultateve. Mund të mos mbështetet nga të dhënat.

**H1:** për moshat 18–50, gratë kanë normë më të lartë mbijetese se burrat brenda secilës klasë. **H2:** për burra 18–30, norma e klasës së parë është më e lartë se e klasës së tretë. **H3:** për burra të klasës së tretë 18–50, të afërmit e regjistruar lidhen me normë më të lartë mbijetese sesa mungesa e të afërmve të regjistruar.

18–25 është profili i ngushtë i Jack-ut, 18–30 është dritarja e H2 dhe 18–50 përdoret te H1/H3. Këto mbivendosen. Kufijtë janë zgjedhje të projektit, jo përfundime të një optimizimi statistikor. Dritarja më e gjerë shton njerëz, por largohet nga profili i ngushtë i personazhit. [Shpjegimi i plotë i intervaleve](methods.html).

Kufijtë ndodhen në [commit-in fillestar](https://github.com/elonaelon000/could-jack-have-survived/commit/7a423658689667bbf34772da22bb66c945d7ee90). Ky udhëzues dhe shpjegimi i hollësishëm janë shtuar më vonë; nuk duhen paraqitur sikur ekzistonin përpara rezultateve.

## 7. Qeliza e kodit 2 — pastrimi pa shpikur të dhëna

```python
clean = df.copy()
clean['RecordedRelatives'] = (clean.SibSp + clean.Parch) > 0
assert len(clean) == len(df)
```

`copy()` krijon tabelën e punës. Nuk ndryshojmë CSV-në. `RecordedRelatives` është një kolonë e re logjike: të paktën një i afërm i regjistruar apo asnjë. Nëse `SibSp=1` dhe `Parch=0`, shuma është 1 dhe rezultati `True`. Nëse të dyja janë 0, rezultati është `False`.

**`False` nuk do të thotë “udhëtonte vetëm”.** Mund të kishte miq ose bashkudhëtarë që këto dy kolona nuk i regjistrojnë.

Qeliza kontrollon rreshtat identikë, ID-të dhe tarifat zero. Tarifë zero është sinjal për ta shqyrtuar, jo autorizim që ta fshijmë. Nuk mbushim moshat me mesataren sepse do të shpiknim se kush hyn në filtrin 18–25. Nuk fshijmë të gjithë rreshtat që kanë kabinën bosh, sepse do të humbnim pjesën më të madhe të tabelës.

Të 891 pasagjerët mbeten në `clean`; filtrat krijojnë nën-tabela. Kjo është ndryshe nga fshirja e rreshtave nga të dhënat bazë.

## 8. Qeliza e kodit 3 — përmbledhja e kolonave

`describe(include='all')` përmbledh të gjitha kolonat. Te numrat shohim `count`, `mean`, `std`, `min`, kuartilet dhe `max`. `mean` është mesatarja; 50% është mediana; 25% dhe 75% tregojnë kuartilet. Te teksti shfaqen numri i vlerave të ndryshme, më e shpeshta (`top`) dhe sa herë shfaqet (`freq`). Boshllëqet në këtë përmbledhje mund të tregojnë statistikë të pazbatueshme për atë tip, jo domosdoshmërisht mungesë në CSV.

`.T` ndërron rreshtat me kolonat vetëm për paraqitjen. `.round(2)` rrumbullakos shfaqjen; nuk duhet të rrumbullakosim të dhënat bazë përpara llogaritjeve.

`value_counts(dropna=False)` numëron sa herë shfaqet secila vlerë dhe nuk fsheh kategorinë e munguar. `rename(...).to_frame()` e bën rezultatin më të lexueshëm. Cikli `for field in [...]` përsërit të njëjtën procedurë për disa kolona.

## 9. Qeliza e kodit 4 — kush gjendet në kampion?

Kjo qelizë shfaq statistika për moshën, tarifën dhe familjen, një tabelë klasë × seks me `pd.crosstab`, dhe tre grafikë: shpërndarjen e moshës, numrat sipas klasës dhe numrat sipas seksit.

Histograma e moshës numëron sa njerëz bien në intervale të vogla; nuk mat ende mbijetesën. `Age.dropna()` heq moshat e panjohura vetëm nga ky vizatim. `bins=24` krijon intervale vizatimi, jo 24 hipoteza. Grafikët e klasës dhe seksit tregojnë madhësinë e grupeve, që më pas të mos ngatërrojmë numrat me normat.

Te `fig, axes = plt.subplots(1, 3, ...)`, `fig` është figura e plotë dhe `axes` janë tre zonat e vizatimit. `axes[0]` është grafiku i parë. `xlabel`, `ylabel`, `title` vendosin etiketat; `tight_layout()` rregullon hapësirat; `show()` shfaq figurën. Ngjyra ndryshon pamjen, jo llogaritjen.

## 10. Qeliza e kodit 5 — nga numrat te normat

Në të gjithë kampionin kemi 342 të mbijetuar nga 891: rreth 38.4%. Pastaj `observed(clean, ['Pclass','Sex'])` llogarit normën për çdo kombinim klasë–seks.

`unstack('Sex')` e kthen nivelin e seksit në kolona, që gratë dhe burrat të vizatohen krah për krah. `PercentFormatter(1)` e shfaq 0.4 si 40%, ndërsa vlera numerike mbetet 0.4. `set_ylim(0,1)` vendos boshtin nga 0% në 100%.

Një klasë mund të ketë më shumë të mbijetuar vetëm sepse ka më shumë pasagjerë. Prandaj krahasimi kryesor është **të mbijetuar / pasagjerë**, jo vetëm të mbijetuar. Numëruesin dhe emëruesin i tregojmë bashkë.

## 11. Qeliza e kodit 6 — grupet e moshës dhe një kujdes teknik

`pd.cut` krijon kolonën ndihmëse `AgeBand` për eksplorim. Nuk është dropdown-i me tre dritare të mbivendosura. Këto intervale të grafikut e ndajnë moshën në kategori.

Në kodin ekzistues kufijtë janë `[-0.01, 12, 17, 25, 35, 50, 65, 110]`. Me parametrat e përdorur, intervalet mbyllen djathtas: për shembull, midis 17 dhe 25 kemi **17 < Age <= 25**. Etiketa e shkurtuar “18–25” në atë grafik nuk e ndryshon këtë kusht dhe mund të jetë e pasaktë për një moshë fraksionare si 17.5. **Hipotezat përdorin `Age.between(18, ...)`, jo etiketën `AgeBand`, ndaj ky dallim nuk e ripërcakton grupin e Jack-ut.**

Gjithashtu, `observed(..., dropna=False)` mund të shfaqë grupin me moshë të panjohur si `nan`. Ai nuk është interval moshe; lexoje si “moshë e paregjistruar”, pavarësisht shënimit të shkurtër që printon qeliza. Ky udhëzues i bën kufijtë realë të qartë pa ndryshuar kodin origjinal. Sjellja dokumentohet te [pandas.cut](https://pandas.pydata.org/docs/reference/api/pandas.cut.html).

Në fund qeliza jep edhe normat sipas të afërmve në të gjithë tabelën. Ai është eksplorim i përgjithshëm, **jo testi H3**, i cili ka filtra shtesë.

## 12. Qeliza e kodit 7 — si dalin 10 dhe 86?

Kodi thërret `jack_like(clean)`. I shkruar hapur, filtri ka këtë kuptim:

```python
mask = (
    (clean['Sex'] == 'male')
    & (clean['Pclass'] == 3)
    & clean['Age'].between(18, 25)
)
jack = clean.loc[mask]
```

`==` pyet për barazi; `=` cakton një vlerë. `&` kërkon që kushtet të jenë të vërteta së bashku për të njëjtin rresht. Kllapat ndajnë kushtet. `.loc[mask]` ruan rreshtat ku rezultati është `True`. Për këtë lloj filtrimi nuk zëvendësojmë `&` me `and`.

```python
n = len(jack)                  # 86 pasagjere
k = int(jack['Survived'].sum()) # 10 te mbijetuar
rate = jack['Survived'].mean()  # 10 / 86
```

`rate` është afërsisht 0.1163. Formati `:.1%` e shfaq 11.6%, me një shifër dhjetore; nuk e shumëzojmë edhe një herë me 100 para këtij formati.

Qeliza provon edhe kufijtë e sipërm 25, 30 dhe 35 në një cikël. Këto janë kontrolle eksploruese të ndjeshmërisë. Në fund krahason gra dhe burra të klasës së tretë 18–25: 14/30 gra dhe 10/86 burra mbijetuan. Ky është konteksti i grafikut të parë të posterit, jo H1 i plotë.

## 13. Qeliza e kodit 8 — H1

`adults(clean)` ruan 18–50. `observed(..., ['Pclass','Sex'])` llogarit normat për secilën klasë dhe seks. Një indeks me këta dy nivele lejon `h1.loc[(c, 'female')]` të marrë gratë e klasës `c`.

| Klasa | Gra | Burra |
|---|---|---|
| 1 | 62/64 = 96.9% | 31/71 = 43.7% |
| 2 | 54/59 = 91.5% | 5/76 = 6.6% |
| 3 | 27/66 = 40.9% | 28/201 = 13.9% |

Cikli krahason normat e grave dhe burrave në çdo klasë dhe ruan rezultatet logjike në një listë. `all(h1_outcomes)` është `True` vetëm kur të tria krahasimet kanë drejtimin e pritur. Prandaj H1 shënohet **SURVIVED**.

Kjo tregon lidhjen në të dhënat tona. Nuk provon mekanizmin që e shkaktoi për secilin pasagjer dhe nuk përjashton dallimet e moshës brenda intervalit.

## 14. Qeliza e kodit 9 — H2 dhe diferenca në pikë përqindjeje

Filtri mban burra 18–30; grupimi është sipas klasës.

| Klasa | Të mbijetuar / pasagjerë | Norma |
|---|---|---|
| 1 | 9/22 | 40.9% |
| 2 | 1/41 | 2.4% |
| 3 | 19/130 | 14.6% |

`h2.loc[1,'rate']` merr normën e klasës 1. Diferenca kundrejt klasës 3 llogaritet si:

```python
gap = 100 * (h2.loc[1, 'rate'] - h2.loc[3, 'rate'])
```

Rezultati është rreth **+26.3 pikë përqindjeje**, jo automatikisht “26.3% më shumë”. Diferenca relative do të kishte formulë tjetër. Meqë diferenca është pozitive, H2 përputhet me drejtimin e pritur.

Klasa 2 shfaqet gjithashtu: është më poshtë se klasa 3. Kjo kundërshton një shkallëzim të thjeshtë 1 > 2 > 3, por **nuk kundërshton H2**, që pyet vetëm nëse 1 > 3. `iterrows()` na lejon të kalojmë rreshtat e tabelës për të printuar numrat dhe intervalet. Grafiku e vizaton këtë krahasim.

## 15. Çfarë bën `wilson(k, n)`?

Funksioni jep një interval afërsisht 95% për një përpjesëtim, nën një model binomial. Kodi përdor `z=1.96`, normën `p=k/n`, një qendër të korrigjuar dhe gjysmën e gjerësisë së intervalit. Për grupe shumë të vogla intervali zakonisht është i gjerë; 3 nga 10 njerëz nuk mbështesin një normë me saktësi të lartë.

Nuk duhet ta shpjegosh si “Jack-u kishte 95% mundësi të binte brenda këtyre kufijve”. Nën supozimet e modelit, procedura synon mbulim rreth 95% në përsëritje të kampionimit. Këtu kemi një kampion historik të kufizuar; intervali nuk e korrigjon përzgjedhjen, mungesat, varësinë familjare apo faktorët e paregjistruar.

Notebook-u **nuk llogarit një p-value për H1/H2/H3**. Statuset bazohen në drejtimin e vëzhguar. Mbivendosja e dy intervaleve të veçanta nuk është vetë test i vlefshëm i diferencës së normave.

## 16. Qeliza e kodit 10 — H3

`family_group(clean)` mban burra të klasës së tretë 18–50 dhe shton treguesin e të afërmve. Grupi `True` ka të paktën një të afërm të regjistruar; `False` ka zero të afërm të regjistruar në ato dy kolona.

Me të afërm të regjistruar: **3/33 = 9.1%**. Pa të afërm të regjistruar: **25/168 = 14.9%**. Diferenca “me minus pa” është rreth **−5.8 pikë përqindjeje**.

H3 priste normë më të lartë për grupin me të afërm. Në këtë popullatë të përcaktuar, drejtimi është i kundërt, ndaj rezultati shënohet **NOT SUPPORTED**. Nuk shkruajmë se familja shkakton vdekje, nuk ka rëndësi, apo se personat pa të afërm udhëtonin vetëm. Asnjërën nga këto nuk e kemi provuar.

## 17. Qeliza e kodit 11 — a ndryshon historia kur ndryshon grupi?

Krahasojmë normat e klasave në gjithë tabelën me normat te burrat e rinj. Pastaj cikli ndryshon kufirin e sipërm të moshës në 25, 30, 35 dhe 50 dhe printon sërish numëruesit dhe emëruesit. Një kontroll tjetër përsërit krahasimin familjar për 18–30, ndryshe nga H3 e regjistruar 18–50.

Ky është kontroll ndjeshmërie: **sa varet përfundimi nga përkufizimi i grupit?** Nuk kërkojmë fshehurazi intervalin që jep përfundimin më të bukur. Ruajmë rezultatin fillestar dhe i etiketojmë të tjerat si eksplorim.

Fakti që renditja e klasës 2 dhe 3 ndryshon në një nëngrup quhet këtu përmbysje renditjeje. Nuk pretendojmë automatikisht se kemi demonstruar kushtet e plota të paradoksit të Simpson-it.

## 18. Qeliza e kodit 12 — tri probleme të provuara me të dhëna

**Mosha:** grupojmë sipas klasës dhe seksit. `missing=lambda s: int(s.isna().sum())` përkufizon një funksion të vogël që numëron boshllëqet e grupit. `total='size'` numëron të gjithë rreshtat, përfshirë moshat bosh. `fraction_missing` është pjesa që mungon.

`pd.crosstab(..., normalize='index')` e kthen secilin rresht në përpjesëtime. Kjo tregon pjesën me moshë të njohur dhe të panjohur për secilin rezultat mbijetese. Ndryshimet e vëzhguara nuk provojnë pse mungojnë moshat; veçanërisht nuk mjaftojnë për të deklaruar një mekanizëm të caktuar MAR ose MNAR.

**Kabina:** e njëjta ide sipas klasës. Klasës 1 i mungojnë 40/216 kabina (18.5%); klasës 2, 168/184 (91.3%); klasës 3, 479/491 (97.6%). Mungesa nuk është e krahasueshme ndërmjet klasave.

**Grupet e vogla:** shfaqim madhësitë dhe intervalet Wilson. H2 ka vetëm 22 burra të klasës së parë, ndërsa grupi H3 me të afërm ka 33. Nuk trajtojmë të gjitha përqindjet si njësoj të sakta.

## 19. Qeliza e kodit 13 — vizualizimi i mungesave

Këtu vizatohen dy grafikë: përqindja e moshave që mungojnë sipas klasës dhe përqindja e kabinave që mungojnë sipas klasës. `apply(lambda s: 100 * s.isna().mean())` llogarit përqindjen për secilin grup.

Boshti vertikal **nuk është norma e mbijetesës**, por përqindja e të dhënave të munguara. Një shtyllë më e lartë do të thotë më pak informacion të regjistruar për atë kolonë. Grafikët e notebook-ut mund të jenë më shumë se tre; kërkesa për saktësisht tre grafikë zbatohet te posteri.

## 20. Përfundimi — çfarë mund të thuash me siguri?

Mund të thuash: **“Në kampionin tonë, 10 nga 86 pasagjerë të profilit të Jack-ut mbijetuan. H1 dhe H2 përputhen me drejtimet e pritura, kurse H3 jo. Rezultatet ndryshojnë sipas përkufizimit të grupit, dhe nuk provojnë se një ndryshim i vetëm do ta shpëtonte Jack-un.”**

Nuk duhet të thuash: “Jack-u kishte saktësisht 11.6% shans”, “klasa e parë do ta kishte shpëtuar”, “familja ul shanset” ose “kemi trajnuar një model”. Këto e tejkalojnë analizën.

**Lidhje nuk është shkakësi.** Klasa e biletës mund të bashkëshoqërohet me moshën, seksin, vendndodhjen dhe rrethana të tjera. Ne nuk kemi vendosur rastësisht njerëz në klasa dhe nuk kemi regjistruar aksesin individual në varka apo kohën e evakuimit.

## 21. Si lidhen notebook-u, posteri dhe faqja?

`src/analysis.py` përmban filtrat dhe llogaritjet e përbashkëta. `src/build_notebook.py` krijon përmbajtjen e notebook-ut. `src/build_exhibit.py` e bën të përdorshëm më vete, e ekzekuton dhe prodhon të dhënat e faqes. `src/make_poster.py` prodhon posterin. `src/publish_story.py` shton faqen e historisë dhe përmbledhjet e veçorive. `src/document_methods.py` shton sqarimet dhe këtë udhëzues, pa ndryshuar qelizat llogaritëse.

Faqja ka 54 kombinime: 2 kategori seksi × 3 klasa × 3 dritare moshe × 3 zgjedhje për të afërmit. Ajo afishon përmbledhje të llogaritura, jo një model që mëson. Paneli i porteve dhe disa përmbledhje të veçorive janë eksplorim shtesë i faqes; mos i paraqit si hipoteza origjinale të notebook-ut.

Testet automatike kontrollojnë numrat, grupet, skedarin origjinal, notebook-un dhe lidhjet. Kalimi i testeve tregon se këto kontrolle funksionuan, jo se profesori e ka vlerësuar projektin ose se të gjitha pretendimet historike janë provuar.

## 22. Provoje vetë pa e mësuar përmendësh

Pas ekzekutimit të qelizës së parë, provo:

```python
print(df.shape)
print(df['Survived'].sum())
print(df['Age'].isna().sum())
```

Duhet të shohësh `(891, 12)`, `342` dhe `177`. Pastaj shkruaj vetë filtrin e Jack-ut dhe llogarit `len`, `sum` dhe `mean`. Para ekzekutimit, shpjego me një fjali çfarë pret të numërojë secili.

Ndrysho vetëm kufirin e sipërm në 30. Tani grupi është tjetër: 130 burra të klasës së tretë, 19 të mbijetuar. Mos thuaj që ndryshoi shansi i të njëjtëve 86 njerëz; ti ndryshove njerëzit që përfshihen.

Për vetëkontroll: a mund të shpjegosh pse `mean()` jep normën, pse një moshë bosh nuk plotësohet automatikisht, pse H3 nuk u mbështet, dhe pse 40.9% − 14.6% është diferencë në pikë përqindjeje? Këto përgjigje vlejnë më shumë se memorizimi i gjithë kodit.

## Burimet për të kontrolluar shpjegimin

Përmbajtja dhe numrat vijnë nga [notebook-u i projektit](notebook.html), skedari i pandryshuar `train.csv`, [evidence.json](evidence.json) dhe [commit-i i hipotezave](https://github.com/elonaelon000/could-jack-have-survived/commit/7a423658689667bbf34772da22bb66c945d7ee90).

Sjellja e funksioneve mund të kontrollohet te dokumentacioni zyrtar: [pandas Series.between](https://pandas.pydata.org/docs/reference/api/pandas.Series.between.html), [pandas.cut](https://pandas.pydata.org/docs/reference/api/pandas.cut.html), [pandas GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html), [pandas describe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html), dhe [Matplotlib pyplot](https://matplotlib.org/stable/tutorials/pyplot.html).
