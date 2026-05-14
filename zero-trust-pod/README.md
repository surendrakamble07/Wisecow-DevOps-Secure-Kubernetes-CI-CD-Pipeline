# KubeArmor Zero Trust Security Demonstration

## Overview
This project demonstrates how to implement a Zero Trust security model for Kubernetes workloads using KubeArmor. The focus is on blocking shell access (`/bin/bash` and `/bin/sh`) in the `wisewow` namespace pods, which ensures strict process-level control to prevent unauthorized access.

## Prerequisites
- A Kubernetes cluster (this demo uses KIND)
- Helm installed and configured
- Kubectl access to the cluster

## Installation and Setup

### 1. Installing KubeArmor
Add the KubeArmor Helm repository and install all components (operator, controller, relay, and daemonset):

helm repo add kubearmor https://kubearmor.github.io/charts
helm repo update
helm upgrade --install kubearmor kubearmor/kubearmor -n kubearmor --create-namespace

Verify that all KubeArmor pods are running:

kubectl get pods -n kubearmor


### 2. Define and Apply Zero Trust Policy
Create a KubeArmor policy YAML to block process execution of `/bin/bash` and `/bin/sh` within pods in the `wisewow` namespace.

Apply it:

kubectl apply -f wisewow-zero-trust.yaml

Verify it’s created:

kubectl get ksp -n wisewow

## Verification and Proof

### Blocked Shell Access
Attempts to exec into pods using `/bin/bash` or `/bin/sh` return immediately with no shell, showing enforcement:
kubectl exec -n wisewow <pod-name> -- /bin/bash
kubectl exec -n wisewow <pod-name> -- /bin/sh



### Allowed Commands
Normal commands such as `ls /` work correctly:

kubectl exec -n wisewow <pod-name> -- ls /



### Optional: Fetch KubeArmor Logs
You can check logs for enforcement events:

kubectl logs -n kubearmor -l app=kubearmor

(Note: logs may be silent or empty if no violation occurs.)

## Notes
- The policy applies at pod level scoped by namespace and labels.
- KubeArmor uses kernel-level technologies (LSM, eBPF) to enforce policies.
- Blocked execs may produce no visible error, but are denied at the syscall level.

## Summary
KubeArmor provides powerful runtime controls enabling zero-trust enforcement on Kubernetes workloads, demonstrated here by selectively blocking shell access while permitting normal execution flow.

## References
- [KubeArmor Documentation](https://kubearmor.io)
- [KubeArmor GitHub](https://github.com/kubearmor/KubeArmor)

## Policies
- `wisewow-zero-trust.yaml`: KubeArmor policy manifest disabling `/bin/bash` and `/bin/sh` execution.

---

*This document and associated configurations complete the demonstration of Zero Trust enforcement using KubeArmor.*


