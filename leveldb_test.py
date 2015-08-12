import leveldb

db = leveldb.LevelDB('/home/elvijs/.btcd/data/mainnet/blocks_leveldb')

count = 0
for elem in db.RangeIter():
    count += 1
    print(elem)
    if count > 5:
        break
