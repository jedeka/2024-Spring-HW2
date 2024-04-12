liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

res = {}
TOKENS = set(['tokenA', 'tokenB', 'tokenC', 'tokenD', 'tokenE'])

def update_liquidity(pair, new_liquidity, liq=liquidity):
    liq[pair] = new_liquidity

def swap(input, x, y):
    """Swap tokens with `input` amount"""
    input *= 0.997 # 0.3% cost
    new_x = x + input
    new_y = (x * y)/(new_x)
    output = y - new_y
    return output, new_x, new_y

def print_dict(a):
    for k, v in a.items():
        print(f'{k} : {v}')

def find():
    """BFS-esque algorithm to search the goal of tokenB >= 20 units"""
    
    node,visited = "tokenB", set() 
    current = (5, node)
    queue = [(node, ['tokenB'], current[0], liquidity.copy())]
    visited.add(node)
    best = 0
    while queue:
        node, path, balance, liq = queue.pop(0)

        # list successors 
        successors = sorted(TOKENS - set([node]))
        pathstr = ''
        for i, p in enumerate(path): pathstr += p + '->'
        pathstr = pathstr.rstrip('->') # strip arrow for final
        
        for successor in successors:
            # copy current liquidity
            liq_cp = liq.copy()

            # swap and update liquidity if current successor is taken
            reverse = False if (node, successor) in liquidity else True
            if not reverse:
                pair = (node, successor)
                liq_node, liq_successor = liquidity[(pair[0], pair[1])]
            else:
                pair = (successor, node)
                liq_successor, liq_node = liquidity[(pair[0], pair[1])]
            # swap token from liquidity pool
            output_amt, new_node, new_successor = swap(balance, liq_node, liq_successor)
            if not reverse: 
                update_liquidity(pair, (new_node, new_successor), liq=liq_cp)
            else:
                update_liquidity(pair, (new_successor, new_node), liq=liq_cp)

            # check if the successor is tokenB with amount >= 20 units
            successor_path = pathstr + f'->{successor}'
            # if successor == 'tokenB' and output_amt >= 20:
            #     return successor_path, output_amt
            if successor == 'tokenB':
                if output_amt >= 20:
                    res[successor_path] = output_amt
                
                    if output_amt > best:
                        best = output_amt
                        print(f"* current best: {successor_path}, with amount: {output_amt}")
                
                if output_amt >= 30:
                    return successor_path, output_amt
            
            # update frontiers            
            queue.append((successor, path + [successor], output_amt, liq_cp))


path, balance = find()
# print(res)
# path, balance = dfs("tokenB", ["tokenB"], 5, liquidity)
print(f"path: {path}, tokenB balance={balance}")

