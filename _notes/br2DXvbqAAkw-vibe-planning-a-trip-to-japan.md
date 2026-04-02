---
layout: post
title: "vibe-planning a trip to Japan"
date: 2026-04-01 23:19 -0700
permalink: /br2DXvbqAAkw/vibe-planning-a-trip-to-japan
redirect_from:
  - /br2DXvbqAAkw
tags: [inkhaven, travel, personal, recommended, japan]
---

Yesterday I arrived at Inkhaven from my most thoroughly planned trip ever: a 3 week trip to Japan. My highlights from the trip were: attending Idolm@ster Million Live! 11th Live 百合咲く誇るレムリア, a couple of action-packed days hiking the Nakasendo + seeing Matsumoto castle/Lake Suwa, an overnight bikepacking trip from Fujiyoshida to Minobu with an stunning view of Mount Fuji from my campsite, and a memorable dinner at a tiny home restaurant in Shuzenji after seeing at least 8 waterfalls on the Izu peninsula.
![Mount Fuji reflected in Lake Motosu from Kouan campground](</images/br2DXvbqAAkw-IMG_4300.jpeg>)

A few years ago, I wouldn't have been able to plan such a trip. On my first trip to Japan, I hadn't even booked a hotel for my first night in Tokyo before my plane landed. I enjoy the spontaneity afforded by last minute planning, but mostly that trip was a product of my laziness/procrastination. The last minute planning led to days with more time spent researching than actually doing things plus significant stress from making same-day hotel bookings while on the train in the afternoon.

A couple of things have changed since that last trip. I've traveled a lot more: that trip to Japan was both my first trip to Japan and my first time solo traveling. More importantly, since mid-2025 I've been using Claude Code to do increasingly larger programming tasks. At first it was mostly useful for making relatively easy changes in the context of a robust test suite, but now it is quite useful for spec-ing out features and planning work too.

Time to plan my trip in March felt very limited: I was leaving my job to start a gap year, applying to Inkhaven, planning my birthday party, pursuing a crush, and focusing on spending more time with friends. While chatting with Claude about my anxiety and stress from all the things I had going on, I laid out that I hadn't planned anything but a rough itinerary:
- I would stay in Fukuoka/Kitakyushu for the first couple of nights after my flight landed + for the live show, and didn't really know if there was anything I wanted to see in Kitakyushu other than the live show
- I wanted to spend some more time in Hiroshima and see Miyajima having previously only overnighted there
- I wanted to spend some time in Nara having missed it on my first trip to Kyoto
- Inspired by watching Yuru Camp I wanted to go through the mountains in the Kiso valley/Nagano/Yamanashi, hike, stop at interesting hot springs, possibly climb Mount Fuji, and maybe camp
- Spend some time in Tokyo, see cherry blossoms at peak bloom, do some shopping, and maybe take a day trip
- Finally I had a multi-day layover in Taiwan/Taipei and didn't really have any idea what to do there[^taiwan]

[^taiwan]: Taiwan ended up getting cut because I got into Inkhaven! Partially because I thought I might get into Inkhaven, I'd procrastinated booking/planning Taiwan in detail.

I often get stuck at a rough itinerary because figuring out details to the level of booking accommodations for specific nights causes cascading changes. Waiting till the last minute prevents ever needing to change or cancel plans you spent time working on. By the time you plan something you're already executing on it. Irrationally, this makes it easy for me to procrastinate work at this stage. Since any work I do might need to be thrown away, why start it at all?

Claude took my rough itinerary and immediately started poking holes into it: Mount Fuji wouldn't be climbable in March, camping with a hammock in March would be far too cold. I checked some alternatives with Claude: perhaps I could spend some time on the Izu peninsula instead of hiking Fuji, maybe I could rent camping gear suitable for camping in March.

I had Claude summarize our trip planning into a markdown document so I could start to nail down details and have a single source of truth to iterate on. Since OpenAI's o3 in early 2025, I've found LLMs using web search more useful than the likes of Tripadvisor for giving personalized recommendations. Now, combined with the longer time-horizon capabilities of coding agents, Claude Code & Cowork were able to break up that markdown file and research, producing detailed itineraries for individual segments.

This medium level of resolution before booking specific hotels/accommodations was particularly critical for the camping/biking segment of the trip. Knowing that there were at best limited buses in the Fuji 5 Lakes area, I had Claude evaluate busing vs biking to the campsite. Claude found a bike rental company that was willing to do 1-way rentals and found a good 40km bike route to Kouan campground at Motosuko. After confirming details of the bike and camping gear reservations, this turned into my favorite portion of the trip: the bikepacking segment with a view of Mount Fuji.

Once I had a mostly finished plan it was also possible to ask Claude to do things like go through the entire itinerary and add vegetarian food recommendations. On my first trip, finding food that I was happy to eat continually brought me stress, so I ended up settling for sushi or meat more often than I'm really comfortable with. Having a bird's-eye view of where it would be easier/harder to find vegetarian food made it easier to holistically plan where to be less strict. Overall, this left me more satisfied with my food choices than when choosing in the moment. I was also pleased Claude found Kakurinbo, a touristy but nice Buddhist temple stay in Minobu, with a completely vegetarian dinner/breakfast menu.

With the medium level itinerary complete, I was also able to verify that everything made sense / was possible. One thing I noticed at this stage was that Claude had created the itinerary starting from the 12th, but the 12th was the day that I was flying to Japan, and I didn't actually arrive in Japan till the 14th due to time zone shenanigans. Claude didn't catch this mistake, but also made it easy to prioritize which activities were the easiest to cut, rejiggering dates to make everything fit with two fewer available days.

Eventually the plan was ready enough to start booking things. The closest thing to a planning failure was mostly caused by me. Claude had warned me that accommodations in the Kiso valley would be limited. But because it was right before the biking/camping segment, which required confirming gear/bike/campsite reservations, I waited to book my stays in case I needed to change plans. I ended up being stuck with a remote mountaintop resort, which, while beautiful, required taking a bus followed by a 3km hike on a day where I already had hiked ~11.5km of the Nakasendo from Magome to Nagiso station.

The result was one of the most action-packed, stress-free trips I've ever gone on. I've also been able to enjoy the benefits of planning further in advance on group trips where communication forces more eager planning. For solo travel though, this was a first: the reduced planning friction let me overcome my laziness.
