from localstack.utils.aws import aws_models
wNYpL=super
wNYpa=None
wNYpJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  wNYpL(LambdaLayer,self).__init__(arn)
  self.cwd=wNYpa
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.wNYpJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,wNYpJ,env=wNYpa):
  wNYpL(RDSDatabase,self).__init__(wNYpJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,wNYpJ,env=wNYpa):
  wNYpL(RDSCluster,self).__init__(wNYpJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,wNYpJ,env=wNYpa):
  wNYpL(AppSyncAPI,self).__init__(wNYpJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,wNYpJ,env=wNYpa):
  wNYpL(AmplifyApp,self).__init__(wNYpJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,wNYpJ,env=wNYpa):
  wNYpL(ElastiCacheCluster,self).__init__(wNYpJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,wNYpJ,env=wNYpa):
  wNYpL(TransferServer,self).__init__(wNYpJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,wNYpJ,env=wNYpa):
  wNYpL(CloudFrontDistribution,self).__init__(wNYpJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,wNYpJ,env=wNYpa):
  wNYpL(CodeCommitRepository,self).__init__(wNYpJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
