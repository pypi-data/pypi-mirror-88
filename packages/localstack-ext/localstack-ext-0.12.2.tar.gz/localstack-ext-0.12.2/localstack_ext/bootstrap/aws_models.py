from localstack.utils.aws import aws_models
dUljp=super
dUljf=None
dUljJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dUljp(LambdaLayer,self).__init__(arn)
  self.cwd=dUljf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.dUljJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,dUljJ,env=dUljf):
  dUljp(RDSDatabase,self).__init__(dUljJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,dUljJ,env=dUljf):
  dUljp(RDSCluster,self).__init__(dUljJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,dUljJ,env=dUljf):
  dUljp(AppSyncAPI,self).__init__(dUljJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,dUljJ,env=dUljf):
  dUljp(AmplifyApp,self).__init__(dUljJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,dUljJ,env=dUljf):
  dUljp(ElastiCacheCluster,self).__init__(dUljJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,dUljJ,env=dUljf):
  dUljp(TransferServer,self).__init__(dUljJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,dUljJ,env=dUljf):
  dUljp(CloudFrontDistribution,self).__init__(dUljJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,dUljJ,env=dUljf):
  dUljp(CodeCommitRepository,self).__init__(dUljJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
