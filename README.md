# HCM AI Playground Platform Definition and GitOps 

## Introduction

This repository contains the ArgoCD (GitOps) applications that, when applied to a cluster, will install the operators, configuration, and workload to create or replicate the HCM AI Playground.  

The HCM AI Playground is a space for Software Engineers to leverage hosted models via an Inference Service, refine their own models and RAGs via OpenShift AI, or leverage the entire OpenShift AI platform in a managed environment.  

You can use this repository to configure most or all replicas of the HCM AI Playground environment operated by Red Hat's HCM organizaiton _or_ you can fork and use this repository to stand up your own environment analogous to the HCM AI Playground environment.  

## Using this Repository

### Repository Structure

The repository is structured as follows:

* `gitops-applications`: contains ArgoCD applications that, when applied to a cluster, install the operators, configuration, and workload defined in the other portions of this repository
* `inference-service`: contains the workload and configuration that defines the intference-as-a-service component of the AI Playground
* `operators`: contains a series of kustomize payloads that have been pulled or adapted from the [GitOps Catalog](https://github.com/redhat-cop/gitops-catalog/) to install the operators necessary for the AI Playground
* `patch`: contains any patches that must be applied before the remainder of the gitops-applications defined in this repository
* `scripts`: contains useful companion scripts for use alongside the completed platform

### Building Your Own AI Playground

To stand up a new replica of the AI Playground based on this repository, you must do the following:
1. Provision an OpenShift Cluster with at least one GPU-Accelerated Node (Note: this repository, by default, enables the NVIDIA GPU Operator, if you want to leverage AMD GPUs, you need to install AMD's GPU Operator)
2. Install the [OpenShift GitOps Operator](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.16/html/installing_gitops/installing-openshift-gitops) on your cluster (or ArgoCD (https://argo-cd.readthedocs.io/en/stable/getting_started/) if you prefer).  
    1. You will need to enable OpenShift GitOps or ArgoCD in cluster-wide mode because our applications reside in multiple namespaces.  OpenShift GitOps automatically deploys in cluster-wide mode if deployed in the openshift-gitops (default) namespace.  
    2. You need to modify your ArgoCD Custom Resource configuration to enable ArgoCD to reconcile Applications from all namespace - make sure to do the following:
        1. Edit the ArgoCD Instance and add the following to both `spec.server` and `spec.controller`: 
        ```
        extraCommandArgs:
        - '--application-namespaces=*'
        ```
        2. Edit the Default AppProject CR to include the following in its `spec`:
        ```
        sourceNamespaces:
            - '*'
        ```
    3. For every namespace that you want ArgoCD to work in, you will need to apply a label as follows: `oc label namespace <namespace-name> argocd.argoproj.io/managed-by=<namespace-of-the-argocd-instance>`
3. `oc apply` the ClusterRoles and ClusterRoleBindings in the `patch/argocd-permissions` directory to give the ArgoCD ServiceAccount the necessary fine-grained permissions necessary to deploy all of the operators
4. `oc apply -f gitops-applications/*.yaml` to install all of the operators and workload onto your cluster
5. Navigate to the ArgoCD UI on your cluster and verify that the Applications reconcile correctly.  

### Modifying an Existing AI Playground Environment or Customizing for your Environment

If you would like to modify an existing deployment that references this repository, you can do so by editing any file in the operator or workload directory (excludes gitops-applications, patch, and scripts directories).  That change will be reconciled to environments by ArgoCD shortly.  

If a modification should only be made to one environment, you should create a Kustomize overlay for that environment's configuration to overlay the current base files and reference that specific environment's config in the environment's version of the gitops-application.  

## Developing and Extending the AI Playground

### Adding Operators

If you would like to add an operator to the AI Playground environment defined in this repository, you should start by checking for an existing entry in the [GitOps Catalog](https://github.com/redhat-cop/gitops-catalog/).  If there is an entry, you can copy it into the `operators` directory.  If there is not an entry, you should use the existing operators as a model and create a new directory and kustomize definition for the operator in the `operators` directory.  

Once you've added a new folder, you should create a corresponding ArgoCD Application in the `gitops-applications` directory, using an existing file as an example.  

### Adding Workload

If you would like to add a workload to the AI Playground environment defined in this repository you should create a new folder and GitOps Application if the workload is net-new _or_ add it to an existing directory if the workload extends and existing workload.  

For example, if you wanted to add a model to the current Inference Service, you would simply add its definition to the payload in the `inference-service` directory.  

If you instead wanted to add a net-new service to validate models for content or correctness, you would add a new directory with its own Kustomize directory that defined the service, then make a cooresponding GitOps Application in `gitops-applications` for that application and apply the GitOps Application to the target cluster.  