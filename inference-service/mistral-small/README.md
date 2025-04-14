# Mistral Small Inference Service

This folder contains the resources necessary to deploy the Mistral Small model as an
inference engine using the Red Hat OpenShift AI `InferenceService` and 
`ServiceRuntime` resources.

Custom parameters have been passed to enable the model to load into the GPU

* `max-model-len` of `20480`
* `gpu-memory-utilization` of `0.95`

These could be optimised further, but right now represent a fairly stable
model load.

TODOs/Further Work:
* Use modelcar for loading the model instead of S3
* Add parameters for replica count