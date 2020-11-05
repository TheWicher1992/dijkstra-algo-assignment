import imports.minheap as minheap
import random
import sys
from dijkstar import Graph, find_path

INFINITY = sys.maxsize


# def test_heap():
#     heap = minheap.min_heap()
#     test_data = [(10, 9), (15, 6), (2, 10), (5, 0), (11, 12)]

#     for k in test_data:
#         heap.insert(k[0], k[1])

#     print(heap.delete_min())
#     heap.decrease_key(2, 1)
#     print(heap.delete_min())
#     print(heap.delete_min())
#     print(heap.delete_min())
#     print(heap.delete_min())
#     print(heap.delete_min())


class graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, u, v, l1, l2, weight):
        if (u not in self.edges):
            self.edges[u] = []

        self.edges[u].append((v, l1, l2, weight))

    def dijkstra(self, src, dst):
        pred = {}
        d = {}

        for v in self.edges:
            d[v] = INFINITY
            pred[v] = []
        d[src] = 0

        priority_queue = minheap.min_heap()

        for v in self.edges:
            print(v, d[v])
            priority_queue.insert(v, d[v])

        while(not priority_queue.is_empty()):
            item = priority_queue.delete_min()

            u = item[0]
            print("u ", u, " ", item[1])
            for edge in self.edges[u]:
                v = edge[0]
                if(d[v] > d[u] + edge[3]):
                    print("v ", v, " ", d[u] + edge[3])
                    priority_queue.decrease_key(v, d[u] + edge[3])
                    d[v] = d[u] + edge[3]
                    pred[v].append(edge)

        print(d, "\n\n")


class flight_path():
    def __init__(self, airport_dataf, flight_dataf):
        self.gmt_offsets = {}
        self.flight_data = []
        self.load_gmt_offsets(airport_dataf)
        self.load_flight_data(flight_dataf)
        self.graph = graph()
        self.make_graph()
        self.test_dijkstra()

    def load_gmt_offsets(self, filename):
        gmtf = open(filename, 'r')

        n = int(gmtf.readline().strip())

        for i in range(n):
            airport, offset = gmtf.readline().strip().split("\t")
            self.gmt_offsets[airport] = int(offset)

        # print(self.gmt_offsets)

    def load_flight_data(self, flight_dataf):
        flightf = open(flight_dataf, 'r')
        data = flightf.readline()

        while(data):
            fd = data.strip().split('\t')
            if(len(fd) == 8):
                self.flight_data.append(fd)
            data = flightf.readline()

        # print(self.flight_data)
    def make_graph(self):
        for flight in self.flight_data:
            airline = flight[0]
            flight_number = flight[1]
            src_airport = flight[2]

            local_dep_ap = flight[4]

            local_dep = int(flight[3]) if local_dep_ap == 'A' else (
                (int(flight[3]) + 1200) % 2400)

            dst_airport = flight[5]

            local_arrv_ap = flight[7]

            local_arrv = int(flight[6]) if local_arrv_ap == 'A' else (
                (int(flight[6]) + 1200) % 2400)

            local_arrv_gmt = local_arrv + self.gmt_offsets[dst_airport]
            local_dep_gmt = local_dep + self.gmt_offsets[src_airport]

            local_arrv_gmt = (
                local_arrv + self.gmt_offsets[dst_airport] + 2400) if local_arrv_gmt < 0 else local_arrv_gmt
            local_dep_gmt = (
                local_dep + self.gmt_offsets[src_airport] + 2400) if local_dep_gmt < 0 else local_dep_gmt

            if(src_airport == 'ABQ' and dst_airport == 'DCA'):
                print("local arr\t" + str(local_arrv))
                print("local dep\t" + str(local_dep))
                print("local arr gmt\t" + str(local_arrv_gmt))
                print("local dep gmt\t" + str(local_dep_gmt))

            local_arrv_gmt_m = local_arrv_gmt % 100
            local_dep_gmt_m = local_dep_gmt % 100
            local_arrv_gmt_h = local_arrv_gmt - local_arrv_gmt_m
            local_dep_gmt_h = local_dep_gmt - local_dep_gmt_m

            total_time_diff = abs(
                ((local_dep_gmt_h/100 * 60) + local_dep_gmt_m)
                -
                ((local_arrv_gmt_h/100 * 60) + local_arrv_gmt_m)
            )

            self.graph.add_edge(
                src_airport, dst_airport,
                airline, flight_number, total_time_diff
            )
        print(self.graph.edges['BOS'])

    def test_dijkstra(self):
        self.graph.dijkstra('BOS', 'HOU')


def main():
    flight_path("airport-data.txt", "flight-data.txt")


main()
