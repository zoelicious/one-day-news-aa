// one-day-news-aa: deliver the built front page to the output directory.
// The newspaper image itself is produced by gen_image.py (Python + PIL);
// this program only copies the finished entry.png into place.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set");
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync("entry.png", join(outDir, "entry.png"));
console.log("entry.png written to " + outDir + " (" + statSync("entry.png").size + " bytes)");
