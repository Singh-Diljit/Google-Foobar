def solution(g):

    r, c = len(g), len(g[0]) #Dimensions of the matrix

    #Our runtime complexity is driven by the number of columns
    #so if r < c, transpose the matrix to speed up the program.
    if r < c:
        g = tuple(zip(*g))
        r, c = len(g), len(g[0])

    #The more restrictive row we start with the less false candidates
    #we will have to weed out. Since an entry of 1 is significantly
    #more restrictive than an entry of 0, reverse the row ordering
    #if it is easier to start at the last row.
    if sum(g[0]) < sum(g[-1]):
        g = g[::-1] 

    #Local preimages for an entry of 1
    inv = [
        [(0,), (0,)], [(0,), (1,)], [(1,), (0,)], [(1,), (1,)]]


    #The general plan of attack is to find local preimages,
    #on a column by column basis and then 'glue' the appropriate
    #blocks together to see how many we can end up with.

    
    for i in range(c):
        to_add = []
        
        if g[0][i]:
            
            while inv != []:

                x, y = inv[0][0], inv[0][1]
                val = x[-1] + y[-1] #val can be 0, 1, 2
                if val == 1:
                    to_add.append([x + (0,), y + (0,)])
                elif val == 0:
                    to_add.append([x + (1,), y + (0,)])
                    to_add.append([x + (0,), y + (1,)])
                    
                inv.pop(0) #In retrospect, it is faster to remove the last element
                    
        else:
        
            while inv != []:
                
                x, y = inv[0][0], inv[0][1]
                val = x[-1] + y[-1]
                to_add.append([x + (1,), y + (1,)])
                if val == 0:
                    to_add.append([x + (0,), y + (0,)])
                elif val == 1:
                    to_add.append([x + (0,), y + (1,)])
                    to_add.append([x + (1,), y + (0,)])
                else: #val == 2
                    to_add.append([x + (0,), y + (0,)])
                    to_add.append([x + (1,), y + (0,)])
                    to_add.append([x + (0,), y + (1,)])

                inv.pop(0)

        inv = to_add #Update running list of inverses

    #If there is only one row we only need to calculate the
    #inverse of the columns which we have done, so we have our
    #answer.
    if r == 1:
        return len(inv)

    seed = set() #Contain all paths we are considering
    hs = {} #'handshake hash' used to transfers path data as we go between columns
        
    for x in inv:
        seed.add(x[1])
        if hs.get(x[1]):
            hs[x[1]] += 1
        else:
            hs[x[1]] = 1

    #Similar logic applies here as it did for the column section above.
    #The main difference are the restrictions already in place which
    #seed and hs deal with as the issues come up.
    for row in range(1, r):

        gr, tmp = g[row], set()
        aux = {} #Auxiliary hash used to update handshake hash

        for x in seed:
            
            inv = [(0,), (1,)]
            for i in range(c):
                
                to_add, val = [], x[i] + x[i+1]
                if gr[i]:
                    while inv != []:
                        y = inv[0]
                        if val + y[i] == 0:
                            to_add.append(y + (1,))   
                        elif val + y[i] == 1:
                            to_add.append(y + (0,))

                        inv.pop(0)
                else:
                    while inv != []:
                        y = inv[0]
                        if val + y[i] == 0:
                            to_add.append(y + (0,))     
                        elif val + y[i] == 1:
                            to_add.append(y + (1,))     
                        else:
                            to_add.append(y + (0,))
                            to_add.append(y + (1,))

                        inv.pop(0)

                inv = to_add
            #Deal with any inconsistent blocks
            for y in inv:
                tmp.add(y)
                if aux.get(y):
                    aux[y] += hs[x]
                else:
                    aux[y] = hs[x]

        hs = {y: aux[y] for y in tmp} #Update the handshake hash
        seed = tmp #Update running list of seeds going into the next row

    return sum(hs.values())


if __name__ == "__main__":
    h = [[False]*10]*50
    print(solution(h))
