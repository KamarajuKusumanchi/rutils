# tags | distribute N element array over p workers, break array into smaller
# chunks

import pandas as pd

def chunkify(N, p):
    # assume N >0, p>0
    quotient = int(N/p)
    remainder = N % p
    nelem = pd.Series([quotient]* p)
    nelem[0:remainder] += 1
    indexList = pd.Series([0]).append(nelem.cumsum())

    res = pd.DataFrame({'indexLow': indexList[0:p].values,
                        'indexHigh': indexList[1:p+1].values})
    res['nelem'] = nelem
    return res

a = chunkify(12, 4)
print(a)
a = chunkify(13, 4)
print(a)
a = chunkify(14, 4)
print(a)
a = chunkify(15, 4)
print(a)
a = chunkify(16, 4)
print(a)