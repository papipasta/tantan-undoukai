const fs=require('fs'), vm=require('vm');
const L=fs.readFileSync(process.argv[2],'utf8').split('\n');
const man=L[607].replace(/^[^{]*/,'').replace(/<\/script>.*$/,'');
const code=L.slice(1070,1365).join('\n');   // line 1071..1365 (M は下で用意)
const STUB=new Proxy(function(){},{get:(t,k)=>k===Symbol.toPrimitive?()=>0:STUB,set:()=>true,apply:()=>STUB,construct:()=>STUB});
function run(iso){
  const RD=Date; class FD extends RD{constructor(...a){super(...(a.length?a:[iso]))} static now(){return new RD(iso).getTime()}}
  const ctx={Date:FD,Math,JSON,console,Set,Map,Object,Array,String,Number,document:{getElementById:()=>({textContent:man}),createElement:()=>STUB}};
  vm.createContext(ctx);
  vm.runInContext('const M=JSON.parse(document.getElementById("manifest").textContent);'+code+';this.MKG=MKG;',ctx);
  return ctx.MKG;
}
const names=['こうき','たぬき','パピィー','あずき','さくら','Tom','もち','ぽん'];
const nov=run('2026-11-17T12:00:00Z'), jan=run('2027-01-10T12:00:00Z');
console.log('season nov=',nov.SEASON&&nov.SEASON.id,' jan=',jan.SEASON);
let diffOld=0,diffNew=0;
for(const n of names){ const s=nov.nameSeed(n);
  const a=JSON.stringify(nov.generate(s,false).col), b=JSON.stringify(jan.generate(s,false).col);
  const c=JSON.stringify(nov.generate(s,false,true).col), d=JSON.stringify(jan.generate(s,false,true).col);
  const ds=JSON.stringify(nov.generate(s,false,true).sel)===JSON.stringify(jan.generate(s,false,true).sel);
  if(a!==b) diffOld++; if(c!==d||!ds) diffNew++; }
console.log('季節あり(旧)で色が変わる名前:',diffOld,'/',names.length,' 季節なし(新)で変わる名前:',diffNew);
