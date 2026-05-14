# 🔒 Kubernetes NetworkPolicy Demo: Default-Deny + DNS + Frontend → Backend (8080)

This repository demonstrates a **minimal, reproducible setup** of Kubernetes `NetworkPolicy` to enforce **Zero Trust networking** inside a namespace.  

It covers:  
✅ Namespace-wide **default deny** (Ingress + Egress)  
✅ Allowing **DNS resolution**  
✅ Allowing only **frontend → backend communication on TCP 8080**  
✅ (Optional) Restricting **frontend egress strictly to backend:8080**

---

## 🚀 Prerequisites

- A Kubernetes cluster with a CNI that implements `NetworkPolicy`  
  _(e.g., [Calico](https://projectcalico.docs.tigera.io/), [Cilium](https://cilium.io/), [Weave Net](https://www.weave.works/docs/net/latest/kubernetes/kube-addon/))_
- `kubectl` configured to talk to your cluster

---

## ⚡ Quick Start

### 1️⃣ Create namespace & sample pods/services

```bash
kubectl create ns zt

# Backend: simple HTTP echo, exposed via Service on 8080
kubectl -n zt run backend 
  --image=hashicorp/http-echo --restart=Never -- -text="ok"
kubectl -n zt expose pod backend --name backend --port 8080 --target-port 5678
kubectl -n zt label pod backend app=backend --overwrite

# Frontend: test client
kubectl -n zt run frontend 
  --image=busybox:1.36 --restart=Never --labels app=frontend -- sleep 600
```

---

### 2️⃣ Apply policies

#### 🛑 Default Deny All (`zt-deny-all.yaml`)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: zt-deny-all
  namespace: zt
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

#### 🌐 Allow DNS (`allow-dns.yaml`)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: zt
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

#### 🔄 Allow Frontend → Backend (8080) (`allow-frontend-to-backend.yaml`)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: zt
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

#### (Optional) 🎯 Restrict Frontend Egress (`allow-frontend-egress-to-backend.yaml`)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-egress-to-backend
  namespace: zt
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 8080
```

Apply all policies:

```bash
kubectl apply -f zt-deny-all.yaml
kubectl apply -f allow-dns.yaml
kubectl apply -f allow-frontend-to-backend.yaml
# optional
kubectl apply -f allow-frontend-egress-to-backend.yaml
```

---

## 🔍 Verify Resources

```bash
kubectl -n zt get pod -L app -o wide
kubectl -n zt get svc -o wide
kubectl -n zt get netpol -o wide
```

✅ You should see:  
- **Pods**: `frontend` (app=frontend), `backend` (app=backend)  
- **Service**: `backend` on `8080/TCP`  
- **Policies**: `zt-deny-all`, `allow-dns`, `allow-frontend-to-backend` (+ optional egress)

---

## 🧪 Tests

### Allowed ✅  
Frontend → Backend on **8080**:  

```bash
kubectl -n zt exec frontend -- wget -qO- http://backend:8080
# Expected:
ok
```

### Blocked 🚫  
Frontend → Backend on **9090**:  

```bash
kubectl -n zt exec frontend -- wget -qO- http://backend:9090 || echo "blocked"
# Expected:
blocked
```

---

## 🛠️ How It Works

- **Default Deny** → `zt-deny-all` isolates all pods until explicit allows are added.  
- **DNS Allow** → `allow-dns` permits egress on UDP/TCP 53 for name resolution.  
- **Frontend → Backend Allow** → `allow-frontend-to-backend` allows ingress only from pods labeled `app=frontend` to `backend` on TCP 8080.  
- **Optional Egress Restrict** → `allow-frontend-egress-to-backend` confines frontend’s egress exclusively to backend:8080.  

📌 **Important**: NetworkPolicies are **additive**. The effective rules are the **union** of all policies that select a given pod.

---

## 📚 References

- [Kubernetes NetworkPolicy Docs](https://kubernetes.io/docs/concepts/services-networking/network-policies/)  
- [Calico NetworkPolicy](https://docs.tigera.io/calico/latest/network-policy)  
- [Cilium NetworkPolicy](https://docs.cilium.io/en/stable/policy/language/)

---

✨ With this setup, you get a **Zero Trust namespace**: nothing talks unless you **explicitly allow** it.  
