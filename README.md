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
