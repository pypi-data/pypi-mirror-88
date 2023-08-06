from localstack.utils.aws import aws_models
KgCiP=super
KgCiW=None
KgCik=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KgCiP(LambdaLayer,self).__init__(arn)
  self.cwd=KgCiW
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.KgCik.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,KgCik,env=KgCiW):
  KgCiP(RDSDatabase,self).__init__(KgCik,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,KgCik,env=KgCiW):
  KgCiP(RDSCluster,self).__init__(KgCik,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,KgCik,env=KgCiW):
  KgCiP(AppSyncAPI,self).__init__(KgCik,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,KgCik,env=KgCiW):
  KgCiP(AmplifyApp,self).__init__(KgCik,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,KgCik,env=KgCiW):
  KgCiP(ElastiCacheCluster,self).__init__(KgCik,env=env)
class TransferServer(BaseComponent):
 def __init__(self,KgCik,env=KgCiW):
  KgCiP(TransferServer,self).__init__(KgCik,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,KgCik,env=KgCiW):
  KgCiP(CloudFrontDistribution,self).__init__(KgCik,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,KgCik,env=KgCiW):
  KgCiP(CodeCommitRepository,self).__init__(KgCik,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
