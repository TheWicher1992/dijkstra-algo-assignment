import sys
import random
import imports.graph as graph


class flight_path():
    def __init__(self, airport_dataf, flight_dataf):
        self.flight_data = []
        graph.load_gmt_offsets(airport_dataf)
        self.load_flight_data(flight_dataf)
        self.graph = graph.graph()
        self.make_graph()
        # print(self.graph.edges)
        # # self.test_dijkstra()

        # # print(self.gmt_offsets)

    def load_flight_data(self, flight_dataf):
        flightf = open(flight_dataf, 'r')
        data = flightf.readline()

        while(data):
            fd = data.strip().split('\t')
            if(len(fd) == 8):
                self.flight_data.append(fd)
            data = flightf.readline()

        # print(self.flight_data)
    def get_time_diff(self, src_time, dst_time):
        src, src_t, src_ap = src_time
        dst, dst_t, dst_ap = dst_time
        # print("SRC TIME: ", src_t, src_ap)
        # print("DST TIME: ", dst_t, dst_ap)

        if(src_ap == 'P'):
            if(src_t >= 1200):
                pass
            else:
                src_t = (src_t + 1200) % 2400
        else:
            if(src_t >= 1200):
                src_t = (src_t + 1200) % 2400

        if(dst_ap == 'P'):
            if(dst_t >= 1200):
                pass
            else:
                dst_t = (dst_t + 1200) % 2400
        else:
            if(dst_t >= 1200):
                dst_t = (dst_t + 1200) % 2400

        # print("24HR SRC TIME: ", src_t)
        # print("24HR DST TIME: ", dst_t)

        src_t_gmt = (src_t - graph.gmt_offsets[src]) % 2400
        dst_t_gmt = (dst_t - graph.gmt_offsets[dst]) % 2400

        # print("GMT SRC TIME: ", src_t_gmt)
        # print("GMT DST TIME: ", dst_t_gmt)

        # src_gmt_m = src_t_gmt % 100
        dst_gmt_m = dst_t_gmt % 100

        if(src_t_gmt > dst_t_gmt):
            dst_t_gmt = 2400 + dst_t_gmt
        src_gmt_m = src_t_gmt % 100

        src_gmt_h = src_t_gmt - src_gmt_m
        dst_gmt_h = dst_t_gmt - dst_gmt_m

        diff = (((src_gmt_h / 100) * 60) + src_gmt_m) - \
            (((dst_gmt_h / 100) * 60) + dst_gmt_m)

        # print('TIME DIFF: ', diff)

        return diff

        pass

    def make_graph(self):
        for flight in self.flight_data:
            airline = flight[0]
            flight_number = flight[1]
            src_airport = flight[2]

            local_srct_ap = flight[4]

            local_srct = int(flight[3])

            dst_airport = flight[5]

            local_dstt_ap = flight[7]

            local_dstt = int(flight[6])

            total_time_diff = self.get_time_diff(
                (src_airport, local_srct, local_srct_ap), (dst_airport, local_dstt, local_dstt_ap))

            self.graph.add_edge(
                src_airport, dst_airport,
                airline, flight_number,
                (local_srct, local_srct_ap), (local_dstt,
                                              local_dstt_ap), -total_time_diff
            )

    def print_path(self, pred, src, dst):
        flights = []
        node = dst
        while(node != src):
            flights.append(pred[node])
            node = pred[node][0]
        flights = flights[::-1]

        for flight in flights:
            flight_code = flight[1][1]
            flight_number = flight[1][2]
            src_airport = flight[0]
            src_time = flight[1][4]
            dst_airport = flight[1][0]
            dst_time = flight[1][5]

            print(flight_code, flight_number, "("+src_airport,
                  src_time[0], src_time[1]+"M -->", dst_airport, dst_time[0], dst_time[1]+"M)")
        # print("\n\nFLIGHTS\n\n", flights)

    def get_route(self, src, dst, start_time, time_at_dst):
        # src = 'BOS'
        # dst = 'HOU'
        # start_time = (1000, 'A')
        # time_at_dst = 22
        if(src not in self.graph.edges or dst not in self.graph.edges):
            print("Source or Destination does not exist\n")
            return
        pred1, d1 = self.graph.dijkstra(src, start_time)
        if(d1[dst] == graph.INFINITY):
            print("No possible schedule\n")
            return
        time_reached = pred1[dst][1][5]
        start_time = (graph.to_24h(time_reached) + (time_at_dst*100)) % 2400
        pred2, d2 = self.graph.dijkstra(dst, graph.to_12h(start_time))
        self.print_path(pred1, src, dst)

        self.print_path(pred2, dst, src)


def main():
    flight_sim = flight_path("airport-data.txt", "flight-data.txt")
    try:
        schedule = input(
            "Enter SRC DST START_TIME TIME_YOU_WANT_TO_SPENT:\n").split(" ")
        if(len(schedule) > 5):
            print("Invalid Input")
            return
        src = schedule[0]
        dst = schedule[1]
        start_time = (int(schedule[2]), schedule[3])
        time_at_dst = int(schedule[4])

        flight_sim.get_route(src, dst, start_time, time_at_dst)
    except:
        print("Invalid Input")


main()
