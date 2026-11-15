import { createRequire } from 'node:module';
import { writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
if (process.argv.length !== 4) throw new Error('Usage: node browser-smoke.mjs <output-root> <absolute-package.json-with-playwright>');
const require = createRequire(path.resolve(process.argv[3]));
const { chromium } = require('playwright');
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const root = path.resolve(process.argv[2]);
mkdirSync(`${root}/evidence`, { recursive: true });
const cases = [
 ['direct','outputs/direct/templates/airy-modern/template.html',8],
 ['selection','outputs/selection/templates/circuit-tech-dark/template.html',8],
 ['preview-circuit','outputs/selection/previews/circuit-tech-dark-preview.html',1],
 ['preview-executive','outputs/selection/previews/midnight-executive-preview.html',1]
];
const results = [];
try {
 for (const [name,file,count] of cases) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(`${root}/${file}`).href);
  await page.evaluate(()=>Promise.race([document.fonts.ready,new Promise(r=>setTimeout(r,3000))]));
  if(await page.locator('.slide').count()!==count) throw new Error(`${name}: slide count`);
  await page.screenshot({ path:`${root}/evidence/${name}.png` });
  if(count>1) {
   await page.keyboard.press('ArrowRight');
   await page.waitForTimeout(500);
   if(await page.locator('.slide.active').evaluate(el=>[...document.querySelectorAll('.slide')].indexOf(el))!==1)throw new Error(`${name}: next`);
   await page.screenshot({path:`${root}/evidence/${name}-agenda.png`});
   await page.keyboard.press('End');
   if(await page.locator('.slide.active').evaluate(el=>[...document.querySelectorAll('.slide')].indexOf(el))!==count-1)throw new Error(`${name}: End`);
   await page.keyboard.press('Home');
   if(await page.locator('.slide.active').evaluate(el=>[...document.querySelectorAll('.slide')].indexOf(el))!==0)throw new Error(`${name}: Home`);
  }
  if(errors.length)throw new Error(`${name}: ${errors}`);
  results.push({name,slideCount:count,pageErrors:errors,navigation:count>1?'ArrowRight, End, Home passed':'single-slide preview'});
  await page.close();
 }
 writeFileSync(`${root}/evidence/browser-results.json`,JSON.stringify(results,null,2)+'\n');
 console.log(JSON.stringify(results,null,2));
} finally { await browser.close(); }
