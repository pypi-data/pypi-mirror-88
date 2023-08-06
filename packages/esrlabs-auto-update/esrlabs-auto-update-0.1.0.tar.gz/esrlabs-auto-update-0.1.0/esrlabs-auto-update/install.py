import click
import os
import shutil

TOOLS_DIR = 'esrlabs-tools'
TOPDIR = os.path.dirname(os.path.abspath(__file__))

@click.command()
@click.option(
    '--install-dir',
    type=click.Path(exists=True),
    help='File path in which all esrlabs tools will be installed.'
    'If not provided, a prompt will allow you to type the input text.'
)
def main(install_dir):
    if not install_dir:
        install_dir = click.prompt('Enter a install dir', type=click.Path(
            exists=True))

    tools_path = os.path.join(install_dir, TOOLS_DIR)

    # copy itself
    updater_install_path = os.path.join(tools_path, 'esrlabs-auto-update')
    os.makedirs(updater_install_path, exist_ok=True)
    shutil.copytree(TOPDIR, updater_install_path, dirs_exist_ok=True)

    execfile(os.path.join(updater_install_path, 'esrlabs-auto-update.py'))


if __name__ == '__main__':
    main()
