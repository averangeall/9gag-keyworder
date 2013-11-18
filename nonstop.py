import database
import keyworder
import time

db = database.Database()
voc = keyworder.VocKeyworder()
meme = keyworder.MemeKeyworder()

dones = set()

while True:
    num_gags = 10
    gags = db.get_latest_gags(num_gags)
    cnt = 0
    for gag in gags:
        print gag
        gag_id = gag[0]
        title = gag[1]
        content_url = gag[2]

        if gag_id in dones:
            continue
        else:
            dones.add(gag_id)

        voc.add_keyword(gag_id, title)
        meme.add_keyword(gag_id, content_url)

    if cnt == 0:
        time.sleep(10)
