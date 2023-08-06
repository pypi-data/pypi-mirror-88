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
from aliyunsdkservicemesh.endpoint import endpoint_data

class UpdateIstioInjectionConfigRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'servicemesh', '2020-01-11', 'UpdateIstioInjectionConfig','servicemesh')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_EnableIstioInjection(self):
		return self.get_body_params().get('EnableIstioInjection')

	def set_EnableIstioInjection(self,EnableIstioInjection):
		self.add_body_params('EnableIstioInjection', EnableIstioInjection)

	def get_Namespace(self):
		return self.get_body_params().get('Namespace')

	def set_Namespace(self,Namespace):
		self.add_body_params('Namespace', Namespace)

	def get_ServiceMeshId(self):
		return self.get_body_params().get('ServiceMeshId')

	def set_ServiceMeshId(self,ServiceMeshId):
		self.add_body_params('ServiceMeshId', ServiceMeshId)