"""
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
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_efs
import aws_cdk.core


class Apisix(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-apisix.Apisix",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        apisix_container: aws_cdk.aws_ecs.ContainerImage,
        dashboard_container: aws_cdk.aws_ecs.ContainerImage,
        etcd_container: aws_cdk.aws_ecs.ContainerImage,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
        efs_filesystem: typing.Optional[aws_cdk.aws_efs.IFileSystem] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param apisix_container: 
        :param dashboard_container: 
        :param etcd_container: 
        :param cluster: 
        :param efs_filesystem: 
        :param vpc: 
        """
        props = ApisixProps(
            apisix_container=apisix_container,
            dashboard_container=dashboard_container,
            etcd_container=etcd_container,
            cluster=cluster,
            efs_filesystem=efs_filesystem,
            vpc=vpc,
        )

        jsii.create(Apisix, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return jsii.get(self, "vpc")


@jsii.data_type(
    jsii_type="cdk-apisix.ApisixProps",
    jsii_struct_bases=[],
    name_mapping={
        "apisix_container": "apisixContainer",
        "dashboard_container": "dashboardContainer",
        "etcd_container": "etcdContainer",
        "cluster": "cluster",
        "efs_filesystem": "efsFilesystem",
        "vpc": "vpc",
    },
)
class ApisixProps:
    def __init__(
        self,
        *,
        apisix_container: aws_cdk.aws_ecs.ContainerImage,
        dashboard_container: aws_cdk.aws_ecs.ContainerImage,
        etcd_container: aws_cdk.aws_ecs.ContainerImage,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
        efs_filesystem: typing.Optional[aws_cdk.aws_efs.IFileSystem] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param apisix_container: 
        :param dashboard_container: 
        :param etcd_container: 
        :param cluster: 
        :param efs_filesystem: 
        :param vpc: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "apisix_container": apisix_container,
            "dashboard_container": dashboard_container,
            "etcd_container": etcd_container,
        }
        if cluster is not None:
            self._values["cluster"] = cluster
        if efs_filesystem is not None:
            self._values["efs_filesystem"] = efs_filesystem
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def apisix_container(self) -> aws_cdk.aws_ecs.ContainerImage:
        result = self._values.get("apisix_container")
        assert result is not None, "Required property 'apisix_container' is missing"
        return result

    @builtins.property
    def dashboard_container(self) -> aws_cdk.aws_ecs.ContainerImage:
        result = self._values.get("dashboard_container")
        assert result is not None, "Required property 'dashboard_container' is missing"
        return result

    @builtins.property
    def etcd_container(self) -> aws_cdk.aws_ecs.ContainerImage:
        result = self._values.get("etcd_container")
        assert result is not None, "Required property 'etcd_container' is missing"
        return result

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        result = self._values.get("cluster")
        return result

    @builtins.property
    def efs_filesystem(self) -> typing.Optional[aws_cdk.aws_efs.IFileSystem]:
        result = self._values.get("efs_filesystem")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApisixProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Apisix",
    "ApisixProps",
]

publication.publish()
