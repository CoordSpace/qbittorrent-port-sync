# qBittorrent Port Sync

## Summary

A simple (ideally dockerized) python script that syncs the Listening Port setting from one instance of qBittorrent to another. Both need to be accessable via webUI and be running at the time of the sync.

## Motivation

Due to weird service limitation with my network-wide VPN, I don't have a static port forward. Instead every 6 days or so I have to request a new random forwarded port from their API and then set my main qBittorrent shard to match. This program allows for keeping that ever-changing setting in sync with another qBittorrent instance without any manual intervention.

# Setup and Execution

## Local Install!

## Docker Install

### Notice

This project is in no way affiliated with the qBittorrent Project and the use of their software's name is only done to facilitate easier discovery for searching users.

