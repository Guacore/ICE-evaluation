################################################################################
#        ______                    ______                            __        #
#       /  _/ /____  ____ ___     / ____/___  ____  ________  ____  / /_       #
#       / // __/ _ \/ __ `__ \   / /   / __ \/ __ \/ ___/ _ \/ __ \/ __/       #
#     _/ // /_/  __/ / / / / /  / /___/ /_/ / / / / /__/  __/ /_/ / /_         #
#    /___/\__/\___/_/ /_/ /_/   \____/\____/_/ /_/\___/\___/ .___/\__/         #
#                                                         /_/                  #
#            ______          __             __    ___                          #
#           / ____/___ ___  / /_  ___  ____/ /___/ (_)___  ____ _              #
#          / __/ / __ `__ \/ __ \/ _ \/ __  / __  / / __ \/ __ `/              #
#         / /___/ / / / / / /_/ /  __/ /_/ / /_/ / / / / / /_/ /               #
#        /_____/_/ /_/ /_/_.___/\___/\__,_/\__,_/_/_/ /_/\__, /                #
#                                                       /____/ credit: patorjk #
################################################################################

# Proj: Item Concept Embedding (ICE)
# File: table_3.py
# Cont:
#   Clas:
#       1) NetStat
#   Func:
#       1) get_avg_degree                   2) display_stat_table

from tqdm import tqdm

class NetStat():
    """
    Store configuration statistics for network.
    """

    def __init__(self):
        """ Constructor for NetStat.
        Param:
            param1 [self] reference to this object.
        """
        self.V = set()       # song cardinality
        self.T = set()       # word cardinality
        self.E_et = set()    # num of rep words defined in ET relation
        self.E_tt = set()    # num of exp words defined in TT relation
        self.E̅_et = set()    # num of exp words found by concept exp

    def get_avg_degree(self):
        """ Calculate average degree of the network.
        Param:
            param1 [self] reference to this object.
        """
        s = len(self.V)
        w = len(self.T)
        d = 2*(len(self.E_et)+len(self.E_tt)/2+len(self.E̅_et)) # discount bidir
        return "{0:.1f}".format(d/(s+w))

def display_stat_table(net_list, top_list, stat_list):
    """ Display network stats in format.
    Param:
        param1 [list] of network names.
        param2 [list] of all representative word dimensions for networks.
        parma3 [list] of NetStat used to record network stats.
    """
    # Step 1: Display table titles.
    print("\t" + (len(top_list)*"\t").join(net_list))
    print("|W|\t" + "\t".join(len(net_list)*["\t".join(top_list)]))

    # Step 2: Display network stats.
    print("|V|\t" + "\t".join([str(len(s.V)) for s in stat_list]))
    print("|T|\t" + "\t".join([str(len(s.T)) for s in stat_list]))
    print("|E_et|\t" + "\t".join([str(len(s.E_et)) for s in stat_list]))
    print("|E_tt|\t" + "\t".join([str(len(s.E_tt)) for s in stat_list]))
    print("|E̅_et|\t" + "\t".join([str(len(s.E̅_et)) for s in stat_list]))
    print("d̅\t" + "\t".join([str(s.get_avg_degree()) for s in stat_list]))

def main():
    # Step 1: Setup.
    top_list = ["top1", "top3", "top5", "top8", "top10"]
    net_list = ["BPT", "ICE(x3)"]

    et_load_path = "./graph-table_3/et_relation/et_"
    ice_load_path = "./graph-table_3/ice_network/ice_full-" 

    stat_list = []

    # Step 2: Calculate stats for bipartite networks.
    print("Calculating BPT network stats...")
    for top in tqdm(top_list):
        bpt_path = et_load_path + top + "_w0.edge"

        bpt_stat = NetStat()
        with open(bpt_path) as et:
            for line in et:
                entry = line.split()
                bpt_stat.V.add(entry[0])
                bpt_stat.T.add(entry[1])
                bpt_stat.E_et.add(line)

        stat_list.append(bpt_stat)

    # Step 3: Calculate stats for ICE networks.
    print("Calculating ICE network stats...")
    for top in tqdm(top_list): 
        et_path = et_load_path + top + "_w0.edge"
        ice_path = ice_load_path + top + "x3_w0.edge" 

        ice_stat = NetStat()
        with open(et_path) as et, open(ice_path) as ice:
            for line in et:
                entry = line.split()
                ice_stat.V.add(entry[0])
                ice_stat.E_et.add(line)
            for line in ice:
                entry = line.split()
                ice_stat.T.add(entry[1])
                if entry[0][0] == "w": # count twice for bidirection
                    ice_stat.E_tt.add(line)
                elif line not in ice_stat.E_et: 
                    ice_stat.E̅_et.add(line)

        stat_list.append(ice_stat)

    # Step 4: Display network stats.
    display_stat_table(net_list, top_list, stat_list)

if __name__ == "__main__":
    main()
