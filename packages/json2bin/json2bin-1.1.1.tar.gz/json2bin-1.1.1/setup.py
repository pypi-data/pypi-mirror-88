# Copyright 2020 The JINKAI Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import shutil
import subprocess
import sys
from setuptools import setup
from setuptools.command.install import install


class BuildProgram(install):
  def run(self):
    root = os.path.dirname(os.path.abspath(__file__))
    subprocess.check_call(
        'g++ -std=c++14 -I{0}/src -o {0}/scripts/json2bin {0}/src/json2bin.cpp'.format(
            root),
        cwd=root,
        shell=True)
    subprocess.check_call(
        'chmod +x {0}/scripts/json2bin'.format(root),
        cwd=root,
        shell=True)
    exec_root = os.path.dirname(os.path.abspath(sys.executable))
    shutil.copy('{0}/scripts/json2bin'.format(root), exec_root)
    super().run()


setup(
    name="json2bin",
    version="1.1.1",
    description="Json Binarize Tool.",
    license="Apache-2.0",
    author="KaiJIN",
    author_email="atranitell@gmail.com",
    cmdclass={'install': BuildProgram},
)
