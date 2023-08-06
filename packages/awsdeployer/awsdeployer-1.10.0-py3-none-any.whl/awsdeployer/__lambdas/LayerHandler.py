import boto3
import shutil
import subprocess

from awsdeployer.__util import *


class LayerHandler:
    def __init__(self, aws_config, layer_name, requirements_file, requirements_ignore, build_args, pre_build_command, post_build_command):
        self.aws = aws_config
        self.client = boto3.client('lambda',
                                   region_name=self.aws['region'],
                                   aws_access_key_id=self.aws['access_key'],
                                   aws_secret_access_key=self.aws['secret_key'])
        self.layer_name = layer_name
        self.requirements_file = requirements_file
        self.requirements_ignore = requirements_ignore
        self.build_args = build_args
        self.pre_build_command = pre_build_command
        self.post_build_command = post_build_command

    def __get_version_list(self):
        response = self.client.list_layer_versions(
            CompatibleRuntime=self.aws['runtime'],
            LayerName=self.layer_name
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise RuntimeError

        return response['LayerVersions']

    def __get_last_version(self, versions=None):
        if not versions:
            versions = self.__get_version_list()

        # check if layer does not exist
        if len(versions) == 0:
            return None

        max_version = versions[0]
        for version in versions:
            if version['Version'] > max_version['Version']:
                max_version = version

        return max_version['Version'], max_version['LayerVersionArn']

    def get_arn(self):
        return self.__get_last_version()[1] if self.__get_last_version() else None

    def cleanup_old_versions(self):
        versions = self.__get_version_list()
        latest_layer = self.__get_last_version(versions)[0]

        for layer_version in versions:
            if layer_version['Version'] != latest_layer:
                print('Delete layer {0}:{1}'.format(self.layer_name, layer_version['Version']))

                response = self.client.delete_layer_version(
                    LayerName=self.layer_name,
                    VersionNumber=layer_version['Version']
                )

                if response['ResponseMetadata']['HTTPStatusCode'] != 204:
                    raise RuntimeError

        print('Deleted old versions of layer {0}, latest is {1}'.format(self.layer_name, latest_layer))

    def compile_new_version(self):
        tmp_dir = 'tmp-' + random_string(32)

        if not self.aws['runtime'].startswith('python'):
            raise ValueError('Unsupported runtime')

        package_dir_name = 'python'

        os.mkdir(tmp_dir)
        os.mkdir(create_path(tmp_dir, package_dir_name))

        # copy requirements file without ignores
        with open(self.requirements_file, 'r') as f:
            lines = f.readlines()
        with open(create_path(tmp_dir, 'requirements.txt'), 'w') as f:
            for line in lines:
                if line.strip('\n') not in self.requirements_ignore:
                    f.write(line)

        os.chdir(tmp_dir)

        # compile layer in docker
        command = '''docker run --rm -v {0}:/foo {1} -w /foo lambci/lambda:build-{2} \
                        /bin/bash -c "{3} pip install -r requirements.txt --no-deps -t {4} {5}"'''.format(os.getcwd(), self.build_args if self.build_args else '', self.aws['runtime'], self.pre_build_command + ' &&' if self.pre_build_command else '', package_dir_name, '&& ' + self.post_build_command if self.post_build_command else '')

        comp = subprocess.run([command], stdout=subprocess.PIPE, shell=True)
        if comp.returncode != 0:
            print('Could not compile new layer')
            raise RuntimeError

        # create package zip
        zip_name = 'temp.zip'
        zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)

        for root, _, files in os.walk(package_dir_name):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()

        # read the zip into memory and send to aws
        content = read_file(zip_name)
        self.client.publish_layer_version(
            LayerName=self.layer_name,
            Content={
                'ZipFile': content
            },
            CompatibleRuntimes=[
                self.aws['runtime']
            ]
        )

        # cleanup
        os.chdir('..')
        shutil.rmtree(tmp_dir)
