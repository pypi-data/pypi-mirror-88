[![NPM version](https://badge.fury.io/js/cdk-apisix.svg)](https://badge.fury.io/js/cdk-apisix)
[![PyPI version](https://badge.fury.io/py/cdk-apisix.svg)](https://badge.fury.io/py/cdk-apisix)
![Release](https://github.com/pahud/cdk-apisix/workflows/Release/badge.svg)

# cdk-apisix

CDK construct library to generate serverless [Apache APISIX](https://github.com/apache/apisix) workload on AWS Fargate.

# sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_apisix import Apisix

Apisix(stack, "apisix-demo",
    apisix_container=ContainerImage.from_asset(path.join(__dirname, "../apisix_container")),
    etcd_container=ContainerImage.from_registry("public.ecr.aws/eks-distro/etcd-io/etcd:v3.4.14-eks-1-18-1"),
    dashboard_container=ContainerImage.from_asset(path.join(__dirname, "../apisix_dashboard"))
)
```
