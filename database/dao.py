from database.DB_connect import DBConnect
from model.album import Album

class DAO:
    @staticmethod
    def getAlbumByDurata(durataMinima):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """    SELECT a.id ,a.title , a.artist_id , SUM(t.milliseconds )/60000 as durata
                        FROM album a , track t 
                        WHERE  a.id = t.album_id 
                        GROUP BY a.id ,a.title , a.artist_id 
                        HAVING durata > %s
                    """

        cursor.execute(query, (durataMinima,))

        for row in cursor:
            result.append(Album(**row))
        print(result)


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def connessioni(dictalbum):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """    SELECT DISTINCT t1.album_id as id1, t2.album_id as id2
                        FROM playlist_track pt1, playlist_track pt2 , track t1, track t2  
                        WHERE t1.id =pt1.track_id 
                        AND t2.id  = pt2.track_id 
                        and pt1.playlist_id  = pt2.playlist_id 
                        and pt1.track_id < pt2.track_id 
                        and t1.album_id  <t2.album_id 
                """

        cursor.execute(query,)

        for row in cursor:
            a1 = dictalbum.get(row["id1"])
            a2 = dictalbum.get(row["id2"])
            if a1 is not None and a2 is not None:
                result.append((a1, a2))

        cursor.close()
        conn.close()
        return result