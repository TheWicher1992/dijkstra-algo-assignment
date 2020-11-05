import imports.minheap as minheap
import random
import sys
from dijkstar import Graph, find_path

INFINITY = sys.maxsize


class flight_path():
    def __init__(self, airport_dataf, flight_dataf):
        self.gmt_offsets = {}
        self.flight_data = []
        self.load_gmt_offsets(airport_dataf)
        self.load_flight_data(flight_dataf)
        self.graph = Graph(undirected=False)
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

            self.graph.add_edge(src_airport, dst_airport, total_time_diff)
        print(self.graph)

    def test_dijkstra(self):
        print("PATH\n\n", find_path(self.graph, 'BOS', 'HOU'))


def main():
    flight_path("airport-data.txt", "flight-data.txt")


main()
