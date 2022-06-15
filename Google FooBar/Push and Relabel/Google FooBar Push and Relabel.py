def solution(entrances, exits, path):
    
    V = list(range(len(path))) #Vertices in our original graph
    n, V_Extended = len(path) + 2, list(range(len(path) + 2))

    #By adding a universal source and sink we can simplify the code down the line
    source, sink = n - 1, n - 2

    #We will work  primarily on an adjacency matrix which we build here
    Adj = [x + [0,0] for x in path]
    Adj += [[0] * n, [0] * n]
    for v in entrances:
        Adj[source][v] = sum(Adj[v])
    for u in exits:
        exit_col = [Adj[i][u] for i in V]
        Adj[u][sink] = sum(exit_col)

    #Define and initialize the following hashes:
    #flow: the amount of flow passing between two vertices
    #runover: the excess flow at a vertex
    #rank: a vertex hierarchy for deciding where runover flow can be pushed to
    #seen: keeps track of neighbors seen by our vertex while it is at a fixed rank
    flow, rank, runover, seen = {}, {}, {}, {}
    for u in V_Extended:
        rank[u], runover[u], seen[u] = 0, 0, 0
        for v in V_Extended:
            flow[(u,v)] = 0

    #The universal source is as 'uphill' as can be, so it has rank n = len(path),
    #and flow has nowhere to go but down
    rank[source] = n

    #Setting the runover of the universal source will ensures the source
    #can saturate every vertex in 'entrances'
    runover[source] = sum(Adj[source])

    def push(u, v):
    #The push procedure, if applicable will transfer as
    #much flow as possible from vertex u to vertex v
        flow_to_push = min(runover[u], Adj[u][v] - flow[(u,v)])
        flow[(u,v)] += flow_to_push
        flow[(v,u)] -= flow_to_push
        runover[u] -= flow_to_push
        runover[v] += flow_to_push

    def relabel(u):
    #The relabel procedure, if applicable will change the
    #rank of vertex u to ensure the push procedure can run
        lower_bound = n + 1
        for v in V_Extended:
            if Adj[u][v] - flow[(u,v)] > 0:
                lower_bound = min(lower_bound, rank[v])
                rank[u] = 1 + lower_bound

    def PUSH_and_RELABEL(u):
        
        while runover[u] > 0: #only push or relabel if our vertex has positive runover flow
            if seen[u] < n:
                v = seen[u]
                if Adj[u][v] - flow[(u,v)] > 0 and rank[u] > rank[v]:
                    #Vertex v can handle more flow and is of lower rank
                    #than vertex u, so we can push flow from u to v
                    push(u, v)
                else:
                    #Since u is still a candidate for  the push procedure,
                    #iterate v to attempt to push flow from u to a new vertex
                    seen[u] += 1 
            else:
                #Vertex u still has excess flow but rank[u] is obstructing the
                #push procedure so relabel the rank of u.
                relabel(u)
                #Because seen[u] tracks vertices while u is a fixed rank,
                #and the rank of u was just changed, we have to reset seen[u]
                seen[u] = 0

    for v in V_Extended:
        #Snowball the algorithm by pushing flow from source to 'entrances'
        push(source, v)
        
    i = 0
    while i in V:
        u = V[i]
        old_rank = rank[u]
        PUSH_and_RELABEL(u)
        if rank[u] > old_rank:
            #If we relabeled, then restart from the front of the list
            V.insert(0, V.pop(i))
            i = 0
        else:
            #If we did not have to relabel, keep iterating through vertices
            i += 1
            
    return sum([flow[(source,i)] for i in V_Extended])


if __name__ == "__main__":
    ent, ex = [0], [3]
    path = [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]
    print(solution(ent, ex, path))
