# -*- coding: utf-8 -*-

"""
Implementation of a greedy solution for the cluster deletion problem for
cographs, and the complete multipartite graph completion problem.
"""


__author__ = 'David Schaller'


from asymmetree.cograph.Cograph import Cotree
from asymmetree.tools.GraphTools import complete_multipartite_graph_from_sets


def cluster_deletion(cograph):
    """Cluster deletion for cographs.
    
    Returns a partition of a cograph into disjoint cliques with a minimal
    number of edges between the cliques.
    """
    
    cotree = cograph if isinstance(cograph, Cotree) else Cotree.cotree(cograph)
    
    if not cotree:
        raise RuntimeError('not a valid cograph/cotree')
    
    P = {}
    
    for u in cotree.postorder():
        
        P[u] = []
        if not u.children:
            P[u].append([u.ID])
        
        elif u.label == 'parallel':
            for v in u.children:
                P[u].extend(P[v])
                
            # naive sorting can be replaced by k-way merge-sort
            P[u].sort(key=len, reverse=True)
        
        elif u.label == 'series':
            for v in u.children:
                for i, Q_i in enumerate(P[v]):
                    if i >= len(P[u]):
                        P[u].append([])
                    P[u][i].extend(Q_i)
        
        else:
            raise RuntimeError('invalid cotree')
    
    return P[cotree.root]


def complete_multipartite_completion(cograph, supply_graph=False):
    """Complete multipartite graph completion for cographs.
    
    Returns a partition of the vertex set corresponding to the (maximal)
    independent sets in an optimal edge completion of the cograph to a
    complete multipartite graph.
    
    Keyword arguments:
        supply_graph - additionally return the complete multipartite graph,
            default is False
    """
    
    cotree = cograph if isinstance(cograph, Cotree) else Cotree.cotree(cograph)
    
    if not cotree:
        raise RuntimeError('not a valid cograph/cotree')
        
    # complete multipartite graph completion is equivalent to 
    # cluster deletion in the complement cograph
    compl_cotree = cotree.complement(inplace=False)
    
    # clusters are then equivalent to the maximal independent sets
    independent_sets = cluster_deletion(compl_cotree)
    
    if not supply_graph:
        return independent_sets
    else:
        return (independent_sets,
                complete_multipartite_graph_from_sets(independent_sets))


if __name__ == '__main__':
    
    import asymmetree.tools.GraphTools as gt
    
    cotree = Cotree.random_cotree(10)
    print('---------- Random cotree ----------')
    print(cotree.to_newick())
    
    print('\n---------- Cluster deletion ----------')
    P = cluster_deletion(cotree)
    print(P)
    
    print('\n---------- CMG completion ----------')
    sets, cmg = complete_multipartite_completion(cotree, supply_graph=True)
    orig_cograph =  cotree.to_cograph()
    print(sets)
    print('original cograph is subgraph:',
          gt.is_subgraph(orig_cograph, cmg))
    