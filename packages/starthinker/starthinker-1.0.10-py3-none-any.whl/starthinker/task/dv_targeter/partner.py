###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################


from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id

from starthinker.task.dv_targeter.types import DV360_Targeting
from starthinker.task.dv_targeter.types import TARGETING_TYPES


def partner_targeting_load():

  targeting = DV360_Targeting()

  partners = [lookup_id(p[0]) for p in get_rows(
    project.task['auth_sheets'], 
    { 'sheets': {
      'sheet': project.task['sheet'],
      'tab': 'Partners',
      'range': 'A2:A'
    }}
  )]

  # write to database
  for targeting_type, targeting_meta in TARGETING_TYPES.items():
    if targeting_meta['partner']:

      put_rows(
        project.task['auth_bigquery'], 
        { 'bigquery': {
          'dataset': project.task['dataset'],
          'table': 'DV_Targeting_%s' % targeting_meta['name'],
          'schema': targeting.get_schema(targeting_meta['name'], targeting_meta['resource']),
          'disposition':'WRITE_APPEND',
          'format': 'JSON'
        }},
        targeting.get_partner(project.task['auth_dv'], partners, targeting_type)
      )
