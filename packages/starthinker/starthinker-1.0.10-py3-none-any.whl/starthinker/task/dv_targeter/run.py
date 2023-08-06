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

from starthinker.util.project import project

from starthinker.task.dv_editor.advertiser import advertiser_clear
from starthinker.task.dv_editor.advertiser import advertiser_load
from starthinker.task.dv_editor.audit import audit_clear
from starthinker.task.dv_editor.audit import audit_load
from starthinker.task.dv_editor.partner import partner_clear
from starthinker.task.dv_editor.partner import partner_load
from starthinker.task.dv_editor.line_item import line_item_clear

from starthinker.task.dv_targeter.campaign import campaign_clear
from starthinker.task.dv_targeter.campaign import campaign_load
from starthinker.task.dv_targeter.insertion_order import insertion_order_clear
from starthinker.task.dv_targeter.insertion_order import insertion_order_load
from starthinker.task.dv_targeter.line_item import line_item_targeting_load
from starthinker.task.dv_targeter.partner import partner_targeting_load
from starthinker.task.dv_targeter.advertiser import advertiser_targeting_load

from starthinker.task.dv_targeter.types import DV360_Targeting
from starthinker.task.dv_targeter.types import TARGETING_TYPES

from starthinker.util.bigquery import table_create
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.sheets import sheets_clear


def targeting_clear():
  targeting = DV360_Targeting()

  for targeting_meta in TARGETING_TYPES.values():

    table_create(
      project.task['auth_bigquery'],
      project.id,
      project.task['dataset'],
      'DV_Targeting_%s' % targeting_meta['name'],
      targeting.get_schema(targeting_meta['name'], targeting_meta['resource'])
    )

    sheets_clear(
      project.task['auth_sheets'],
      project.task['sheet'],
      targeting_meta['name'],
      'A2:Z'
    )


@project.from_parameters
def dv_targeter():
  print('COMMAND:', project.task['command'])

  if project.task['command'] == 'Clear':
    audit_clear()
    #patch_clear()
    partner_clear()
    targeting_clear()

  elif project.task['command'] == 'Load Partners':
    partner_clear()
    partner_load()

  elif project.task['command'] == 'Load Advertisers':
    advertiser_clear()
    advertiser_load()

  elif project.task['command'] == 'Load Line Items':
    campaign_clear()
    campaign_load()
    insertion_order_clear()
    insertion_order_load()
    line_item_clear()
    line_item_load()

  elif project.task['command'] == 'Load Targeting':
    #targeting_clear()
    #partner_targeting_load()
    #advertiser_targeting_load()
    line_item_targeting_load()

  elif project.task['command'] in ('Preview', 'Patch'):
    audit_clear()
    patch_clear()
    audit_load()

    #partner_patch(commit=project.task['command'] == 'Patch')
    #advertiser_patch(commit=project.task['command'] == 'Patch')
    #line_item_patch(commit=project.task['command'] == 'Patch')


if __name__ == '__main__':
  dv_targeter()
