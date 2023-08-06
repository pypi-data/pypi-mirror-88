import networkx as nx
from dgnx.classes import DynamicDirectedGraph as ddg

def write_snapshots_to_gexf(DG):
    for t in DG.snapshots:
        f = open("graph_" + str(t) + '.gexf', 'w')
        i = nx.generate_gexf(DG.snapshots[t])
        for l in i:
            if l == '  <graph defaultedgetype="directed" mode="static" name="">':
                f.write('  <graph mode="slice" defaultedgetype="directed" timerepresentation="timestamp" timestamp=' + str(t) + '>')
            else:
                f.write(l)
            f.write("\n")
