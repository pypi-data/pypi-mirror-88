from localstack.utils.aws import aws_models
JzUTb=super
JzUTv=None
JzUTw=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  JzUTb(LambdaLayer,self).__init__(arn)
  self.cwd=JzUTv
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.JzUTw.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,JzUTw,env=JzUTv):
  JzUTb(RDSDatabase,self).__init__(JzUTw,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,JzUTw,env=JzUTv):
  JzUTb(RDSCluster,self).__init__(JzUTw,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,JzUTw,env=JzUTv):
  JzUTb(AppSyncAPI,self).__init__(JzUTw,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,JzUTw,env=JzUTv):
  JzUTb(AmplifyApp,self).__init__(JzUTw,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,JzUTw,env=JzUTv):
  JzUTb(ElastiCacheCluster,self).__init__(JzUTw,env=env)
class TransferServer(BaseComponent):
 def __init__(self,JzUTw,env=JzUTv):
  JzUTb(TransferServer,self).__init__(JzUTw,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,JzUTw,env=JzUTv):
  JzUTb(CloudFrontDistribution,self).__init__(JzUTw,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,JzUTw,env=JzUTv):
  JzUTb(CodeCommitRepository,self).__init__(JzUTw,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
