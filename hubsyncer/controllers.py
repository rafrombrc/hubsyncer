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
# The Initial Developer of the Original Code is Mozilla Corporation.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Rob Miller (rmiller@mozilla.com)
#
# ***** END LICENSE BLOCK *****
from webob.exc import HTTPBadRequest
import json
import os.path
import pipes
import subprocess


class HubSyncController(object):
    def __init__(self, app):
        self.app = app
        repos_path = self.app.config['repos_path']
        if not os.path.exists(repos_path):
            os.mkdir(repos_path)

    def sync(self, request):
        payload = request.POST.get('payload', '{}')
        payload = json.loads(payload)
        repo_data = payload.get('repository', {})
        repo_name = pipes.quote(repo_data.get('name'))
        if not repo_name:
            raise HTTPBadRequest('Missing or malformed payload')
        repos_path = request.config['repos_path']
        repo_path = os.path.join(repos_path, repo_name)
        if not os.path.isdir(repo_path):
            # have to clone the repo
            os.chdir(repos_path)
            git_repo_url = '/'.join([request.config['git_base_url'],
                                     '%s.git' % repo_name])
            subprocess.call(['hg', 'clone', git_repo_url])
            # have to append the hg repo to the paths
            hgrc_path = os.path.join(repo_path, '.hg', 'hgrc')
            with open(hgrc_path, 'a') as hgrc_appender:
                hg_repo_url = '/'.join([request.config['hg_base_url'],
                                        repo_name])
                hgrc_appender.write('\nmoz = %s' % hg_repo_url)
        os.chdir(repo_path)
        # should default to original github repo
        subprocess.call(['hg' 'pull'])
        subprocess.call(['hg' 'up'])
        # explicitly push to the 'moz' path we set up
        subprocess.call(['hg' 'push', 'moz'])
        return 'repo cloned'
