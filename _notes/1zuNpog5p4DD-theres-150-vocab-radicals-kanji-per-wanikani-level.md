---
layout: post
title: "There's ~150 vocab/radicals/kanji per WaniKani level"
date: 2025-12-22 14:32 -0500
permalink: /1zuNpog5p4DD/theres-150-vocab-radicals-kanji-per-wanikani-level
redirect_from:
  - /1zuNpog5p4DD
  - /de14645c
  - /de14645c/theres-150-vocab-radicals-kanji-per-wanikani-level
tags: [japanese, jq]
---

After my first trip to Japan in October of 2023 I started using WaniKani. After a few months, in February, it had stopped being easy because I was starting to actually learn new vocabulary rather than mostly reviewing vocabulary that I already knew. I was spending 30-60 minutes a day on reviews and wanted to know what I was getting myself into longer term. I also was curious what it would actually take to get to level 60 and learn all ~2000 kanji/6000 vocab items in just over a year as advertised by leveling up roughly once a week.

It's easy to use the WaniKani API to fetch json files for all of the levels:
```bash
for level in {1..60}; do
  curl "https://api.wanikani.com/v2/subjects?levels=$level" \
    -H 'Wanikani-Revision: 20170710' \
    -H 'Authorization: Bearer <wanikani readonly token here>' \
    >"$level.json"
done
```

Each of these is a json object like:
```json
{
  "object": "collection",
  "url": "https://api.wanikani.com/v2/subjects?levels=21",
  "pages": {"per_page": 1000, "next_url": null, "previous_url": null},
  "total_count": 155,
  "data_updated_at": "2024-01-31T11:54:21.208925Z",
  "data": [
    {
      "id": 148,
      "object": "radical",
      "url": "https://api.wanikani.com/v2/subjects/148",
      "data_updated_at": "2023-09-26T22:33:09.343743Z",
      "data": { /* detailed data */ }
    }
  ]
}

```
This can easily be post processed with `jq`:
```bash
zmv '(?).json' '0$1.json'
for i in {01..60}; do jq '.data|length' "$i.json"; done | jq --slurp 'add / length'
```

This gives an average of 154.35 items per level, aggregating radicals, kanji, and vocabulary.

Each item needs to be reviewed at least 4 times if you always get it correct to get to Guru, plus more if you get them wrong sometimes. This means that just for the new items for your current level you have ~600 reviews to do per week, which is \~100 per day. If you add to that reviews for Guru/Master/Enlightened level items the review workload approaches \~200 per day. That probably takes ~60 minutes to complete, which is a fairly large time commitment per day.
