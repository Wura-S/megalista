# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import apache_beam as beam
import logging

from typing import List

from uploaders import google_ads_utils as ads_utils
from uploaders.google_ads_customer_match.abstract_uploader import GoogleAdsCustomerMatchAbstractUploaderDoFn 
from uploaders import utils as utils
from utils.execution import Action
from utils.oauth_credentials import OAuthCredentials


class GoogleAdsCustomerMatchMobileUploaderDoFn(GoogleAdsCustomerMatchAbstractUploaderDoFn):
  def __init__(self, oauth_credentials: OAuthCredentials, developer_token: str, customer_id: str, app_id: str):
    super().__init__(oauth_credentials, developer_token, customer_id)
    self.app_id = app_id

  def get_list_definition(self, list_name):
    return {
      'operand': {
        'xsi_type': 'CrmBasedUserList',
        'name': list_name,
        'description': list_name,
        # CRM-based user list_name can use a membershipLifeSpan of 10000 to indicate
        # unlimited; otherwise normal values apply.
        'membershipLifeSpan': 10000,
        'appId': self.app_id,
        'uploadKeyType': 'MOBILE_ADVERTISING_ID'
      }
    }

  def get_row_keys(self) -> List[str]:
    return ['mobileId']

  def get_action_type(self) -> Action:
    return Action.ADS_CUSTOMER_MATCH_MOBILE_DEVICE_ID_UPLOAD
