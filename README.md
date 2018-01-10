This blueprint demonstrates a "service composition" approach.

It creates the following components:

1. A database cluster.
2. A load balancer, handling requests across the cluster nodes.
3. An application that uses the database cluster as a backend via the load balancer.

Components (1) and (2) are deployments in themselves. They run in virtual machines.

Component (3) is a Kubernetes deployment.


### Usage instructions

* Make sure your manager has the required plugins:

  * https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases
  * https://github.com/cloudify-incubator/cloudify-kubernetes-plugin/releases
  * https://github.com/EarthmanT/cloudify-dblb/releases

__Check which version of each plugin is required by the blueprint.__


* Execute install workflow:

```
cfy install db-lb-app/blueprint.yaml
```


The default IaaS is Openstack. You can run on AWS, Azure, or GCP as well by overriding the environment blueprint:

```
cfy install db-lb-app/blueprint.yaml-i environment_blueprint_filename=aws-blueprint.yaml
```


* Once the application is installed, you can scale the database cluster:

```
cfy executions start scale_and_update -d db-lb-app
```


* To uninstall the demo:

```
cfy uninstall --allow-custom-parameters -p ignore_failure=true db-lb-app
```
