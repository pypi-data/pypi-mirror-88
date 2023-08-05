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

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

Query to Sheet

Copy the contents of a query into a Google Sheet.

  - Specify the sheet and the query.
  - Leave range blank or set to A2 to insert one line down.
  - The range is cleared before the sheet is written to.
  - To select a table use SELECT * FROM table.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_read': 'user',  # Credentials used for reading data.
  'sheet': '',  # Either sheet url or sheet name.
  'tab': '',  # Name of the tab where to put the data.
  'range': '',  # Range in the sheet to place the data, leave blank for whole sheet.
  'dataset': '',  # Existing BigQuery dataset.
  'query': '',  # Query to pull data from the table.
  'legacy': True,  # Use Legacy SQL
}

RECIPE = {
  'tasks': [
    {
      'bigquery': {
        'auth': {
          'field': {
            'name': 'auth_read',
            'kind': 'authentication',
            'order': 1,
            'default': 'user',
            'description': 'Credentials used for reading data.'
          }
        },
        'from': {
          'auth': 'service',
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'order': 4,
              'default': '',
              'description': 'Existing BigQuery dataset.'
            }
          },
          'query': {
            'field': {
              'name': 'query',
              'kind': 'text',
              'order': 5,
              'default': '',
              'description': 'Query to pull data from the table.'
            }
          },
          'legacy': {
            'field': {
              'name': 'legacy',
              'kind': 'boolean',
              'order': 6,
              'default': True,
              'description': 'Use Legacy SQL'
            }
          }
        },
        'to': {
          'sheet': {
            'field': {
              'name': 'sheet',
              'kind': 'string',
              'order': 1,
              'default': '',
              'description': 'Either sheet url or sheet name.'
            }
          },
          'tab': {
            'field': {
              'name': 'tab',
              'kind': 'string',
              'order': 2,
              'default': '',
              'description': 'Name of the tab where to put the data.'
            }
          },
          'range': {
            'field': {
              'name': 'range',
              'kind': 'string',
              'order': 3,
              'default': '',
              'description': 'Range in the sheet to place the data, leave blank for whole sheet.'
            }
          }
        }
      }
    }
  ]
}

DAG_FACTORY = DAG_Factory('bigquery_to_sheet', RECIPE, INPUTS)
DAG = DAG_FACTORY.generate()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
