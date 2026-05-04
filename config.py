ROUTERS = {
    "A": {"port": 5001},
    "B": {"port": 5002},
    "C": {"port": 5003},
    "D": {"port": 5004},
    "E": {"port": 5005},
}

TOPOLOGY = {
    "A": {"B": 1, "C": 2},
    "B": {"A": 1, "D": 3, "E": 1},
    "C": {"A": 2, "E": 4},
    "D": {"B": 3, "E": 2},
    "E": {"B": 1, "C": 4, "D": 2},
}

UPDATE_INTERVAL = 5
MAX_HOPS        = 16