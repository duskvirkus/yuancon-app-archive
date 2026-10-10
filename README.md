# Yuancon App Archive Script

(currently work in progress capture doesn't seem to function fully)

This project is meant to archive https://yuancon.app/ to perserve the app so controllers can continue full functionality if the site ever goes down.

Currently just the script to do it yourself however if the site ever goes down I may publish my own captures.

## Usage

```shell
./run.sh
```

You can serve the site by
```shell
cd capture/<capture-timestamp>/yuancon.app
python -m http.server
```