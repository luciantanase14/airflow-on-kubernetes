# Airflow Deployment on Kubernetes

This repository has what it needs to deploy Apache Airflow on a Kubernetes cluster, specifically to an existing Amazon EKS cluster.

## Table of Contents

- [Introduction](#introduction)
- [Executor Choice](#executor-choice)
  - [Why KubernetesExecutor?](#why-kubernetesexecutor)
  - [Alternatives I considered](#alternatives-i-considered)
- [DAG Deployment Method](#dag-deployment-method)
- [Logging Configuration](#logging-configuration)
- [Deployment Instructions](#deployment-instructions)
- [How to deploy new DAGs](#how-to-deploy-new-dags)

## Introduction

This project provides a reliable and scalable way to deploy Apache Airflow on Kubernetes. By leveraging Kubernetes powerful orchestration capabilities, we can efficiently manage Airflow's components and workloads.

## Executor Choice

### Why KubernetesExecutor?

I chose the **KubernetesExecutor** for the Airflow deployment because it offers great scalability, efficiency, and integrates very well with Kubernetes.

#### Benefits of KubernetesExecutor

- **Scalability**: Each Airflow task runs in its own Kubernetes pod, allowing to scale dynamically based on workload demands.
- **Resource Isolation**: Tasks are isolated in separate pods, so issues with one task won't affect others.
- **Dynamic Resource Allocation**: It can specify resources (CPU, memory) for each task, giving the fine-grained control over resource usage.
- **Simplified Architecture**: Eliminates the need for extra components like Celery workers and message brokers, reducing complexity.
- **Native Kubernetes Integration**: Takes full advantage of Kubernetes features like scheduling, auto-scaling, and self-healing.

#### How It Works

- The Airflow Scheduler schedules tasks and creates corresponding Kubernetes pods.
- Each pod runs an Airflow task independently.
- After a task is completed, the pod shuts down, freeing up resources.

### Alternatives I Considered

#### CeleryExecutor

- **Overview**: Uses a message broker (like RabbitMQ or Redis) and a pool of worker processes to execute tasks.
- **Why We Didn't Choose It**:
  - **Added Complexity**: Managing extra components increases complexity.
  - **Resource Overhead**: Worker nodes consume resources even when idle.
  - **Maintenance Burden**: More components mean more maintenance and potential points of failure.

#### LocalExecutor

- **Overview**: Executes tasks locally on the same machine as the Scheduler.
- **Why I didn't choose it**:
  - **Limited Scalability**: Not suitable for high workloads or distributed environments.
  - **Resource Contention**: Scheduler and tasks compete for the same resources.
  - **Single Point of Failure**: Doesn't offer the fault tolerance of distributed systems.

### Conclusion

The **KubernetesExecutor** fits the main goal perfectly. It provides scalability, efficient resource use, and integrates smoothly with any existing Kubernetes infrastructure. By using it, it can simplify deployment and reduce the operational overhead of managing additional components.

---

## DAG Deployment Method

### Using Git-Sync Sidecar Container

I choosed to use the **Git-Sync Sidecar Container** method to deploy the DAGs. This involves adding a sidecar container to the Scheduler and Webserver pods that continuously syncs DAGs from a Git repository.

#### How It Works

- **Scheduler and Webserver Deployments**:
  - Located in the `manifests/` directory:
    - `scheduler-deployment.yaml`
    - `webserver-deployment.yaml`
- **Git-Sync Sidecar**:
  - Included in the deployments mentioned above.
  - Pulls DAGs from the specified Git repository and updates the DAGs directory in the Airflow containers.

#### Benefits

- **Automation**: DAGs are automatically updated when changes are pushed to the Git repository.
- **Version Control**: Utilize Git powerful features for collaboration, history tracking, and code review.
- **Simplicity**: Avoids the need for setting up and maintaining additional storage solutions.

#### Configuration

To set up Git-Sync:

- **Git Repository**: Ensure it has a Git repository containing the DAGs. This can be on GitHub, GitLab, or any Git server.
- **Environment Variables**: Configure the Git-Sync container with the repository URL, branch, and synchronization frequency.

## Logging Configuration

Airflow logs, including logs from tasks running in KubernetesExecutor pods, are configured to display in the Airflow UI.

### How It Works

- **Local Logging**: Logs are written to local files and displayed in the Airflow UI.
- **Worker Logs**: Logs from worker pods are fetched and displayed in the Airflow console, configured through Airflow's logging settings.

### Logging Setup

- Configure the logging settings in `airflow.cfg` or through environment variables in the Scheduler and Webserver deployments.
- Example logging configuration can be found in the `airflow-configmap.yaml` file in the `manifests/` directory.

## Deployment Instructions

### Prerequisites

- Access to a Kubernetes cluster (e.g., Amazon EKS).
- `kubectl` installed and configured.
- The `airflow-dags` Git repository is accessible to the cluster.

### Deploy Airflow

Follow these steps to deploy Airflow on your Kubernetes cluster:

1. **Clone This Repository**

   Clone the repository that contains the Airflow setup:

   ```bash
   git clone https://github.com/luciantanase14/airflow-on-kubernetes.git
   cd airflow-on-kubernetes

2. **Deploy Script Executable**
    ```bash
    chmod +x deploy.sh

3. **Run the Deploy Script**
    ```bash
    ./deploy.sh

4. **Verify the Deployment**
    ```bash
    kubectl get pods -n default
    kubectl get services -n default

5. **Access the Airflow UI**
    Access the Airflow Webserver UI using the IPm or URL configured by the service. If you used a LoadBalancer service, use the external IP, for NodePort access it via the node IP and the specified port.


## How to Deploy New DAGs

To add, or update DAGs in your Airflow setup:

1. **Clone the DAGs Repository**

   Clone the DAGs repository, where all DAG files are stored:

   ```bash
   git clone https://github.com/luciantanase14/airflow-dags.git
   cd airflow-dags

2. **Add or Modify DAG Files**
    Add the new DAG files or update existing ones in the dags/ directory.

3. **Commit and Push Changes**
    ```bash
    git add dags/new_dag.py
    git commit -m "Add new DAG for data processing"
    git push origin main
