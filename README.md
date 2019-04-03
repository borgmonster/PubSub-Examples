
 ## PubSub Subscription Quota Monitoring
 
 ## Table of Contents
 <!-- TOC -->
  [Introduction](#Introduction) 
  [Architecture](#Architecture) 
  [Instructions](#CodeHere)
  <!-- TOC -->
  

## Introduction
Google Cloud has a per project quota limit on number of subscriptions. This limit is somewhat hard limit. There are use cases where this limit can be reached and causes unwanted behavior of processes that are subscribing to topics. This article describes a simple way to monitor the total number of subscriptions within a project and send alerts once a threshold is reached.

## Architecture
TODO: add a chart

## Instructions

 - Create or use a service account with proper roles to run the usage extraction process on a VM
 - Provision a small VM and install the scripts
 - Create a cron job on the VM

Alternatively, you can put these steps in VM startup scripts or create a container.

- Create a log filter on Stackdriver logging:
> resource.type="pubsub_subscription" AND resource.labels.project_id="your project id" AND jsonPayload.total_subscriptions>your threshold

- Test the filter to make sure it captures the log entries emitted by the shell script.
- Create a logbase metric from the filter defined above.
- From Stackdriver Monitoring page, create a alert policy based on the metric defined above.
