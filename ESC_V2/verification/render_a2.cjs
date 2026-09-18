const fs=require('fs'); const path=require('path');
const sharp=require('C:/Users/mrtgv/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
(async()=>{
 const dir=path.join(__dirname,'svg_a2');
 const selected=fs.readdirSync(dir).filter(n=>n==='ESC_3kW_A2.svg'||n.includes('Faz A')||n.includes('Gerilim')&&n.includes('DC')||n.includes('STM32')||n.includes('arıza'));
 for(let i=0;i<selected.length;i++){
  await sharp(path.join(dir,selected[i]),{density:150}).resize(2200).png().toFile(path.join(__dirname,'a2_preview_'+i+'.png'));
  process.stdout.write(i+' '+selected[i]+'\n');
 }
})();
