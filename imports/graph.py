import sys
import imports.minheap as minheap
gmt_offsets = {}


def load_gmt_offsets(filename):
    gmtf = open(filename, 'r')

    n = int(gmtf.readline().strip())

    for i in range(n):
        airport, offset = gmtf.readline().strip().split("\t")
        gmt_offsets[airport] = int(offset)


INFINITY = sys.maxsize


def get_time_diff(src_time, dst_time):
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

    src_t_gmt = (src_t - gmt_offsets[src]) % 2400
    dst_t_gmt = (dst_t - gmt_offsets[dst]) % 2400

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


def to_12h(time):
    res = ()
    if(time >= 1200):
        res = (time, 'P')
        if(time >= 1300):
            res = (time-1200, 'P')

    else:
        if(time < 100):
            res = (time + 1200, 'A')
        else:
            res = (time, 'A')
    return res


def to_24h(time):
    t, ap = time

    if(ap == 'P'):
        if(t >= 1200):
            pass
        else:
            t = (t + 1200) % 2400
    else:
        if(t >= 1200):
            t = (t + 1200) % 2400

    return t


class graph:
    def __init__(self):
        self.edges = {}
        self.nodes = []
        # self.data = flight_data

    def add_edge(self, u, v, l1, l2, l3, l4, weight):
        if (u not in self.edges):
            self.edges[u] = []
        if(v not in self.edges):
            self.edges[v] = []

        self.edges[u].append((v, l1, l2, weight, l3, l4))

    def dijkstra(self, src, start_time):
        pred = {}
        d = {}

        for v in self.edges:
            d[v] = INFINITY
            pred[v] = []

        d[src] = 0

        priority_queue = minheap.min_heap()

        for v in self.edges:
            # print(v, d[v])
            priority_queue.insert(v, d[v])

        while(not priority_queue.is_empty()):
            item = priority_queue.delete_min()

            u = item[0]
            # print("u ", u, " ", item[1])
            for edge in self.edges[u]:
                v = edge[0]
                if(u == src):
                    diff = get_time_diff(
                        (u, start_time[0], start_time[1]), (u, edge[4][0], edge[4][1]))
                    # print("diff: ", diff)
                    if(diff > -120):
                        continue
                    else:
                        if(d[v] > d[u] + edge[3] + abs(diff)):
                            # print("v ", v, " ", d[u] + edge[3] + abs(diff))
                            priority_queue.decrease_key(
                                v, d[u] + edge[3] + abs(diff), d[v])
                            d[v] = d[u] + edge[3] + abs(diff)
                            pred[v] = (u, edge)
                else:
                    if(len(pred[u]) == 0):
                        continue
                    landed_time = (u, pred[u][1][5][0], pred[u][1][5][1])
                    # print("LANDED: ", landed_time)
                    # print("TAKE: ", (u, edge[4][0], edge[4][1]))
                    diff = get_time_diff(
                        landed_time, (u, edge[4][0], edge[4][1]))
                    if(diff > -60):
                        continue
                    else:
                        if(d[v] > d[u] + edge[3] + abs(diff)):
                            # print("v ", v, " ", d[u] + edge[3]+abs(diff))
                            priority_queue.decrease_key(
                                v, d[u] + edge[3]+abs(diff), d[v])
                            d[v] = d[u] + edge[3]+abs(diff)
                            pred[v] = (u, edge)

        # print(d, "\n\n", pred)
        return pred, d
