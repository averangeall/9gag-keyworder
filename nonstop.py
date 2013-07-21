import database
import keyworder

db = database.Database()
voc = keyworder.VocKeyworder()
meme = keyworder.MemeKeyworder()

while True:
    gags = db.get_latest_gags(100000)
    for gag in gags:
        print gag
        gag_id = gag[0]
        title = gag[1]
        content_url = gag[2]
        voc.add_keyword(gag_id, title)
        meme.add_keyword(gag_id, content_url)
