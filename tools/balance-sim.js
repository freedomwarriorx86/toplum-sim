// Denge simülasyonu: node tools/balance-sim.js "file://$PWD/index.html?demo" 2000
// Gerekenler: npm i puppeteer-core, sistemde /usr/bin/google-chrome. Her ilçe × oyuncu sayısı × yolsuzluk modu için görev kazanma oranlarını (%) basar.
// Kullanım: node tools/balance-sim.js <url> [oyun sayısı]. Satır anahtarı: tur|ilçe|oyuncu|mod.
const puppeteer=require('puppeteer-core');
const N=+process.argv[3]||3000;
(async()=>{
  const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',headless:'new',args:['--no-sandbox']});
  const p=await b.newPage();await p.goto(process.argv[2]);await new Promise(r=>setTimeout(r,500));
  const out=await p.evaluate((N,TR,SD)=>{SUSP_DECAY=+SD;
    const cards=DEMO_SEED.cards,missions=DEMO_SEED.missions,res={};
    const apply=(g,d,cor)=>{['health','education','security','transport','social'].forEach(k=>{if(d[k])g[k]=clamp(g[k]+d[k])});
      if(d.treasury)g.treasury+=d.treasury;if(d.businessman_cash)g.businessman_cash=Math.max(0,g.businessman_cash+d.businessman_cash);
      if(cor&&d.suspicion)g.suspicion=clamp(g.suspicion+d.suspicion)};
    const sh=a=>[...a].sort(()=>Math.random()-.5);
    for(const R of [5,8,12])for(const city of Object.keys(CITIES))for(const n of [2,4,6])for(const cor of [true,false]){
      const key=`${R}|${city}|${n}|${cor?'kor':'temiz'}`;const r=res[key]={games:0,end:{},ov:0,mw:{},mg:{}};
      S.corruption=cor;S.selectedCity=city;
      for(let it=0;it<N;it++){
        S.players=Array(n).fill({});S.rounds=R;const g={...CITIES[city].start,suspicion:0};const ms=sh(missions.filter(missionOk)).slice(0,n);const roles=sh(ROLES.map(x=>x.key)).slice(0,n);
        const pl=roles.map((role,i)=>({role,m:ms[i],ep:EP_START,cap:ROLES.find(x=>x.key===role).ep}));
        const deck=[...sh(cards),...sh(cards)];let played=0,end='Dönem sona erdi',k=R;
        outer:for(let t=0;t<k;t++)for(const P of pl){if(t>0&&P.lt!==t){P.lt=t;P.ep=Math.min(P.cap,P.ep+EP_GAIN)}
          const c=deck[played++%deck.length];const o=hasOpts(c)?botChoose(c,P.m):null;{S.selectedCity=city;const d=upkeep(deltasFor(c,o),randWear());apply(g,d,cor)}
          if(t>0&&!P.g){};P.g=0;if(Math.random()<.6){const opts=[...actionsFor(P.role)].sort(()=>Math.random()-.5).slice(0,OFFER_N).filter(a=>a.ep<=P.ep);if(opts.length){const a=opts[botChoose({options:opts.map(o=>({effects:o.fx,cost:o.fx.treasury||0}))},P.m)];if(missionGain(a.fx,P.m)>=0){P.ep-=a.ep;apply(g,a.fx,cor)}}}
          if(g.treasury<0){end='İflas';break outer}if(cor&&g.suspicion>=100){end='Soruşturma';break outer}
        }
        r.games++;r.end[end]=(r.end[end]||0)+1;r.ov+=overall(g);
        pl.forEach(P=>{r.mg[P.m.code]=(r.mg[P.m.code]||0)+1;if(missionWon(P.m,g))r.mw[P.m.code]=(r.mw[P.m.code]||0)+1});
      }
    }
    return res;
  },N,+(process.argv[4]||0.06),+(process.argv[5]||2));
  const byLen={};for(const[k,r]of Object.entries(out)){const L=k.split('|')[0];byLen[L]=byLen[L]||{};for(const c of Object.keys(r.mg)){byLen[L][c]=byLen[L][c]||[0,0];byLen[L][c][0]+=r.mw[c]||0;byLen[L][c][1]+=r.mg[c]}}
  const codes=[...new Set(Object.values(out).flatMap(r=>Object.keys(r.mg)))].sort();
  console.log('senaryo'.padEnd(24),'konfor','bitiş                        ',codes.join('  '));
  for(const[k,r]of Object.entries(out)){
    const end=Object.entries(r.end).map(([a,c])=>a.slice(0,5)+':'+Math.round(100*c/r.games)).join(' ');
    console.log(k.padEnd(24),String(Math.round(r.ov/r.games)).padEnd(6),end.padEnd(30),codes.map(c=>String(Math.round(100*(r.mw[c]||0)/(r.mg[c]||1))).padStart(3)).join('  '));
  }
  const tot={};for(const r of Object.values(out))for(const c of codes){tot[c]=tot[c]||[0,0];tot[c][0]+=r.mw[c]||0;tot[c][1]+=r.mg[c]||0}
  console.log('GENEL'.padEnd(62),codes.map(c=>String(Math.round(100*tot[c][0]/tot[c][1])).padStart(3)).join('  '));
  for(const[L,v]of Object.entries(byLen))console.log('TUR '+L,codes.map(c=>c+':'+Math.round(100*v[c][0]/v[c][1])).join(' '));
  await b.close();
})();
