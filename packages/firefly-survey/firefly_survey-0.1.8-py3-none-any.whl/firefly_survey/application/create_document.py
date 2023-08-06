#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

from __future__ import annotations

import importlib
import os

import firefly as ff

secured = False if os.environ.get('ANONYMOUS_ACCESS', 'false') in (True, 'true', 1, '1') else True

domain = importlib.import_module(f'{os.environ.get("CONTEXT")}.domain')


@ff.rest('/documents', method='POST', secured=secured)
class CreateDocument(ff.ApplicationService):
    _registry: ff.Registry = None

    def __call__(self, schema: str, data: dict, **kwargs):
        schemas = self._registry(domain.Schema)
        documents = self._registry(domain.Document)

        schema = schemas.find(schema)
        if schema is None:
            raise ff.NotFound()

        params = {'schema': schema, 'data': data}
        params.update(kwargs)

        documents.append(domain.Document.from_dict(params))
