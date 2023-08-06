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

class DescribeRouteEntryListRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Vpc', '2016-04-28', 'DescribeRouteEntryList','vpc')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_RouteEntryName(self):
		return self.get_query_params().get('RouteEntryName')

	def set_RouteEntryName(self,RouteEntryName):
		self.add_query_param('RouteEntryName',RouteEntryName)

	def get_NextToken(self):
		return self.get_query_params().get('NextToken')

	def set_NextToken(self,NextToken):
		self.add_query_param('NextToken',NextToken)

	def get_RouteEntryType(self):
		return self.get_query_params().get('RouteEntryType')

	def set_RouteEntryType(self,RouteEntryType):
		self.add_query_param('RouteEntryType',RouteEntryType)

	def get_IpVersion(self):
		return self.get_query_params().get('IpVersion')

	def set_IpVersion(self,IpVersion):
		self.add_query_param('IpVersion',IpVersion)

	def get_NextHopId(self):
		return self.get_query_params().get('NextHopId')

	def set_NextHopId(self,NextHopId):
		self.add_query_param('NextHopId',NextHopId)

	def get_NextHopType(self):
		return self.get_query_params().get('NextHopType')

	def set_NextHopType(self,NextHopType):
		self.add_query_param('NextHopType',NextHopType)

	def get_RouteTableId(self):
		return self.get_query_params().get('RouteTableId')

	def set_RouteTableId(self,RouteTableId):
		self.add_query_param('RouteTableId',RouteTableId)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_DestinationCidrBlock(self):
		return self.get_query_params().get('DestinationCidrBlock')

	def set_DestinationCidrBlock(self,DestinationCidrBlock):
		self.add_query_param('DestinationCidrBlock',DestinationCidrBlock)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_MaxResult(self):
		return self.get_query_params().get('MaxResult')

	def set_MaxResult(self,MaxResult):
		self.add_query_param('MaxResult',MaxResult)

	def get_RouteEntryId(self):
		return self.get_query_params().get('RouteEntryId')

	def set_RouteEntryId(self,RouteEntryId):
		self.add_query_param('RouteEntryId',RouteEntryId)