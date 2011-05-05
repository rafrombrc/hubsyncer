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
from pkg_resources import Requirement, resource_filename
from webob.exc import HTTPBadRequest
import json
import os.path
import pipes
import subprocess

hubsyncer_egg = Requirement.parse('hubsyncer')
PAYLOAD_QUEUE_FILE_PATH = resource_filename(hubsyncer_egg, 'var/payloads.json')


def abort(payload_json):
    """
    Write the payload out to the 'catchup' file and return an error message.
    """
    with open(PAYLOAD_QUEUE_FILE_PATH, 'a') as payload_file_appender:
        payload_file_appender.write('\n\n%s\n\n' % payload_json)
    return 'repository sync aborted!'


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
        ref = payload.get('ref')
        if not repo_name or not ref:
            raise HTTPBadRequest('Missing or malformed payload')
        branchname = pipes.quote(ref.split('/')[-1])
        repos_path = request.config['repos_path']
        repo_path = os.path.join(repos_path, repo_name)
        hgbin = os.path.join(request.config['bin'], 'hg')
        if not os.path.isdir(repo_path):
            # have to clone the repo
            os.chdir(repos_path)
            git_repo_url = '/'.join([request.config['git_base_url'],
                                     '%s.git' % repo_name])
            # any non-zero return code == failure
            if subprocess.call([hgbin, 'clone', git_repo_url]):
                return abort(payload_json)
            # have to append the hg repo to the paths
            hgrc_path = os.path.join(repo_path, '.hg', 'hgrc')
            with open(hgrc_path, 'a') as hgrc_appender:
                hg_repo_url = '/'.join([request.config['hg_base_url'],
                                        repo_name])
                hgrc_appender.write('\nmoz = %s' % hg_repo_url)
        os.chdir(repo_path)
        # should default to original github repo
        if subprocess.call([hgbin, 'pull']):
            return abort(payload_json)
        if subprocess.call([hgbin, 'up']):
            return abort(payload_json)
        # explicitly push to the 'moz' path we set up
        if subprocess.call([hgbin, 'push', '-B', branchname, 'moz']):
            return abort(payload_json)
        return 'repo cloned'
