# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
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

"""Tests for tensorflow_datasets.scripts.cli.main."""

from unittest import mock

from tensorflow_datasets.scripts.cli import main


def test_main():

  def _check_exit(status=0, message=None):
    del message
    assert status == 0  # Check argparse exit gracefully

  # Argparse call `sys.exit(0)` when `--version` is passed.
  with mock.patch('sys.exit', _check_exit):
    version_flag = '--version'
    main.main(main._parse_flags(['', version_flag]))


def test_normalize_flags():
  assert main._normalize_flags([
      'path/to/cli/main.py',
      'build',
      '--regular_flag=14001',
      '--bolean_flag=true',
      '--bolean_flag=false',
      '--bolean_FLAG_123=true',
      '--bolean_FLAG_123=false',
      '--non_bolean_flag=abc=true',
      'non_bolean_flag=false',
  ]) == [
      'path/to/cli/main.py',
      'build',
      '--regular_flag=14001',
      '--bolean_flag',
      '--nobolean_flag',
      '--bolean_FLAG_123',
      '--nobolean_FLAG_123',
      '--non_bolean_flag=abc=true',
      'non_bolean_flag=false',
  ]
