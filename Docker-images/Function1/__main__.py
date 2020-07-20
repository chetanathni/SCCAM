
def aggregate(BangaloreNorth,BangaloreSouth):
    return {'result':(BangaloreNorth+BangaloreSouth)/2}

#print(aggregate(BangaloreNorth , BangaloreSouth))
def main(args):
    BangaloreNorth = args[2]
    BangaloreSouth = args[3]
    aggregate(BangaloreNorth,BangaloreSouth)