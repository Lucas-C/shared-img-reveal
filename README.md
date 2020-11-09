Online demo at: <https://chezsoi.org/lucas/shared-img-reveal/>

**Usage**: the [GM](https://en.wikipedia.org/wiki/Gamemaster) creates a table, and share the public URL with players.
The portions of the image seen by the other players can then be controlled the GM by clicking the hatched zones.

<!-- TODO: add mention of Run.Die.Repeat scenario -->

# Resources used
## JS libs
To display `textarea` line numbers: [MatheusAvellar/textarea-line-numbers](https://github.com/MatheusAvellar/textarea-line-numbers) (served by the app).

## Demo images
From those Adventure Time flickr albums, all illustrations [CC BY-NC-ND 2.0](https://creativecommons.org/licenses/by-nc-nd/2.0/) :
- [Adventure Time Backgrounds, Season One](https://www.flickr.com/photos/84568447@N00/albums/72157616038185579)
- [Adventure Time Characters](https://www.flickr.com/photos/84568447@N00/albums/72157615075682469)

# Installation

## Local launch

    pip install -r requirements.txt
    FLASK_ENV=development ./sir_app.py

## systemd service

    $ pew new shared-img-reveal -p python3 -r requirements.txt
    $ cat /etc/systemd/system/shared-img-reveal.service
    [Service]
    WorkingDirectory=/path/to/parent/dir
    ExecStart=/usr/local/bin/pew in shared-img-reveal python -u sir_app.py
    Restart=always

## nginx configuration

    location /shared-img-reveal {
        include uwsgi_params;
        rewrite ^/shared-img-reveal/?(.*)$ /$1 break;
        proxy_pass http://127.0.0.1:8086;
    }
