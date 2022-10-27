# Lil' Johnny Checkup

> This Software is in Beta

*An API for performing health checks on remote endpoints.*


## About

Lil' Johnny Checkup is a simple API that allows clients to check the health status of a remote HTTP/HTTPS service. Johnny can optionally verify TLS/SSL certificates as well as report request duration, certificate validity duration, and other metrics.

Lil' Johnny Checkup is 100% ready to go in your production setup. Simply follow the instructions below and use with **very minimal configuration**.


## Usage

Johnny is Docker-ready. If you have Docker-Compose installed, then simply run the following:

```
$ cp Caddyfile.sample Caddyfile
# Don't forget to configure your new Caddyfile
$ docker-compose up -d
```

## API Documentation

To view the docs, simply run the app and go to `http://localhost/docs`.


## Options

For a list of all the supported options, please refer to `docker-compose.yml`.

- `HTTP_USERS`: A comma-separated list of `username:password` pairs that can be used to log in to the API.
- `LOG_LEVEL`: The level that the proxy will log.
- `LOG_LOCATION`: Where to store the logs. The defaulr value of '-' will log to stdout.


## Contributing

Pull Requests are welcome. I may not be the best at responding to feedback, but I'll do my best. Features that go out of scope will be rejected.

Please ensure all linting and testing passes before making your PR (use `./preflight` to be sure).

