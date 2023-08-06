# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkmpaas.endpoint import endpoint_data

class UpdateMpaasAppInfoRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'mPaaS', '2019-08-21', 'UpdateMpaasAppInfo')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_SystemType(self):
		return self.get_body_params().get('SystemType')

	def set_SystemType(self,SystemType):
		self.add_body_params('SystemType', SystemType)

	def get_OnexFlag(self):
		return self.get_body_params().get('OnexFlag')

	def set_OnexFlag(self,OnexFlag):
		self.add_body_params('OnexFlag', OnexFlag)

	def get_AppName(self):
		return self.get_body_params().get('AppName')

	def set_AppName(self,AppName):
		self.add_body_params('AppName', AppName)

	def get_TenantId(self):
		return self.get_body_params().get('TenantId')

	def set_TenantId(self,TenantId):
		self.add_body_params('TenantId', TenantId)

	def get_Identifier(self):
		return self.get_body_params().get('Identifier')

	def set_Identifier(self,Identifier):
		self.add_body_params('Identifier', Identifier)

	def get_IconFileUrl(self):
		return self.get_body_params().get('IconFileUrl')

	def set_IconFileUrl(self,IconFileUrl):
		self.add_body_params('IconFileUrl', IconFileUrl)

	def get_AppId(self):
		return self.get_body_params().get('AppId')

	def set_AppId(self,AppId):
		self.add_body_params('AppId', AppId)