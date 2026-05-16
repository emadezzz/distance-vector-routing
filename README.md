# Distance Vector Routing Simulation

Python based simulation of distance vector routing using UDP sockets and distributed router instances.

## Overview

This project simulates how routing tables are built and updated using a distance vector routing approach.

The system demonstrates how routers exchange routing information with neighbouring routers and gradually discover the lowest cost paths across a network. The implementation follows concepts used in routing protocols such as RIP and applies Bellman Ford style route calculations.

The simulation was designed using multiple router instances communicating through UDP sockets while maintaining independent routing behaviour.

---

## Features

- Distance vector routing simulation
- Bellman Ford based route updates
- UDP socket communication
- Multiple router instances
- Periodic routing table exchange
- Distributed routing behaviour
- Routing table convergence
- Configurable network topology
- Console based routing output
- Multithreaded message handling

---

## Technologies Used

- Python
- UDP Sockets
- Threading
- JSON
- Distance Vector Routing
- Bellman Ford Algorithm
- Network Simulation

---

## Project Files

```text
config.py
router.py
Distance_Vector_Routing_Report.pdf
```

---

## Network Topology

The simulation uses five routers:

```text
A, B, C, D, E
```

Each router has a dedicated UDP port and predefined neighbouring routers with associated link costs.

Example topology:

```text
A --1-- B
|       | \
2       1  3
|       |   \
C --4-- E --2-- D
```

---

## Configuration

Example router ports:

```python
ROUTERS = {
    "A": {"port": 5001},
    "B": {"port": 5002},
    "C": {"port": 5003},
    "D": {"port": 5004},
    "E": {"port": 5005},
}
```

Update interval:

```python
UPDATE_INTERVAL = 5
MAX_HOPS = 16
```

---

## How It Works

Each router:

- Starts with knowledge of itself and direct neighbours
- Sends routing updates to neighbouring routers
- Receives updates through UDP sockets
- Stores neighbour vectors
- Recalculates paths using advertised route costs
- Updates routing tables when better routes are discovered
- Continues until network convergence is reached

---

## How to Run

Open separate terminal windows and run:

```bash
python3 router.py A
python3 router.py B
python3 router.py C
python3 router.py D
python3 router.py E
```

Each router will continuously exchange routing information and display updated routing tables.

---

## Academic Context

Developed for the Computer Networks module as part of the BSc Computer Science programme at the University of South Wales.

---

## Author

Emad Ezzadeen  
BSc Computer Science Graduate  
University of South Wales
