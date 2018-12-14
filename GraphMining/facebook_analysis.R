library("igraph")

fbGraph <- read.table("facebook_combined.txt")
net <- graph.data.frame(fbGraph)
net <- as.undirected(net)
# plot(net)

# Density - The proportion of present edges from all possible edges in the network.
edge_density(net, loops=F)

# Transitivity - global - ratio of triangles (direction disregarded) to connected triples.
transitivity(net, type="global")

# Diameter - A network diameter is the longest geodesic distance (length of the shortest path between two nodes) in the network.
diameter(net, directed=F, weights=NA)
diam <- get_diameter(net, directed=F, weights=NA)
diam

# Node degrees
deg <- degree(net, mode="all")
hist(deg, breaks=1:1100, main="Histogram of node degree")

# Community detection - Detect groups that consist of densely connected nodes with fewer connections across groups.
# based on propagating labels
clp <- cluster_label_prop(net)
plot(clp, net)

class(clp)
length(clp)
membership(clp)
modularity(clp) # how modular the graph partitioning is

# based on greedy optimization of modularity
cfg <- cluster_fast_greedy(as.undirected(net))
plot(cfg, as.undirected(net))


