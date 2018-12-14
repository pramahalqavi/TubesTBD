library("igraph")

fbGraph <- read.table("facebook_combined.txt")
net <- graph.data.frame(fbGraph)
net <- as.undirected(net)
# plot(net)

# Density - The proportion of present edges from all possible edges in the network.
edge_density(net, loops=F)

# Transitivity - This is simply the ratio of the triangles and the connected triples in the graph.
transitivity(net, type="average")

# Diameter - A network diameter is the longest geodesic distance (length of the shortest path between two nodes) in the network.
diameter(net, directed=F, weights=NA)
diam <- get_diameter(net, directed=F, weights=NA)
diam

# Node degrees
deg <- degree(net, mode="all")
hist(deg, breaks=1:1100, main="Histogram of node degree")

# Community detection - Detect groups that consist of densely connected nodes with fewer connections across groups.
# based on greedy optimization of modularity
cfg <- cluster_fast_greedy(as.undirected(net))
plot(cfg, as.undirected(net))

class(cfg)
length(cfg)
membership(cfg)
modularity(cfg)






