// GTA 6 meme entry for make.fun (gta6-meme-x-01): the entry is the X post
// itself. This program copies POST.json from the repository root into
// $MAKEFUN_OUTPUT_DIR, where the house reads it and builds the dossier
// from the post (its first picture and its text) for the judge. Nothing
// this program writes is judged.
//
// POST.json holds a placeholder address until the meme is posted on X;
// replace it with the real post address before submitting, or the gate
// refuses the entry.
//
// Run locally as:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const source = join(BOT_DIR, "POST.json");
const target = join(OUTPUT_DIR, "POST.json");

mkdirSync(OUTPUT_DIR, { recursive: true });

let raw: string;
try {
  raw = readFileSync(source, "utf8");
} catch (err) {
  console.error(`cannot read ${source}: ${(err as Error).message}`);
  process.exit(1);
}

let post: unknown;
try {
  post = JSON.parse(raw);
} catch {
  console.error("POST.json is not valid JSON");
  process.exit(1);
}

if (
  typeof post !== "object" ||
  post === null ||
  typeof (post as { url?: unknown }).url !== "string"
) {
  console.error('POST.json must be an object with a string "url"');
  process.exit(1);
}

copyFileSync(source, target);

// Read-back self-check: what landed in /output must be byte for byte what
// the repository holds. A silent short write would hand the gate a broken
// POST.json, so refuse loudly instead of exiting 0 on a mismatch.
const written = readFileSync(target, "utf8");
if (written !== raw) {
  console.error(`POST.json mismatch after copy to ${target}`);
  process.exit(1);
}

console.log(`POST.json copied to ${target} (verified ${raw.length} bytes)`);
