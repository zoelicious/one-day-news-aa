// one-day-news-aa: deliver the built front page to the output directory.
// The newspaper image itself is produced by gen_image.py (Python + PIL);
// this program only copies the finished entry.png into place.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = new URL("./entry.png", import.meta.url);
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
console.log("entry.png written to " + outDir + " (" + statSync(dest).size + " bytes)");
