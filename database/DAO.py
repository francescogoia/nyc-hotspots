from database.DB_connect import DBConnect
from model.location import Location


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllProviders():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct (Provider)
        from nyc_wifi_hotspot_locations nwhl 
        order by Provider asc 
        """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row["Provider"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getLocationOfProvider(provider):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct Location
        from nyc_wifi_hotspot_locations nwhl 
        where Provider = %s
        """
        cursor.execute(query, (provider, ))
        result = []
        for row in cursor:
            result.append(row["Location"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getLocationOfProviderV2(provider):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select Location , avg(Latitude) as lat, avg(Longitude) as lon
            from nyc_wifi_hotspot_locations nwhl 
            where Provider = %s
            group by Location
            order by Location asc
            """
        cursor.execute(query, (provider,))
        result = []
        for row in cursor:
            result.append(Location(row["Location"], row["lat"], row["lon"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(provider):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select n1.Location as n1Loc, n2.Location as n2Loc, avg(n1.Latitude) as n1Lat, avg(n2.Latitude) as n2Lat, avg(n1.Longitude) as n1Long, avg(n2.Longitude) as n2Long
                from nyc_wifi_hotspot_locations n1, nyc_wifi_hotspot_locations n2
                where n1.Provider = n2.Provider and n2.Provider = %s
                    and n1.Location < n2.Location 
                group by n1.Location, n2.Location 
                """
        cursor.execute(query, (provider,))
        result = []
        for row in cursor:
            loc1 = Location(row["n1Loc"], row["n1Lat"], row["n1Long"])
            loc2 = Location(row["n2Loc"], row["n2Lat"], row["n2Long"])
            result.append((loc1, loc2))

        cursor.close()
        conn.close()
        return result


if __name__ == "__main__":
    d = DAO()
    d.getAllProviders()