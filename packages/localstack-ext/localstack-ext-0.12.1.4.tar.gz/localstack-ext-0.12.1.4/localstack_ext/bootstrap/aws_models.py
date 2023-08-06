from localstack.utils.aws import aws_models
VoJlu=super
VoJlM=None
VoJlB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  VoJlu(LambdaLayer,self).__init__(arn)
  self.cwd=VoJlM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.VoJlB.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,VoJlB,env=VoJlM):
  VoJlu(RDSDatabase,self).__init__(VoJlB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,VoJlB,env=VoJlM):
  VoJlu(RDSCluster,self).__init__(VoJlB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,VoJlB,env=VoJlM):
  VoJlu(AppSyncAPI,self).__init__(VoJlB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,VoJlB,env=VoJlM):
  VoJlu(AmplifyApp,self).__init__(VoJlB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,VoJlB,env=VoJlM):
  VoJlu(ElastiCacheCluster,self).__init__(VoJlB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,VoJlB,env=VoJlM):
  VoJlu(TransferServer,self).__init__(VoJlB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,VoJlB,env=VoJlM):
  VoJlu(CloudFrontDistribution,self).__init__(VoJlB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,VoJlB,env=VoJlM):
  VoJlu(CodeCommitRepository,self).__init__(VoJlB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
