#!/usr/bin/python3
import argparse
import json
import subprocess
import sys
import typing as t
from pathlib import Path

Config = t.Dict[str, t.Dict[str, str]]


def abort(msg: str = "Abort!", *, code: int = -1):
    print(msg, file=sys.stderr)
    return SystemExit(code)


CONFIG_FILE = Path("~/.config/fflex.json").expanduser()


def init_config(path: Path):
    with open(path, "w") as f:
        default_config: Config = {"test": {}, "prod": {}}
        json.dump(default_config, f, indent=2)


if not CONFIG_FILE.exists():
    CONFIG_FILE.touch(exist_ok=True)
    init_config(CONFIG_FILE)

with open(CONFIG_FILE) as f:
    config: Config = json.load(f)

parser = argparse.ArgumentParser(
    prog='forward',
    description='Configure ports forwarding with ssh',
)
subparsers = parser.add_subparsers(dest='command')
subparsers.add_parser("list", help="List available services")
start_command = subparsers.add_parser("start", help="Start forwarding port")
start_command.add_argument("service", help="service to run")
start_command.add_argument("--env", "-e",
                           help="environment of service. default: test",
                           choices=("test", "prod"),
                           default="test")


def list_services():
    for env, env_config in config.items():
        print(f"{env}:")

        for service, command in env_config.items():
            print(f'  {service}:  "{command}"')


def start_service(env: str, service: str):
    env_config = config[env]
    if service not in env_config:
        raise abort(f'service {service} not found')

    command = env_config[service]
    print(f'running "{command}" ({env} environment)')
    try:
        result = subprocess.run(command.split(" "))
    except KeyboardInterrupt:
        raise abort(f"KeyboardInterrupt, service {service} stopped")

    exit(result.returncode)


def main():
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        exit()

    elif args.command == "list":
        list_services()
        exit()

    elif args.command == "start":
        return start_service(args.env, args.service)

    else:
        raise abort(f"Unknown command: {args.command}")


if __name__ == '__main__':
    main()
