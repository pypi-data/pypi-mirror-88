# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

from . import initlogging
from aridity.config import ConfigCtrl
from importlib import import_module
from pkg_resources import iter_entry_points
import logging

log = logging.getLogger(__name__)

def main_halp():
    '''You're looking at it!'''
    initlogging()
    config = ConfigCtrl().loadappconfig(main_halp, 'halp.arid')
    projects = set(config.projects)
    others = set()
    undocumented = set()
    halps = []
    for ep in iter_entry_points('console_scripts'):
        project = ep.dist.project_name
        if project in projects:
            obj = import_module(ep.module_name)
            for a in ep.attrs:
                obj = getattr(obj, a)
            doc = obj.__doc__
            if doc is None:
                undocumented.add(ep.name)
            else:
                halps.append((ep.name, doc))
        else:
            others.add(project)
    log.debug("Other projects: %s", ' '.join(sorted(others)))
    log.debug("Undocumented commands: %s", ' '.join(sorted(undocumented)))
    format = "%%-%ss %%s" % max(len(halp[0]) for halp in halps)
    for halp in sorted(halps):
        print(format % halp)
