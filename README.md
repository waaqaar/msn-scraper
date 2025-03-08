# MSN News Feed Scraper

## Overview
This Python module **scrapes the MSN News Feed**, retrieves **articles/videos/etc with the most likes**. It persists credentials for MSN news requests using **Playwright** and **requests** module.

It is fully **Dockerized** to ensure a consistent environment for execution.

---

## Features
- **Intercepts MSN News Feed requests** to extract authentication credentials.
- **Scrapes news articles** and finds the one with the most likes.
- **Supports filtering** by article type (`all`, `article`, `video`, `webcontent` etc.).
- **Runs in a Docker container** to avoid dependency issues.
- **Handles automatic refreshing of the credentials** if they are expired.

---

## Installation (Dockerized Setup)
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/waaqaar/msn-scraper.git
cd msn-scraper
```
### 2️⃣ Build & Start the Docker Container
```sh
docker-compose up --build
```

### 3️⃣ Access the Container Shell
```sh
# SSH into docker container
$ docker exec -it playwright_scraper bash
```

### Usage
Run the scraper Inside the docker container
```sh
$ python scraper.py --max-scans 100 --only-type article
```

#### Arguments
| Argument      | Description                                       | Default |
|--------------|-------------------------------------------------|---------|
| `--max-scans` | Maximum number of results to scan              | `120`   |
| `--only-type` | Filter results by type (`all`, `article`, `video`, `webcontent`) | `"all"` |

#### Sample Output
```sh
# Sample output when you run the Scraper inside the docker container
$ python scraper.py --max-scans 100 --only-type article

Scanning progress: 0.0 %  [ Most likes so far: 1895, URL: https://www.msn.com/en-us/travel/../ ]
Scanning progress: 24.0 %  [ Most likes so far: 1895, URL: https://www.msn.com/en-us/travel/../ ]
Scanning progress: 48.0 %  [ Most likes so far: 1895, URL: https://www.msn.com/en-us/travel/../ ]
Scanning progress: 72.0 %  [ Most likes so far: 1895, URL: https://www.msn.com/en-us/travel/../ ]
Scanning progress: 96.0 %  [ Most likes so far: 1895, URL: https://www.msn.com/en-us/travel/../ ]
Scanning progress: 100.0 %  [ Most likes so far: 1895, URL: https://www.msn.com/en-us/travel/../ ]

The 'type=article' result with most likes in top 100 results is:
 {
    "id": "AA1oIRiY",
    "type": "article",
    "category": "travel",
    "title": "The 'origins of Atlantis' discovered off the coast of Lanzarote",
    "abstract": "Ancient islands, some of which still have their beaches intact, have been discovered deep in the Atlantic Ocean. The find is so significant that experts are hailing the landmasses as the potential inspiration for one of history\u2019s greatest myths. \"This could be the origin of the Atlantis legend,\" Luis Somoza, who was involved in the investigation, t...",
    "url": "https://www.msn.com/en-us/travel/tripideas/the-origins-of-atlantis-discovered-off-the-coast-of-lanzarote/ar-AA1oIRiY",
    "provider": {
        "id": "AAjaKBr",
        "name": "Indy 100",
        "logoUrl": "https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AAT0qC2.img",
        "profileId": "vid-dimwcdph69ytjebqqy5ii4c6inuda488dqc78hv632pkmax0xs7a",
        "largeFaviconUrl": "https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AAT04RR.img"
    }
}

Total likes:
 1895
```

## Troubleshooting
- No results found? Increase `--max-scans` to scan through more results.
