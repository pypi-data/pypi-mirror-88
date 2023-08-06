import os
import shutil
import click

from .settings import EXPORT_KUBECONFIG, ENVRC_FILENAME, KUBECONFIG_FILENAME


class BaseFile:
    filename = "filename"

    def __init__(self, directory):
        self.path = os.path.join(directory, self.filename)

    def exists(self):
        return os.path.isfile(self.path)


class EnvrcFile(BaseFile):
    filename = ENVRC_FILENAME

    def create(self):
        with open(self.path, 'w') as file:
            file.write('{export}\n'.format(export=EXPORT_KUBECONFIG))

    def __contains_export(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.strip().startswith('export KUBECONFIG='):
                return True
        return False

    def __append_export(self):
        with open(self.path, 'a') as file:
            file.write('\n{export}\n'.format(export=EXPORT_KUBECONFIG))

    def __replace_export(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.strip().startswith('export KUBECONFIG='):
                lines[i] = '{export}\n'.format(export=EXPORT_KUBECONFIG)
        with open(self.path, 'w') as f:
            f.writelines(lines)

    def replace_or_append_export(self):
        if self.__contains_export():
            self.__replace_export()
        else:
            self.__append_export()

    def allow(self):
        os.system('direnv allow {path}'.format(path=self.path))

    def process(self):
        if self.exists():
            click.echo('dirk: {path} does already exist.'.format(path=self.path))
            click.echo('dirk: process {path}.'.format(path=self.path))
            self.replace_or_append_export()
        else:
            click.echo('dirk: {path} does not exist.'.format(path=self.path))
            click.echo('dirk: create {path}.'.format(path=self.path))
            self.create()
        click.echo('dirk: direnv allow {path}.'.format(path=self.path))
        self.allow()


class KubeconfigFile(BaseFile):
    filename = KUBECONFIG_FILENAME

    def create(self):
        open(self.path, 'a').close()

    def replace_by_configfile(self, configfile):
        shutil.copyfile(configfile, self.path)

    def replace_by_emptyfile(self):
        open(self.path, 'w').close()

    def set_mode(self):
        os.chmod(self.path, 0o600)

    def process(self, configfile, mode):
        if self.exists():
            click.echo('dirk: {path} does already exist'.format(path=self.path))
            if mode == 'skip':
                if configfile:
                    click.echo('dirk: skip writing {file} to existing kubeconfig.'.format(file=configfile))
                else:
                    click.echo('dirk: skip writing empty file to existing kubeconfig.'.format(file=configfile))
            if mode == 'replace':
                if configfile:
                    click.echo('dirk: replace existing kubeconfig by {file}.'.format(file=configfile))
                    self.replace_by_configfile(configfile)
                else:
                    click.echo('dirk: replace existing kubeconfig by empty file.'.format(file=configfile))
                    self.replace_by_emptyfile()
                self.set_mode()
        else:
            click.echo('dirk: {path} does not exist.'.format(path=self.path))
            if configfile:
                click.echo('dirk: write {file} to kubeconfig.'.format(file=configfile))
                self.replace_by_configfile(configfile)
            else:
                click.echo('dirk: create empty {path}.'.format(path=self.path))
                self.create()
            self.set_mode()
