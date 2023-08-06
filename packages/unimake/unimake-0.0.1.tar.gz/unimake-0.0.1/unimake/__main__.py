"""Main entrypoint for console usage."""
import argparse
import os
import sys

# This is just a temporary module until unimatrix.ext.cli is implemented.


UNIMAKE_TEMPLATE_DIR = '.lib/templates'

def template(args):
    import jinja2
    from unimake.conf import settings
    env = jinja2.Environment(
        lstrip_blocks=True,
        trim_blocks=True,
        loader=jinja2.ChoiceLoader([
            jinja2.PackageLoader('unimake'),
            jinja2.FileSystemLoader(UNIMAKE_TEMPLATE_DIR)
        ])
    )
    ctx = {
        'env': dict(os.environ),
        'settings': settings,
        **{x: y for x, y in map(lambda x: str.split(x, '='), args.variables)}
    }
    t = env.get_template(args.src)
    output = t.render(**ctx)
    print(output)


parser = argparse.ArgumentParser(
    "Unimake",
    usage="unimake [subcommand] ..."
)
subparsers = parser.add_subparsers(
    title="subcommands",
    description="Available subcommands:"
)
template.parser = subparsers.add_parser('template')
template.parser.add_argument('src',
    help="path to a Jinja2 template.")
template.parser.add_argument('-f',
    help="write the output to this destination. If not provided, use stdout.",
    required=False,
    dest='dst'
)
template.parser.add_argument('-v',
    action='append',
    default=[],
    dest='variables'
)
template.parser.set_defaults(func=template)


def main():
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    sys.exit(main())
