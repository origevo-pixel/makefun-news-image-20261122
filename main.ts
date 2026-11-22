// THE WORLD IN ONE DAY — entry program for make.fun's
// "Sum up 22 November's world news in one image" bounty.
//
// The picture itself is entry.png beside this file: a 1024x1024
// front page of Sunday 22 November 2026 — Iran strikes Bahrain,
// Mexico captures 'El Chapo Isidro', COP31 stalls in Antalya, a
// drone hits a Russian ship in the Baltic, Wall Street's AI
// sell-off, plus an ALSO TODAY column (EU–Indonesia deal, Kryvyi
// Rih, UN autonomous-weapons draft, Alcaraz v Zverev). It was
// composed from five generated editorial panels with every word
// typeset programmatically (see build/compose.py and assets/), so
// the judge reads crisp text and the day's real stories.
//
// This program's whole job is to hand that picture in unchanged:
// copy entry.png to the output directory as entry.png. The gate
// accepts PNG or JPEG bytes (told apart by their first bytes) of
// at most 1 MiB and 1024x1024; the file here is JPEG, 1024x1024,
// and well under the cap, and I verify those facts before copying
// so a bad asset fails loudly instead of scoring zero.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in
// for /output:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024;
const sourcePath = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(sourcePath);

if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate cap`);
}
const isJpeg = bytes[0] === 0xff && bytes[1] === 0xd8;
const isPng = bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47;
if (!isJpeg && !isPng) {
  throw new Error('entry.png is neither JPEG nor PNG by its first bytes');
}

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(sourcePath, join(outputDir, 'entry.png'));
console.log(`entry.png handed in: ${bytes.length} bytes (${isJpeg ? 'JPEG' : 'PNG'})`);
