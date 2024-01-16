ForwardFlex
===

CLI for managing ssh forwarded ports.

# Installation

Requirements: python >= 3.8

## MacOS

```shell
git clone https://github.com/Marik28/fflex
cd fflex
chmod +x fflex.py
cp fflex.py ~/.local/bin/fflex
```

# Usage

Firstly you need to edit your `~/.config/fflex.json` and add some services like this:

```json
// ~/.config/fflex.json
{
  "test": {
    "my-service": "ssh -L 9999:localhost:5432 mytesthost"
  },
  "prod": {
    "my-service": "ssh -L 9998:localhost:5432 myprodhost"
  }
}
```

List your services

```shell
fflex list
## Output:
## test:
##   my-service:  "ssh -L 9999:localhost:5432 mytesthost"
## prod:
##   my-service:  "ssh -L 9998:localhost:5432 myprodhost"
```

Start port-forwarding for a service. By default, test environment will be selected

```shell
fflex start my-service
# Output
# running "ssh -L 9999:localhost:5432 mytesthost" (test environment)
```

For more info, refer to command help

```shell
fflex --help
```
