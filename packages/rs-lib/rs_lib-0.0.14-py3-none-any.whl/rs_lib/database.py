import psycopg2

from .config import Config


def get_io(camera_id, cone_id, date, conf : Config):
    config = conf.get()

    if cone_id == "" or cone_id == "None" or cone_id == "Na":
        cone_id = "0"

    conn = psycopg2.connect(
        "host={host} port={port} dbname={name} user={user} password={pswd}".format(
            host=config.get("RemoteSensingDb", "Host"),
            port=config.get("RemoteSensingDb", "Port"),
            name=config.get("RemoteSensingDb", "Name"),
            user=config.get("RemoteSensingDb", "User"),
            pswd=config.get("RemoteSensingDb", "Password"),
        )
    )

    cur = conn.cursor()
    query = "SELECT * FROM {}.{} WHERE camera_id = '{}' AND cone_id = '{}' AND calibration_date < '{}' ORDER BY calibration_date DESC LIMIT 1".format(
        config.get("RemoteSensingDb", "Schema"),
        config.get("RemoteSensingDb", "Table"),
        str(camera_id),
        cone_id,
        date
    )

    print("Get camera orientations from camera_calibrations database: \n"+query+"\n")

    cur.execute(query)
    result = cur.fetchone()

    if result is None:
        raise ValueError("Error: Camera '{}' not found in database".format(camera_id))

    focal_length = float(result[1]) * (-1)  # 100.5
    pixel_size = result[2] / 1000  # 0.006
    x_ppa = float(result[3])  # (-18)
    y_ppa = float(result[4])  # (0)
    image_extent_x = float(result[5])  # -34.008
    image_extent_y = float(result[6])  # -52.026
    mount_rotation = result[13]

    return [x_ppa, y_ppa, focal_length, pixel_size, image_extent_x, image_extent_y, mount_rotation]
    


def get_db_conn(conf : Config):
    config = conf.get()

    conn = psycopg2.connect(
        "host={host} port={port} dbname={name} user={user} password={pswd}".format(
            host=config.get("GruDb", "Host"),
            port=config.get("GruDb", "Port"),
            name=config.get("GruDb", "Name"),
            user=config.get("GruDb", "User"),
            pswd=config.get("GruDb", "Password"),
        )
    )

    return conn
