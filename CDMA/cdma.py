# https://www.includehelp.com/computer-networks/code-division-multiple-access-cdma.aspx
# https://en.wikipedia.org/wiki/Code-division_multiple_access#Code-division_multiplexing_(synchronous_CDMA)
# https://gist.github.com/manudatta/45845f457d2f4ea75b6a

class CDMA:
    wtable = []  # walsh table
    copy = []    # matrix
    channel_sequence = []  # array
    num_stations = None

    def __init__(self, num_stations):
        self.num_stations = num_stations

    def set_up(self, data):
        for i in range(self.num_stations):
            self.wtable.append([])
            for j in range(self.num_stations):
                self.wtable[i].append(None)

        for i in range(self.num_stations):
            self.copy.append([])
            for j in range(self.num_stations):
                self.copy[i].append(None)

        self.build_walsh_table(self.num_stations, 0, self.num_stations - 1, 0, self.num_stations - 1, False)
        self.print_walsh_table()

        for i in range(self.num_stations):
            for j in range(self.num_stations):
                self.copy[i][j] = self.wtable[i][j]
                self.wtable[i][j] *= data[i]

        for i in range(self.num_stations):
            self.channel_sequence.append(0)

        for i in range(self.num_stations):
            for j in range(self.num_stations):
                self.channel_sequence[i] += self.wtable[j][i]

    def build_walsh_table(self, length, i1, i2, j1, j2, is_bar):
        if length == 2:
            if not is_bar:
                self.wtable[i1][j1] =  1
                self.wtable[i1][j2] =  1
                self.wtable[i2][j1] =  1
                self.wtable[i2][j2] = -1
            else:
                self.wtable[i1][j1] = -1
                self.wtable[i1][j2] = -1
                self.wtable[i2][j1] = -1
                self.wtable[i2][j2] =  1
        elif length > 2:
            mid_i = (i1 + i2) // 2
            mid_j = (j1 + j2) // 2

            self.build_walsh_table(length // 2,        i1, mid_i,        j1, mid_j, is_bar)
            self.build_walsh_table(length // 2,        i1, mid_i, mid_j + 1,    j2, is_bar)
            self.build_walsh_table(length // 2, mid_i + 1,    i2,        j1, mid_j, is_bar)
            self.build_walsh_table(length // 2, mid_i + 1,    i2, mid_j + 1,    j2, not is_bar)

    def print_walsh_table(self):
        print("--------------Displaying walsh table--------------")
        for i in range(self.num_stations):
            for j in range(self.num_stations):
                print(str(self.wtable[i][j]) + " ", end='')
            print()
        print("--------------------------------------------------")

    def listen_to(self, source_station):
        inner_product = 0
        for i in range(self.num_stations):
            inner_product += self.copy[source_station - 1][i] * self.channel_sequence[i]

        k = inner_product / self.num_stations

        if k == 1:
            print("The data received from station " + str(source_station) + ": " + str(k))
        elif k == -1:
            print("The data received from station " + str(source_station) + ": 0")
        else:
            print("Station " + str(source_station) + " is idle, it didn't send any data")


if __name__ == "__main__":
    print("--------------CDMA Implementation--------------")

    input_num_stations = int(input("Enter number of stations: "))
    print("press  1 if station is sending bit 1")
    print("press -1 if station is sending bit 0")
    print("press  0 if station is idle")

    input_data = []
    for i in range(input_num_stations):
        input_data.append(int(input("enter for station " + str(i + 1) + ": ")))

    channel = CDMA(input_num_stations)
    channel.set_up(input_data)

    input_source_station = int(input("enter station you want to listen: "))
    channel.listen_to(input_source_station)
