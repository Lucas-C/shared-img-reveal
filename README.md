Online demo at: <https://chezsoi.org/lucas/shared-img-reveal/>

# Images sources
## Adventure Time
From those flickr albums, all illustrations CC BY-NC-ND 2.0 :
- [Adventure Time Backgrounds, Season One](https://www.flickr.com/photos/84568447@N00/albums/72157616038185579)
- [Adventure Time Characters](https://www.flickr.com/photos/84568447@N00/albums/72157615075682469)

# Installation

    pip install flask

## Local launch

    FLASK_ENV=development ./sir_app.py

## nginx configuration

    location /lucas/shared-img-reveal {
        include uwsgi_params;
        rewrite ^/lucas/shared-img-reveal/?(.*)$ /$1 break;
        proxy_pass http://127.0.0.1:8086;
    }

## systemd service

    $ pew new shared-img-reveal -p python3 -i flask
    $ cat /etc/systemd/system/shared-img-reveal.service
    [Service]
    WorkingDirectory=/path/to/parent/dir
    ExecStart=/usr/local/bin/pew in shared-img-reveal python -u sir_app.py
    Restart=always
