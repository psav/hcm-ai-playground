# Jina Embedding Service

This folder contains the resources necessary to deploy the Jina model as an
inference engine using the Red Hat OpenShift AI `InferenceService` and 
`ServiceRuntime` resources.

These could be optimised further, but right now represent a fairly stable
model load.

TODOs/Further Work:
* Use modelcar for loading the model instead of S3
* Add parameters for replica count