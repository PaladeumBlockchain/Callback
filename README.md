# Callback

Callback service is used to get reply from mobile wallet back to web serive.

## Setup

Systemd example:

```
[Unit]
Description=Gunicorn instance to serve callback example
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/callback
Environment="PATH=/home/user/callback/venv/bin"
ExecStart=/home/user/callback/venv/bin/gunicorn app:app --worker-class eventlet -w 1 --bind 0.0.0.0:9000 --reload

[Install]
WantedBy=multi-user.target
```

Nginx example:

```
server {
    server_name callback.codepillow.io;
    listen 80;

    location / {
        proxy_pass http://localhost:9000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /socket.io {
        include proxy_params;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://localhost:9000/socket.io;
    }
}
```
