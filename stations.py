# This is the page for class definitiaon and initialisation, as well as some function making
# as well as dictionaries and arrays
import csv


class Station:
    def __init__(self, given_name, given_name_full, given_locations, given_num):
        self.name = given_name
        self.name_full = given_name_full
        # Locations are arrays of 5 characters, 2 pairs of 2
        self.locations = given_locations
        # Number is decided by this code, just for route finding
        self.num = given_num
        self.directions = [[0 for _ in range(len(self.locations))] for _ in range(len(self.locations))]
        self.directions_acc = [[0 for _ in range(len(self.locations))] for _ in range(len(self.locations))]

    def station_pathing_routes(self, start, end, access):
        if access == 0:
            return self.directions_acc[self.locations.index(start)][self.locations.index(end)]
        elif access == 1:
            return self.directions[self.locations.index(start)][self.locations.index(end)]
        else:
            print("Invalid Access Given")

    def location_arr(self, loc):
        return self.locations.index(loc)

    def dir_update(self, start, end, access, change):
        if access == 0:
            self.directions_acc[self.locations.index(start)][self.locations.index(end)] = change
        elif access == 1:
            self.directions[self.locations.index(start)][self.locations.index(end)] = change


class Lines:
    def __init__(self, given_name, given_name_full, given_colour, given_directions, given_ends, given_num):
        self.name = given_name
        self.name_full = given_name_full
        self.colour = given_colour
        self.directions = given_directions
        self.ends = given_ends
        self.num = given_num


def station_num_to_name(num):
    return station_list[station_array[num]].name_full


def station_num_to_object(num):
    return station_list[station_array[num]]


def station_name_to_num(name):
    return station_list[name].num


def station_name_to_object(name):
    return station_list[name]


def line_num_to_col(num):
    return line_list[line_array[num]].colour


def line_num_to_name(num):
    return line_list[line_array[num]].name_full


def plat_change_calc(line, direction, old_line, old_direction):
    ending = plat_change_calc_depth(line, direction)
    starting = plat_change_calc_depth(old_line, old_direction)

    return starting, ending


def plat_change_calc_depth(line, direction):
    # First part
    over_all = ""
    if line == 0:
        over_all = over_all + "BK"
    elif line == 9:
        over_all = over_all + "VI"
    # middle part
    over_all = over_all + "_"
    # End part, dir
    if direction == "Northbound":
        over_all = over_all + "NB"
    elif direction == "Southbound":
        over_all = over_all + "SB"
    return over_all


def lines_dir_and_bound(stop1_g, stop2_g, line):
    stop1 = station_array[stop1_g]
    stop2 = station_array[stop2_g]
    if line == 0:
        if BK_list.index(stop1) < BK_list.index(stop2):
            return "Northbound", BK.ends[1]
        else:
            return "Southbound", BK.ends[0]
    elif line == 9:
        if VI_list.index(stop1) < VI_list.index(stop2):
            return "Northbound", VI.ends[1]
        else:
            return "Southbound", VI.ends[0]
    else:
        print("Non existant line num (that or i havent coded it yet)")


def calc_directions():
    # Csv format:
    # Station short hand, start location shorthand, end location short hand, access, description
    with open('dir.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for item in csv_reader:
            if len(item) != 1:
                station = station_name_to_object(item[0])
                start = item[1]
                end = item[2]
                access = int(item[3])
                loaded_directions = item[4:]

                if access == 0:
                    station.dir_update(start, end, access, loaded_directions)
                elif access == 1:
                    station.dir_update(start, end, access, loaded_directions)
                else:
                    print("invalid access")


def make_station_mtx():
    rows, cols = (11, 11)
    st_mx = [[0 for _ in range(cols)] for _ in range(rows)]
    st_ln = [[-1 for _ in range(cols)] for _ in range(rows)]
    # Add to matrix:
    # Vic line
    st_mx[VIC.num][GRN.num] = 1
    st_mx[GRN.num][OXF.num] = 1
    st_mx[OXF.num][WAR.num] = 1
    st_mx[WAR.num][EUS.num] = 1
    st_mx[EUS.num][KNG.num] = 1
    st_ln[VIC.num][GRN.num] = VI.num
    st_ln[GRN.num][OXF.num] = VI.num
    st_ln[OXF.num][WAR.num] = VI.num
    st_ln[WAR.num][EUS.num] = VI.num
    st_ln[EUS.num][KNG.num] = VI.num

    # Bakerloo line
    st_mx[OXF.num][REG.num] = 1
    st_mx[REG.num][BKS.num] = 1
    st_mx[BKS.num][MYL.num] = 1
    st_mx[MYL.num][EDR.num] = 1
    st_mx[EDR.num][PAD.num] = 1
    st_ln[OXF.num][REG.num] = BK.num
    st_ln[REG.num][BKS.num] = BK.num
    st_ln[BKS.num][MYL.num] = BK.num
    st_ln[MYL.num][EDR.num] = BK.num
    st_ln[EDR.num][PAD.num] = BK.num

    # Reflect it:
    for row in range(0, len(st_mx)):
        for col in range(0, len(st_mx)):
            if st_mx[row][col] != 0:
                st_mx[col][row] = st_mx[row][col]
            if st_ln[row][col] != -1:
                st_ln[col][row] = st_ln[row][col]
    return st_mx, st_ln


# Fist 2 are station, second 2 are north, east, south or west bount, except the first 2 which are:
# OV_GR = Over Ground, ST_SD is Street Side
all_locations = ["OV_GR", "ST_SD", "BK_NB", "BK_SB", "CE_EB", "CE_WB", "CC_EB", "CC_WB", "DI_EB", "DI_WB", "HM_EB",
                 "HM_WB", "JU_NB", "JU_SB", "MT_EB", "MT_WB", "NO_NB", "NO_SB", "PI_EB", "PI_WB", "VI_NB", "VI_SB"]

# All lines are refered to as their initial 2 Letters
BK = Lines("BK", "Bakerloo", "Brown", "NS", ["Elephant and Castle", "Harrow and Wealdstone"], 0)
CE = Lines("CE", "Central", "Red", "EW", ["West Ruislip", "Epping"], 1)
CC = Lines("CC", "Circle", "Yellow", "EW", ["Edgewhere", "Hammersmith"], 2)
DI = Lines("DI", "District", "Green", "EW", ["Ealing Broadway", "Upminster"], 3)
HM = Lines("HM", "Hammersmith", "Pink", "EW", ["Barking", "Hammersmith"], 4)
JU = Lines("JU", "Jubilee", "Gray", "NS", ["Stanmore", "Stradford"], 5)
MT = Lines("MT", "Metropolotan", "Purple", "EW", ["Aldgate", "Uxbridge"], 6)
NO = Lines("NO", "Northern", "Black", "NS", ["High Barnet", "Morden"], 7)
PI = Lines("PI", "Piccadilly", "Dark Blue", "EW", ["Cockfosters", "Heathrow"], 8)
VI = Lines("VI", "Victoria", "Light Blue", "NS", ["Brixton", "Walthamstone Central"], 9)

line_list = {"BK": BK, "CE": CE, "CC": CC, "DI": DI, "HM": HM, "JU": JU, "MT": MT, "NO": NO, "PI": PI, "VI": VI}
line_array = ["BK", "CE", "CC", "DI", "HM", "JU", "MT", "NO", "PI", "VI"]

VIC = Station("VIC", "Victoria", ["OV_GR", "ST_SD", "CC_EB", "CC_WB", "DI_EB", "DI_WB", "VI_NB", "VI_SB"], 0)
GRN = Station("GRN", "Green Park", ["ST_SD", "JU_NB", "JU_SB", "PI_EB", "PI_WB", "VI_NB", "VI_SB"], 1)
OXF = Station("OXF", "Oxford Circus", ["ST_SD", "BK_NB", "BK_SB", "CE_EB", "CE_WB", "VI_NB", "VI_SB"], 2)
WAR = Station("WAR", "Waren Street", ["ST_SD", "NO_NB", "NO_SB", "VI_NB", "VI_SB"], 3)
EUS = Station("EUS", "Eusten", ["OV_GR", "ST_SD", "NO_NB", "NO_SB", "VI_NB", "VI_SB"], 4)
KNG = Station("KNG", "Kings Cross St Pancras",
              ["OV_GR", "ST_SD", "CC_EB", "CC_WB", "HM_EB", "HM_WB", "MT_EB", "MT_WB", "NO_NB", "NO_SB", "PI_EB",
               "PI_WB", "VI_NB", "VI_SB"], 5)

REG = Station("REG", "Regent Park", ["ST_SD", "BK_NB", "BK_SB"], 6)
BKS = Station("BKS", "Bakers Street",
              ["ST_SD", "BK_NB", "BK_SB", "CC_EB", "CC_WB", "HM_EB", "HM_WB", "JU_NB", "JU_SB", "MT_EB", "MT_WB"],
              7)
MYL = Station("MYL", "Marylbone", ["OV_GR", "ST_SD", "BK_NB", "BK_SB"], 8)
EDR = Station("EDR", "Edgeware Road", ["ST_SD", "BK_NB", "BK_SB"], 9)
PAD = Station("PAD", "Paddington",
              ["OV_GR", "ST_SD", "BK_NB", "BK_SB", "CC_EB", "CC_WB", "DI_EB", "DI_WB", "HM_EB", "HM_WB"], 10)

station_list = {"VIC": VIC, "GRN": GRN, "OXF": OXF, "WAR": WAR, "EUS": EUS, "KNG": KNG, "REG": REG, "BKS": BKS,
                "MYL": MYL, "EDR": EDR, "PAD": PAD}
station_array = ["VIC", "GRN", "OXF", "WAR", "EUS", "KNG", "REG", "BKS", "MYL", "EDR", "PAD"]

# if a stop is greater than annother, it is more north
VI_list = ["VIC", "GRN", "OXF", "WAR", "EUS", "KNG"]
# If greater then North
BK_list = ["OXF", "REG", "BKS", "MYL", "EDR", "PAD"]

calc_directions()

station_matrix, lines_matrix = make_station_mtx()