# facebook-discord

A simple Discord bot that sends new Facebook posts to a channel.

## Setup

Copy `config.example.py` to `config.py` and fill in the values.
Use a cronjob to run `main.py` once a while.

## Docker

```yaml
services:
  app:
    image: ulysseszhan/facebook-discord:master
    container_name: facebook-discord
    restart: unless-stopped
    volumes:
      - ./data:/data
```

Put `config.py` in `./data`.

## License

MIT.
