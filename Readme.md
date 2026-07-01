# Heartbeat Monitoring System

This project demonstrates a simple heartbeat monitoring system using Python sockets.

## Overview
The system consists of a client and server:
- The client sends periodic heartbeat messages.
- The server monitors active clients and detects failures if heartbeats are missed.

## Features
- Real-time heartbeat tracking
- Automatic client timeout detection
- Multi-threaded server handling multiple clients
- Automatic client reconnection

## Technologies Used
- Python
- Socket Programming
- Multithreading

## How to Run

### 1. Start server
python server.py

### 2. Start clients
python client.py

## Use Case
This project simulates monitoring of data pipelines or distributed systems to detect failures in real time.