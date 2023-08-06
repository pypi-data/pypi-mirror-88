import json
import os
import re
import pwd
import getpass

from .app import App, ConfigFile


def get_username():
    try:
        return pwd.getpwuid( os.getuid())[0]
    except Exception as e:
        return None


def main(args):
    path = os.path.expanduser('~/.secrethub')
    username = get_username()
    command = args.which

    if command == 'auth':
        token = getpass.getpass('Token:')
        ConfigFile.generate(path, token)
    elif command == 'read':
        app = App(path)
        secrets = app.read(args.name, user_app=username)
        if args.output is None:
            for secret in secrets:
                value = secret.get('value').encode('unicode_escape').decode('utf-8')
                print(f"{secret.get('name')}={value}")
        elif args.output == 'json':
            for secret in secrets:
                print(json.dumps(secret))
    elif command == 'write':
        app = App(path)
        app.write(args.name, args.value, user_app=username)
    elif command == 'inject' or command == 'printenv':
        app = App(path)

        with open(args.i) as f:
            template = f.read()

        def extract(x):
            name = x.replace("{{", '').replace('}}', '').strip()
            secrets = app.read(name, user_app=username)
            return (x, "".join(name.split('/')[2:]).upper().replace('-', '_'), secrets[0].get('value'))

        variables = [extract(x) for x in re.findall('{{.*}}', template)]

        if command == 'printenv':
            for _, key, value in variables:
                print(f"export {key}=\"{value}\"")
        else:
            for key, _, value in variables:
                template = template.replace(key, value)
            with open(args.o, 'w') as writer:
                writer.write(template)
