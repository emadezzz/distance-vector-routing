import socket
import threading
import json
import time
import sys

from config import ROUTERS, TOPOLOGY, UPDATE_INTERVAL, MAX_HOPS

INF = MAX_HOPS

class Router:
    def __init__(self, router_id):
        self.id = router_id
        self.port = ROUTERS[router_id]["port"]
        self.neighbours = TOPOLOGY[router_id]
        self.routing_table = {}
        self.neighbour_vectors = {}
        self.lock = threading.Lock()
        self.running = True
        self._init_routing_table()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", self.port))
        self.sock.settimeout(1.0)

    def _init_routing_table(self):
        self.routing_table[self.id] = {"cost": 0, "next_hop": self.id}
        for neighbour, cost in self.neighbours.items():
            self.routing_table[neighbour] = {"cost": cost, "next_hop": neighbour}
        self._log("Routing table initialised")
        self._print_table()

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        print(f"[{ts}] Router {self.id}: {msg}")

    def _print_table(self):
        print(f"\n{'─'*45}")
        print(f"  Router {self.id}  -  Routing Table")
        print(f"{'─'*45}")
        print(f"  {'Dest':<8} {'Cost':<8} {'Next Hop'}")
        print(f"{'─'*45}")
        for dest in sorted(self.routing_table):
            entry = self.routing_table[dest]
            cost_str = "INF" if entry["cost"] >= INF else str(entry["cost"])
            print(f"  {dest:<8} {cost_str:<8} {entry['next_hop']}")
        print(f"{'─'*45}\n")

    def _send_update(self):
        with self.lock:
            vector = {dest: entry["cost"] for dest, entry in self.routing_table.items()}
        message = json.dumps({"from": self.id, "vector": vector}).encode()
        for neighbour in self.neighbours:
            dest_port = ROUTERS[neighbour]["port"]
            self.sock.sendto(message, ("127.0.0.1", dest_port))
        self._log(f"Sent update to: {list(self.neighbours.keys())}")

    def _recalculate(self):
        changed = False
        with self.lock:
            for neighbour, vector in self.neighbour_vectors.items():
                link_cost = self.neighbours[neighbour]
                for dest, advertised_cost in vector.items():
                    if advertised_cost >= INF:
                        continue
                    new_cost = min(link_cost + advertised_cost, INF)
                    current = self.routing_table.get(dest)
                    if current is None or new_cost < current["cost"]:
                        self.routing_table[dest] = {"cost": new_cost, "next_hop": neighbour}
                        changed = True
                    elif current["next_hop"] == neighbour and new_cost != current["cost"]:
                        self.routing_table[dest] = {"cost": new_cost, "next_hop": neighbour}
                        changed = True
        return changed

    def _receive_loop(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(4096)
                msg = json.loads(data.decode())
                sender = msg["from"]
                vector = msg["vector"]
                self._log(f"Received update from Router {sender}")
                with self.lock:
                    self.neighbour_vectors[sender] = vector
                if self._recalculate():
                    self._log("Routing table UPDATED")
                    self._print_table()
                else:
                    self._log("No changes")
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    self._log(f"Error: {e}")

    def _send_loop(self):
        time.sleep(1)
        while self.running:
            self._send_update()
            time.sleep(UPDATE_INTERVAL)

    def start(self):
        self._log(f"Starting on port {self.port}. Neighbours: {self.neighbours}")
        threading.Thread(target=self._receive_loop, daemon=True).start()
        threading.Thread(target=self._send_loop, daemon=True).start()
        self._log("Router running. Press Ctrl+C to stop.\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self._log("Shutting down...")
            self.running = False
            self.sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ROUTERS:
        print(f"Usage: python3 router.py <router_id>")
        print(f"Available: {list(ROUTERS.keys())}")
        sys.exit(1)
    r = Router(sys.argv[1])
    r.start()