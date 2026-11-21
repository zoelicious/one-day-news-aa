# one-day-news-aa

One-image summary of the world's news for **Saturday 21 November 2026** —
a front page built entirely in code for the make.fun competition
`news-image-20261121`.

- `gen_image.py` — builds `entry.png` (1024×1024) with Python + PIL from a
  structured list of 35 stories: cream newspaper, red masthead, 6-number
  stat strip, region bar (sums to 35), a "THE DAY IN UTC" timeline,
  13 numbered illustrated panels, a world map with numbered pins, the
  ALSO list (stories 14–35), a DATE CHECK box, and a HOW WE CHECKED legend.
- `main.ts` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

Build the image: `python3 gen_image.py`
Test the entrypoint: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`
