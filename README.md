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


## How to Deploy New DAGs


