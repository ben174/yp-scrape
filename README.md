# Ben's YP Scraper

# Start a scrapyd instance:

### run scrapyd in a container

    docker run -d -p 6800:6800 --name=scrapyd vimagick/scrapyd

### deploy to the container

    scrapyd-deploy docker

### build the webapp

    docker build -t yp-scrape .

### run the webapp, liking to scrapyd

    docker run -d -p 8495:8495 --name yp-scrape --link=scrapyd yp-scrape

### navigate to the webapp in yoru browser:

    http://localhost:8495
