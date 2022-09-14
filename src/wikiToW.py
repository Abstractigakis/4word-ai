import pandas as pd
import os 
import json
import numpy as np

COL_NAMES=['word', 'count']

def processRawWikiDataIntoPaginatedData():
    '''a utility that was used to do the inial processiong.  once we created the 4 word univers, we dont need to call this again'''
    
    pages = [{'a': int(filename.split('-')[0]),'b': int(filename.split('-')[1])} for filename in os.listdir("./data/raw_wiki/")]
    pages = sorted(pages, key=lambda d: d['a'])
    for pageNum, page in enumerate(pages):
        a = page['a']
        b = page['b']
        path = f"./data/raw_wiki/{a}-{b}"
        X = getCleanWikiData(path)
        pages[pageNum]["X"] = X 
        pages[pageNum]["n"] = len(X)

    df = pd.DataFrame(columns=COL_NAMES)

    for page in pages:
        df2 = pd.DataFrame(page['X'], columns=COL_NAMES)
        df = pd.concat([df, df2], ignore_index=True)

    df.to_csv('./data/4words/universe.csv', index=False)

    with open('./data/4words/universe.json', 'w') as f:
        json.dump(list(df['word']), f)
    return df

def getCleanWikiData(path:str) -> np.ndarray:
    with open(path) as f:
        res=[]
        for index, line in enumerate(f.readlines()):
            # ignore the first 3 lines of junk
            if index < 4:
                continue
            if index % 2 == 0:
                continue

            x = line.split("||")
            if len(x) > 1:
                w = x[1][3:-3]

                if len(w) == 4 and \
                    not "\'" in x[1] and \
                    not "\<" in x[1]:


                    nStr = ""
                    for c in x[2]:
                        seenFirstNum=False
                        if c in "0123456789":
                            seenFirstNum=True
                            nStr += c
                        elif not seenFirstNum:
                            continue
                        else :
                            break

                    n = int(nStr)

                    res.append([f"{w.upper()}", n])

        return res

if __name__ == "__main__":
    processRawWikiDataIntoPaginatedData()