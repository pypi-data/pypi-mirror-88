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
from aliyunsdkvpc.endpoint import endpoint_data

class UpdateIpsecServerRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Vpc', '2016-04-28', 'UpdateIpsecServer','vpc')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_IkeConfig(self):
		return self.get_query_params().get('IkeConfig')

	def set_IkeConfig(self,IkeConfig):
		self.add_query_param('IkeConfig',IkeConfig)

	def get_ClientToken(self):
		return self.get_query_params().get('ClientToken')

	def set_ClientToken(self,ClientToken):
		self.add_query_param('ClientToken',ClientToken)

	def get_IpsecConfig(self):
		return self.get_query_params().get('IpsecConfig')

	def set_IpsecConfig(self,IpsecConfig):
		self.add_query_param('IpsecConfig',IpsecConfig)

	def get_Psk(self):
		return self.get_query_params().get('Psk')

	def set_Psk(self,Psk):
		self.add_query_param('Psk',Psk)

	def get_LocalSubnet(self):
		return self.get_query_params().get('LocalSubnet')

	def set_LocalSubnet(self,LocalSubnet):
		self.add_query_param('LocalSubnet',LocalSubnet)

	def get_EffectImmediately(self):
		return self.get_query_params().get('EffectImmediately')

	def set_EffectImmediately(self,EffectImmediately):
		self.add_query_param('EffectImmediately',EffectImmediately)

	def get_ClientIpPool(self):
		return self.get_query_params().get('ClientIpPool')

	def set_ClientIpPool(self,ClientIpPool):
		self.add_query_param('ClientIpPool',ClientIpPool)

	def get_DryRun(self):
		return self.get_query_params().get('DryRun')

	def set_DryRun(self,DryRun):
		self.add_query_param('DryRun',DryRun)

	def get_PskEnabled(self):
		return self.get_query_params().get('PskEnabled')

	def set_PskEnabled(self,PskEnabled):
		self.add_query_param('PskEnabled',PskEnabled)

	def get_IpsecServerName(self):
		return self.get_query_params().get('IpsecServerName')

	def set_IpsecServerName(self,IpsecServerName):
		self.add_query_param('IpsecServerName',IpsecServerName)

	def get_IpsecServerId(self):
		return self.get_query_params().get('IpsecServerId')

	def set_IpsecServerId(self,IpsecServerId):
		self.add_query_param('IpsecServerId',IpsecServerId)