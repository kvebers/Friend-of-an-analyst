# Friend of an Analyst

## Demo

![Demo](./docs/giff_small.gif)

## How to get extension

1. Choose the type of test device you need:
2. Apps—Sign in to your Google Account on a Chrome device.
3. Extensions—Sign in to your Google Account on a Chrome device or Chrome browser on a Windows, Mac, or Linux computer.
4. Save the app or extension folder on your test device.
5. Go to chrome://extensions/.
6. At the top right, turn on Developer mode.
7. Click Load unpacked.
8. Find and select the app or extension folder.
9. Open a new tab in Chromeand thenclick Appsand thenclick the app or extension. Make sure it loads and works correctly.
10. If needed, make changes in the manifest.json file, host the app folder, and retest it. Repeat until the app or extension works correctly.

## How to run backend

You need Docker, and everything else should be fine. Should also work without .env setup time +- 10 minutes

```
make
```

or

```
docker-compose --build
docker-compose up
```


## Notes

Our Extension is super rought right now there are only select videos that are elevated as true, for example: https://www.youtube.com/watch?v=Y8Yx8J1YNng


## Tech Stack




## Purpose of the project

Why Youtube? Youtube usage by 2024 analytics: ~49 minutes a day is spent on Youtube per person; Every day - 1 billion hours has been watched on Youtube; more than 500 hours are uploaded every minute on Youtube.
Here’s the challenge we’re solving. So First: video platforms such as YouTube have become a major channel for disinformation and manipulation - including in defence, national security and operational environments. For example, research indicates the algorithmic dynamics on YouTube create filter bubbles, amplifying certain content. Second: volume and speed of content exceeds most human fact-checking capabilities. As one chart shows, YouTube has a “misinformation amplification factor” of ~6 above baseline.Third: The impact is real. False narratives can shape perceptions, degrade situational awareness, influence audiences, and complicate defence planning.So emotionally: imagine a tactical video arriving on YouTube claiming a false event, being shared hundreds of thousands of times - and your intelligence team only discovers it after it has spread. That gap is the risk we address.

Here’s how we respond. Friend of an Analyst is an AI-driven platform that: • Automatically ingests YouTube (and similar) videos, including live streams, analysing audio, visual and text content. • Identifies asserted claims with timestamps, clusters related claims across videos, and surfaces them in a timeline UI. • For each claim, it cross-references trusted databases and open sources to produce a ranked list of supporting or refuting evidence, and generates an auditable evidence-bundle.Two standout features: 1) Multimodal Claim Extraction & Timeline — extracts claims from audio, subtitles, scene OCR, and key frames, then anchors them in time and across videos. 2) Automated Evidence-Trace & Provenance Engine — for each claim we provide a confidence score, source ranking, downloadable “forensic brief” (PDF/JSON) for audit and integration into intelligence workflows.In other words: we bring speed, scale and operational readiness to video-based misinformation detection for defence contexts.