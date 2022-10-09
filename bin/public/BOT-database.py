#== init database ==
with open ("./bin/Global/DB/music_queue.db", mode="w", encoding="utf-8") as file :
    file.write("//本資料庫由電腦自動生成== encoding utf-8 ==//\n")
#====
class music_queue_db() :
    def add_songs(songs :list) :
        with open ("./bin/Global/DB/music_queue.db", mode="a", encoding="utf-8") as file :
            for song in songs :
                file.write(str(song))

    def songs_ouput(counts :int) :
        songs = []
        with open ("./bin/Global/DB/music_queue.db", mode="w+r", encoding="utf-8") as file :
            f = file.readline().strip("\n")
            if f == "//本資料庫由電腦自動生成== encoding utf-8 ==//\n" :
                pass
            else :
                songs.append(str(f))

            # for i in range(counts) :
            #     file.write(str(song))