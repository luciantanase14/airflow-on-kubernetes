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



## Logging Configuration



## Deployment Instructions



## How to Deploy New DAGs


