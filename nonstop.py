import database
import keyworder

db = database.Database()
meme = keyworder.MemeKeyworder()

while True:
    gags = db.get_latest_gags(100000)
    for gag in gags:
        gag_id = gag[0]
        content_url = gag[1]
        meme.add_keyword(gag_id, content_url)
