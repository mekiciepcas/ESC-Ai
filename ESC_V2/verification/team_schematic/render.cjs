const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/mrtgv/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
(async()=>{
 const dir=path.join(__dirname,'svg');
 for(const [label,match] of [['phase',n=>n.includes('Faz A')],['bulk',n=>n.includes('DC bara _')],['inductor',n=>n.includes('DC bara')&&n.includes('12')&&!n.includes('devam')]]){
 const name=fs.readdirSync(dir).find(match);
 if(name)await sharp(path.join(dir,name),{density:200}).resize(2600).png().toFile(path.join(__dirname,label+'.png'));
 }
})();
