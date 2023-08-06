# Backend.AI Statistics Monitoring Plugin with Datadog

## Installation

Just `pip install backend.ai-monitor-datadog` inside the virtualenv of the Backend.AI Manager and Agent.

## Configuration

Set the following etcd configurations via the manager cli:
```
backend.ai mgr etcd put config/plugins/stats_monitor/datadog/datadog_api_key "..."
backend.ai mgr etcd put config/plugins/stats_monitor/datadog/datadog_app_key "..."
```
