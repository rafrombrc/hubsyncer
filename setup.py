# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is hubsyncer.
#
# The Initial Developer of the Original Code is the Mozilla Corporation.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Rob Miller (rmiller@mozilla.com)
#
# ***** END LICENSE BLOCK *****

from setuptools import setup, find_packages

VERSION = '0.1'

setup(
    name='hubsyncer',
    version=VERSION,
    description=('hubsyncer is a simple app that listens for github '
                 'post-receive POSTs and syncs the repository to a '
                 'mercurial repository elsewhere.'),
    author='Mozilla Corporation',
    author_email='rmiller@mozilla.com',
    url='http://www.mozilla.com/',
    install_requires=[
        "PasteScript>=1.6.3",
        "services",
        "nose",
        "coverage",
        "mercurial",
        "hg-git",
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'hubsyncer': ['i18n/*/LC_MESSAGES/*.mo']},
    message_extractors={'hubsyncer': [
            ('**.py', 'python', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript'],
    entry_points="""
    [paste.app_factory]
    main = hubsyncer.wsgiapp:make_app

    [paste.filter_app_factory]
    dbgp = linkdrop.debug:make_dbgp_middleware
    profiler = linkdrop.debug:make_profile_middleware

    [paste.app_install]
    main = paste.script.appinstall:Installer
    """,
)
