import imports.minheap as minheap


class graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, u, v, l1, l2, weight):
        if (u not in self.edges):
            self.edges[u] = []

        self.edges[u].append((v, l1, l2, weight))


class flight_path():
    def __init__(self, airport_dataf, flight_dataf):
        self.gmt_offsets = {}
        self.flight_data = []
        self.load_gmt_offsets(airport_dataf)
        self.load_flight_data(flight_dataf)
        self.graph = graph()
        self.make_graph()

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
            local_dep = (int(flight[3]) + 1200) % 2400
            local_dep_ap = flight[4]
            dst_airport = flight[5]
            local_arrv = (int(flight[6]) + 1200) % 2400
            local_arrv_ap = flight[7]
            local_arrv_gmt = local_arrv + self.gmt_offsets[dst_airport]
            local_dep_gmt = local_dep + self.gmt_offsets[src_airport]

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


def main():
    flight_path("airport-data.txt", "flight-data.txt")


main()
