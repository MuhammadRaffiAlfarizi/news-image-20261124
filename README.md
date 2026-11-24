# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/MuhammadRaffiAlfarizi/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/MuhammadRaffiAlfarizi/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page in one image that sums up Tuesday 24 November 2026's world news: NATO vows to defend space, a Russian strike on Zaporizhzhia, a US drone helping catch El Chapo Isidro, a 5.6 quake in Nepal, and 33 more stories across 9 regions, with a UTC timeline, a day-in-numbers panel, a pin map, and a date check that proves every story is from 24 November (UTC).

## Run it

```sh
python3 main.py
```

That writes the image to `/output/entry.png` (1024x1024 PNG, under 1 MiB). Running it twice writes the same bytes both times.

## Layout

- `entry.png`, the image: a 1024x1024 PNG of the day's world news.
- `main.py`, the entry program: copies `entry.png` to `/output/entry.png`.
- `render.py`, the build-time script that drew `entry.png` with Pillow (no network, no randomness, no clock, re-running it reproduces the same image).

News as reported on 24 November 2026. Every figure in the image was checked against news reporting of the day: the Zaporizhzhia toll (Reuters, updated by the regional governor), the Nepal quake (Nepal's NEMRC and USGS), the NATO space vow (NATO chief Rutte), the El Chapo Isidro capture (Mexican officials), and the 181 by Priyansh Arya (PTI). Stories from earlier days, such as the COP31 collapse, the ICJ Myanmar ruling and the Benghazi ship strikes, are listed in the image's date check as deliberately left out.

---

<sub>Entered on [make.fun](https://make.fun/?ref=g3mwmsqn&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
