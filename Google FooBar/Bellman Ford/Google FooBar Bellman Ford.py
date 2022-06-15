def solution(times, time_limit):

    n = len(times)
    start, end, V = 0, n - 1, list(range(n))
    E = [(u, v) for u in V for v in V] #Edge set

    #The shortest path from x -> y, is the one that takes the least amount
    #of time not the path visiting the least number of nodes

    #dist[x][y] will be the minimum time to go from x -> y
    dist = [[float('inf')] * n for i in V]

    #path_key[x][y] will be the penultimate node on the shortest path from x -> y
    path_key = [[None] * n for i in V]

    for v in V:
        if times[v][v] < 0:
            #If staying on this node results in time being added
            #then we can exploit this property to save every bunny
            return [i for i in range(n - 2)]
        else:
            dist[v][v] = 0

    def Bellman_Ford(i):
        #Finds the shortest path from i -> v
        counter = 0
        while counter != n - 1:
            counter += 1
            for e in E:
                u, v = e[0], e[1]
                if dist[i][u] + times[u][v] < dist[i][v]:
                    dist[i][v] = dist[i][u] + times[u][v]
                    path_key[i][v] = u

    #Initially perform Bellman_Ford for a fixed vertex
    #and check for any time-adding loops
    Bellman_Ford(start)
            
    for e in E:
        u, v = e[0], e[1]
        if dist[start][u] + times[u][v] < dist[start][v]:
            #There exists a time-adding loop
            #so exploit the loop to save every bunny
            return [i for i in range(n - 2)]

    for v in range(1, n):
        #Perform Bellman_Ford for all v except
        #the node: start = 0, as this was already done
        Bellman_Ford(v)

    def shortest_path(x, y):
        #Using path_key return the unique nodes visited going from x -> y
        if x == y:
            #An artifact of path_key[v][v] being 'None' for every node, v
            return {x}
        seen = {x, y}
        prev = path_key[x][y]
        while prev != x:
            seen.add(prev)
            prev = path_key[x][prev]
        return seen

    def bunnies_visited(path):
        #Bunnies encountered on a path (= string of nodes)
        #using the fact we travel between two nodes
        #using the shortest_path function (that is the actual nodes
        #traversed may be more than just the nodes on the path.
        visited = {v for v in path}
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            visited.update(shortest_path(u, v))
        return {v for v in visited if v not in {start, end}}

    def path_to_node(path, v):
        #Checks if a given path can visit node v while
        #still ensuring enough time to reach 'end'?
        time_in_path = [dist[path[i]][path[i + 1]] for i in range(len(path) - 1)]
        time_left = time_limit - sum(time_in_path)
        if dist[path[-1]][v] + dist[v][end] > time_left:
            return False
        return True

    def feasable_to_save(path):
        #List of bunnies not yet saved that we can feasibly save in the next step
        remaining = [i for i in range(1,n-1) if i not in bunnies_visited(path) ]
        return [i for i in remaining if path_to_node(path, i) ]

    def better_path(path1, path2):
        #Tells us which of two paths saves the most bunnies,
        #ties are settled by the sum of the bunnie's I.D.'s.
        bunnies1, bunnies2 = bunnies_visited(path1), bunnies_visited(path2)
        if len(bunnies1) > len(bunnies2):
            return path1
        elif len(bunnies2) > len(bunnies1):
            return path2
        
        #In case of tie
        return path1 if sum(bunnies1) < sum(bunnies2) else path2


    Paths = [[start]] #list of all paths being considered
    best = [] #the best path, as determined by better_path

    while Paths !=[]:

        New_Paths = []
        for path in Paths:
            
            next_bunny = feasable_to_save(path)   
            if next_bunny == []: #We are done adding to this path
                #Add any nodes on the way to the bulkhead
                path += shortest_path(path[-1], end) 
                best = better_path(best, path) #Makes sure we are looking at the best path
            
            for bunny in next_bunny:
                foo = [x for x in path]
                foo.append(bunny)
                New_Paths.append(foo)
                foo = []
                
        Paths = [x[:] for x in New_Paths]
        

    bunnies_saved = [x-1 for x in bunnies_visited(best)] #Vertex i is bunny i-1.
    bunnies_saved.sort()
    
    return bunnies_saved
