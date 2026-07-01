# Heartbeat Monitoring System

## Overview
This project implements a real-time heartbeat monitoring system using Python sockets.

The system follows a client-server architecture:
- Clients send periodic heartbeat signals.
- Server tracks active clients and detects failures if heartbeat stops.

## Features
- Real-time heartbeat monitoring
- Automatic client timeout detection
- Multi-client support using multithreading
- Auto-reconnect mechanism
- Logging of activity

## Tech Stack
- Python
- Socket Programming
- Multithreading

## How to Run

### Start Server
python server.py

### Start Client
python client.py

## Sample Output

Server:
[12:00:01] Server: New connection  
[12:00:05] Server: Received HEARTBEAT  

Client:
[12:00:05] Client: Sent heartbeat  

## Use Case
This system simulates monitoring of distributed systems or data pipelines by detecting failures in real time.
