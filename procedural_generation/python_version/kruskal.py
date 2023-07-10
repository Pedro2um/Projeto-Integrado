




def find(roots, i):
    
    while( i != roots[i]):
        roots[i] = roots[roots[i]]
        i = roots[i]

    return i

def union(roots, weights, p, q):
    i = find(roots, p)
    j = find(roots, q)
    
    if( i == j ):
        return 
    
    if weights[j] > weights[i]:
        roots[i] = j
        weights[j] += weights[i]
    else:
        roots[j] = i
        weights[i] += weights[j]


def kruskal(points, edges):
    
    roots = []
    weights = []
    
    N = len(points)
    for i in range(N):
        roots.append(i)
        weights.append(1)
        
    edges = sorted(edges, key = lambda edge : edge[2])
    
    
    mst = []
    #print(edges)
    
    index = 0 
    while len(mst) != N -1:
        p1, p2, w = edges[index]
        
        i = find(roots, p1)
        j = find(roots, p2)
        
        if i != j:
            mst.append((p1 ,p2))
            union(roots, weights, i, j)
    
        index +=1
    
    
    return mst
        