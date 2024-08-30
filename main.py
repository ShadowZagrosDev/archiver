#!/usr/bin/env python
# -*- coding: utf-8 -*-
# iagitup - Download github repository and upload it to the Internet Archive with metadata.

# Copyright (C) 2017-2018 Giovanni Damiola
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

__author__     = "Giovanni Damiola"
__copyright__  = "Copyright 2018, Giovanni Damiola"
__main_name__  = 'iagitup'
__license__    = 'GPLv3'
__status__     = "Production/Stable"
__version__    = "v1.7"

import shutil
import argparse

from iagitup import iagitup

PROGRAM_DESCRIPTION = 'A tool to archive a GitHub repository to the Internet Archive. \
                       The script downloads the GitHub repository, creates a git bundle and uploads \
                       it to archive.org. https://github.com/gdamdam/iagitup'

# Configure argparser
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('--metadata', '-m', default=None, type=str, required=False, help="custom metadata to add to the archive.org item")
parser.add_argument('--version', '-v', action='version', version=__version__)
parser.add_argument('url', type=str, help='[GITHUB REPO] to archive')
args = parser.parse_args()

def main():
    iagitup.check_ia_credentials()

    URL = args.url
    custom_metadata = args.metadata
    custom_meta_dict = None

    print(f":: Downloading {URL} repository...")
    gh_repo_data, repo_folder = iagitup.repo_download(URL)

    # parse supplemental metadata.
    if custom_metadata != None:
        custom_meta_dict = {}
        for meta in custom_metadata.split(','):
            k, v = meta.split(':')
            custom_meta_dict[k] = v

    # upload the repo on IA
    identifier, meta, bundle_filename = iagitup.upload_ia(repo_folder, gh_repo_data, custom_meta=custom_meta_dict)

    # cleaning
    shutil.rmtree(repo_folder)

    # output
    print("\n:: Upload FINISHED. Item information:")
    print(f"Identifier: {meta['title']}")
    print(f"Archived repository URL: \n \thttps://archive.org/details/{identifier}")
    print(f"Archived git bundle file: \n \thttps://archive.org/download/{identifier}/{bundle_filename}.bundle \n\n")


if __name__ == '__main__':
    main()

