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

from .common import findproject
from lagoon import ag
import os, sys

def main_agi():
    'Search for identifier.'
    ag._ws.exec(*sys.argv[1:], findproject())

def main_agil():
    'Edit files containing identifier.'
    # XXX: Can't we use lagoon here?
    command = [os.environ['EDITOR']] + ag._wsl(*sys.argv[1:], findproject()).splitlines()
    os.execvp(command[0], command)
