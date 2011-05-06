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
# The Original Code is Raindrop.
#
# The Initial Developer of the Original Code is
# Mozilla Messaging, Inc..
# Portions created by the Initial Developer are Copyright (C) 2009
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Rob Miller (rmiller@mozilla.com)
#
# ***** END LICENSE BLOCK *****
"""
Application entry point.
"""
from hubsyncer.controllers import HubSyncController
from hubsyncer.controllers import hubsyncer_egg
from pkg_resources import resource_filename
from services.baseapp import set_app, SyncServerApp
import os.path

urls = [
    ('POST', '/', 'hubsync', 'sync'),
    ]

controllers = {'hubsync': HubSyncController}


class HubSyncerApp(SyncServerApp):
    """HubSyncer WSGI application"""
    def __init__(self, urls, controllers, config, auth_class=None,
                 *args, **kwargs):
        if auth_class is not None:
            raise ValueError("A HubSyncerApp's ``auth_class`` must be None.")
        # make sure var folder exists
        var_path = resource_filename(hubsyncer_egg, 'var')
        if not os.path.isdir(var_path):
            os.mkdir(var_path)
        super(HubSyncerApp, self).__init__(urls, controllers, config,
                                           auth_class, *args, **kwargs)


make_app = set_app(urls, controllers, klass=HubSyncerApp, auth_class=None)
