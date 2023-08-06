import psycopg2
from datetime import datetime

from .database import get_io, get_db_conn
from .config import Config
from .rs_lib import ray, bounding_box, create_def
from .gru_util import gdal_translate_str


def minion_manager(job_type, path_bat_file, created_by, wkt, priority, conf : Config):
    conn = get_db_conn(conf)
    cur = conn.cursor()
    config = conf.get()

    geometry = "ST_GeomFromText('" + wkt +"',25832)"

    query = "INSERT INTO {db_schema}.{db_table} (job_type, job_status, progress, path_bat_file, priority, creation_time, created_by, geom) VALUES ('{job_type}', '{job_status}', '{progress}', '{path_bat_file}', {priority}, '{creation_time}', '{created_by}', {geometry})".format(
        db_schema=config.get("GruDb", "Schema"),
        db_table=config.get("GruDb", "Table"),
        job_type=job_type,
        job_status="Pending",
        progress=0,
        path_bat_file=path_bat_file,
        priority=priority,
        creation_time=str(datetime.now()),
        created_by=created_by,
        geometry=geometry
    )

    print("Insert '{job_type}'-job into job queue: \n{sql}\n".format(job_type, query))
    cur.execute(query)

    conn.commit()


def gru_orto(schema, table, priority, conf : Config):
    print("Checking for new Ortho Photo Jobs")

    conn = get_db_conn(conf)
    cur = conn.cursor()
    config = conf.get()
    
    try:
        cur = conn.cursor()
        query = "SELECT imageid," \
            "easting," \
            "northing," \
            "height," \
            "omega," \
            "phi," \
            "kappa," \
            "timeutc," \
            "cameraid," \
            "coneid," \
            "image_path_tif," \
            "geom," \
            "gsd" \
            " FROM {schema}.{table}" \
            " WHERE qo_done = 'New' AND comment_co != crossstrip AND level > 1 AND size_kb_tif > 10 ORDER BY time_file_tif LIMIT 1".format(
                schema = schema,
                table = table
            )
        
        print("Select all new areas marked for orthophoto creation:\n{}\n".format(query))
        cur.execute(query)
    except(psycopg2.ProgrammingError):
        print("DB error getting image from PPC orto part")
        return -1, "Error", "orto image"

    if cur.rowcount == 0:
        return -1, "NoNew", "ortho image"

    print("Job found:")

    result = cur.fetchone()
    image_id = str(result[0])

    print("Id: {}\n".format(image_id))

    try:
        gsd = float(result[12])
    except:
        gsd = 0.1

    if (gsd > 0.12):
        res = "0.16"
        final_destination = config.get("GruOrto", "16cmTargetDestination")
    else:
        res = "0.1"
        final_destination = config.get("GruOrto", "10cmTargetDestination")

    base_path = config.get("GruOrto", "BasePath")
    calc_path = config.get("GruOrto", "CalcPath")
    jpeg_path = calc_path + "jpeg\\"

    o_name = "O{}.tif".format(image_id)
    ort_name = calc_path + o_name
    dem_path = "{}DTM_{}.asc".format(calc_path, image_id)

    filename = image_id
    orto_batfile = "{}.bat".format(base_path + filename)
    def_name = "{}.def".format(base_path + filename)
    Z = 0

    camera_id = str(result[8])
    image_date = str(result[7])
    img_path = str(result[10])
    cone_id = str(result[9])
    
    io = get_io(camera_id, cone_id, image_date, conf)
    
    pixel_size = io[3]
    image_extent_x = io[4] * -2 / pixel_size
    image_extent_y = io[5] * -2 / pixel_size

    filename = image_id
    
    x0 = (result[1])
    y0 = (result[2])
    z0 = (result[3])
    ome = (result[4])
    phi = (result[5])
    kap = (result[6])

    eo = [x0, y0, z0, ome, phi, kap]

    with open(orto_batfile, "w") as bat_file:
        # Processingmanager info
        job_name = image_id[5:10]
        bat_file.write("python {} {} 50 \n".format(
            config.get("GruOrto", "ProgressScript"),
            job_name
        ))

        if (image_extent_x < image_extent_y):
            ul = ray(io, eo, Z, image_extent_x * 0.25, image_extent_y * 0.07)
            ur = ray(io, eo, Z, image_extent_x * 0.25, image_extent_y * 0.93)
            lr = ray(io, eo, Z, image_extent_x * 0.75, image_extent_y * 0.93)
            ll = ray(io, eo, Z, image_extent_x * 0.75, image_extent_y * 0.07)
        else:
            ul = ray(io, eo, Z, image_extent_x * 0.07, image_extent_y * 0.25)
            ur = ray(io, eo, Z, image_extent_x * 0.07, image_extent_y * 0.75)
            lr = ray(io, eo, Z, image_extent_x * 0.93, image_extent_y * 0.75)
            ll = ray(io, eo, Z, image_extent_x * 0.93, image_extent_y * 0.25)

        polyg = [ul, ur, lr, ll]

        bbox = bounding_box(polyg)
        
        tlx = int(round((bbox[0] / float(res)), 0) * float(res))
        tly = int(round((bbox[3] / float(res)), 0) * float(res))
        lrx = int(round((bbox[1] / float(res)), 0) * float(res))
        lry = int(round((bbox[2] / float(res)), 0) * float(res))
        
        bo_box = "MULTIPOLYGON ((({} {}, {} {}, {} {}, {} {}, {} {})))".format(
                tlx,
                tly,
                lrx,
                tly,
                lrx,
                lry,
                tlx,
                lry,
                tlx,
                tly
            )
        bat_file.write("cd {} \n".format(config.get("GruOrto", "TempPath")))
        bat_file.write("gdal_translate -of AAIGrid -projwin {} {} {} {} {} {dem_path}\n".format(
            str(tlx - (float(res) * 20)),
            str(tly + (float(res) * 20)),
            str(lrx + (float(res) * 20)),
            str(lry - (float(res) * 20)),
            config.get("GruOrto", "VrtFile"),
            dem_path
        ))
        bat_file.write("{} -def {}\n".format(
            config.get("GruOrto", "CowsExecutable"),    
            def_name
        ))
        bat_file.write("gdal_translate -b 1 -b 2 -b 3 -a_srs EPSG:25832 -of GTIFF -co COMPRESS=JPEG -co JPEG_QUALITY=85 -co PHOTOMETRIC=YCBCR -co TILED=YES {} {}\n".format(calc_path + o_name, jpeg_path + o_name))
        bat_file.write("REM *** Move Output *** \n")
        bat_file.write("copy {} {} \n".format(jpeg_path + o_name, final_destination))
        bat_file.write("IF %ERRORLEVEL% NEQ 0 (\n")
        bat_file.write("  ECHO Copy failed\n")
        
        sql_streng = "UPDATE {}.{} SET qo_done = 'Fail' WHERE imageid = '{}'".format(schema, table, image_id)
      
        bat_file.write("  python {} '{}' \n".format(
            config.get("GruOrto", "ReportScript"),
            sql_streng
        ))
        bat_file.write(") ELSE (\n")
        bat_file.write("  ECHO Copy succeded\n")
        
        sql_streng = "UPDATE {}.{} SET qo_done = 'Done' WHERE imageid = '{}'".format(schema, table, image_id)
        
        bat_file.write("  python {} '{}' \n".format(
            config.get("GruOrto", "ReportScript"),
            sql_streng
        ))
        bat_file.write(")\n")
        bat_file.write("REM *** CleanUP *** \n")
        bat_file.write("del {}DTM_{}.*\n".format(calc_path, image_id))
        bat_file.write("del {}O{}.*\n".format(calc_path, image_id))
        bat_file.write("del {}O{}.*\n".format(jpeg_path, image_id))
        bat_file.write("python {} {} 101 \n".format(
            config.get("GruOrto", "ProgressScript"),
            job_name
        ))

        query = "UPDATE {}.{} SET qo_done = 'Pending' WHERE imageid = '{}'".format(schema, table, image_id)
        
        print("Database call to update {}: \n{}\n".format(table, query))
        cur.execute(query)
        conn.commit()

    create_def(def_name, img_path, dem_path, ort_name, io, eo, polyg, res)
    minion_manager("Orto", orto_batfile, "GRU", bo_box, priority, conf)
    
    print("Job id: {} - bat file created".format(image_id))
    return 1, "JobBuilt", "ortho image"


def gru_filelist(schema, table, gsd, conf : Config):
    conn = get_db_conn(conf)
    cur = conn.cursor()
    config = conf.get()

    if gsd == "0.10":
        out_path = config.get("GruFileList", "10cmTargetDestination")
    else:
        out_path = config.get("GruFileList", "16cmTargetDestination")

    query = "SELECT DISTINCT a.kn10kmdk FROM remote_sensing.'10km_tiles' a, {}.{} b WHERE ST_DWithin(a.geom, b.geom,2000) AND b.qo_done = 'Done' AND gsd = '{}'".format(schema, table, gsd)

    cur.execute(query)

    list1 = cur.fetchall()

    for i in list1:
        print(i[0])
        with open(out_path + i[0] + ".filelist", "w") as text_file:
            query = "SELECT DISTINCT b.imageid FROM remote_sensing.'10km_tiles' a, {}.{} b WHERE ST_DWithin(a.geom, b.geom,2000) AND (b.qo_done = 'Done' OR b.qo_done = 'Distrib') AND a.kn10kmdk = '{}' AND gsd = '{}'".format(
                schema, 
                table, 
                i[0], 
                gsd
            )
            cur.execute(query)

            list2 = cur.fetchall()

            for j in list2:
                print(j)

                text_file.write("O" + j[0] + ".tif\n")

                query = "UPDATE {}.{} SET qo_done = 'Distrib' WHERE imageid = '{}'".format(schema, gsd, j[0])
                print(query)
                cur.execute(query)
            
            conn.commit()
            text_file.close()


def gru_oblique_tiles(schema, table_fp, table_tile, priority, conf : Config):
    config = conf.get()

    try:
        conn = get_db_conn(conf)
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = {})".format(table_fp))
        
        if cur.fetchone()[0]:
            print("Footprint database found")
        else:
            print("Footprint database not found")
        
        cur2 = conn.cursor()
        cur2.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = {})".format(table_tile))
        
        if cur2.fetchone()[0]:
            print("Tile database found")
        else:
            print("Tile database not found")
        
        cur.execute("SELECT centroid_tile FROM {}.{} WHERE oblique_tile_done = 'New' AND centroid_tile != ''".format(
            schema,
            table_fp
        ))
        
        if cur.rowcount == 0:
            print("No new tiles, will now fool around for a minute - " + str(datetime.now()))
            return -1, "NoNew", "oblique"

        result = cur.fetchone()
        tile = str(result[0])
        cur2.execute("SELECT ST_AsText(geom) FROM {}.{} WHERE kn1kmdk = '{}'".format(
            schema,
            table_tile,
            tile
        ))
        res = cur2.fetchone()
        bo_box = res[0]
        print("\n ---------------------------------------------------------------------\n Tile id: " + tile)

        base_path = config.get("GruObliqueTiles", "BasePath")
        temp_disc = config.get("GruObliqueTiles", "TempPath")
        zip_file = config.get("GruObliqueTiles", "ZipFileName").replace("{tile}", str(tile))

        # Set destination folder
        ftp_path = config.get("GruObliqueTiles", "FtoPath")
        oblique_tile_batfile = base_path + tile + ".bat"
        
        with open(oblique_tile_batfile, "w") as bat_file:
            job_name = tile
            
            bat_file.write("@ECHO OFF \n")
            bat_file.write("python {} {} 50 \n".format(
                config.get("GruObliqueTiles", "ProgressScript"),
                job_name
            ))
            bat_file.write("python {} {}\n".format(
                config.get("GruObliqueTiles", "TileMakerScript"),
                tile
            ))
            bat_file.write("REM *** Copy to ftp *** \n")
            bat_file.write("python {} {} {} {}\n".format(
                config.get("GruObliqueTiles", "FtpUploadScript"),
                temp_disc + zip_file,
                ftp_path + zip_file,
                tile
            ))
            bat_file.write("IF %ERRORLEVEL% NEQ 0 (\n")
            bat_file.write("  ECHO ftp upload failed\n")
            
            sql = "UPDATE {}.{} SET oblique_tile_done = 'Fail' WHERE centroid_tile = '{}'".format(
                schema,
                table_fp,
                tile
            )
            
            bat_file.write("  python {} '{}'\n".format(
                config.get("GruObliqueTiles", "ProgressScript"),
                sql
            ))
            bat_file.write(") ELSE (\n")
            bat_file.write("  ECHO ftp upload succeded\n")
            
            sql = "UPDATE {}.{} SET oblique_tile_done = 'Done' WHERE centroid_tile = '{}'".format(
                schema,
                table_fp,
                tile
            )
            
            bat_file.write("  python {} '{}'\n".format(
                config.get("GruObliqueTiles", "ProgressScript"),
                sql
            ))
            bat_file.write(")\n")
            bat_file.write("REM *** CleanUP *** \n")
            bat_file.write("del {}\n".format(temp_disc + zip_file))
            bat_file.write("python {} {} 101\n".format(
                config.get("GruObliqueTiles", "ProgressScript"),
                job_name
            ))

            query = "UPDATE {}.{} SET oblique_tile_done = 'Done' WHERE centroid_tile = '{}'".format(
                schema,
                table_fp,
                tile
            )

            cur.execute(query)
            conn.commit()

        minion_manager("Oblique_tile", oblique_tile_batfile, "GRU", bo_box, priority, conf)

        return 1, "JobBuilt", "oblique tiles"
    except(psycopg2.ProgrammingError):
        print("Error during oblique tiling")
        return -1, "Error", "oblique tiles"

def gru_ml_orto(schema, table, priority, conf : Config):
    print("Checking for new Machine Learning Ortho Photo Job\n")
    conn = get_db_conn(conf)
    cur = conn.cursor()
    config = conf.get()

    try:
        cur = conn.cursor()
        query = "SELECT imageid," \
                 "easting," \
                 "northing," \
                 "height," \
                 "omega," \
                 "phi," \
                 "kappa," \
                 "timeutc," \
                 "cameraid," \
                 "coneid," \
                 "image_path_tif," \
                 "geom," \
                 "gsd" \
                 " FROM {}.{} WHERE qo_done = 'ML'"
        print("Select all new areas marked for ML-orthophoto creation:\n{}\n".format(query))
        cur.execute(query)

        if cur.rowcount == 0:
            return -1, "NoNew", "ML orto image"
        else:
            print("Job found:")
            result = cur.fetchone()
            image_id = str(result[0])
            print("Id: {}\n".format(image_id))

            try:
                gsd = float(result[12])
            except:
                gsd = 0.1

            if (gsd > 0.12):
                res = "0.16"
            else:
                res = "0.16"

            final_dst = config.get("GruMlOrto", "TargetDestination")

            base_path = config.get("GruMlOrto", "BasePath")
            calc_path = config.get("GruMlOrto", "CalcPath")
            jpeg_path = calc_path + "jpeg\\"

            o_name = "O{}.tif".format(image_id)
            ort_name = calc_path + o_name
            dem_path = "{}DTM_{}.asc".format(calc_path, image_id)

            file_name = image_id
            orto_batfile = "{}.bat".format(base_path + file_name)
            def_name = "{}.def".format(base_path + file_name)

            camera_id = str(result[8])
            image_date = str(result[7])
            img_path = str(result[10])
            cone_id = str(result[9])
            io = get_io(camera_id, cone_id, image_date, conf)

            file_name = image_id
            x0 = (result[1])
            y0 = (result[2])
            z0 = (result[3])
            ome = (result[4])
            phi = (result[5])
            kap = (result[6])

            eo = [x0, y0, z0, ome, phi, kap]

            with open(orto_batfile, "w") as bat_file:
                # Processingmanager info
                job_name = image_id[5:10]
                bat_file.write("python {} {} 50 \n".format(
                    config.get("GruMlOrto", "ProgressScript"),
                    job_name
                ))

                tlx = int(x0 - (200))
                tly = int(y0 + (200))
                lrx = int(x0 + (200))
                lry = int(y0 - (200))

                polyg = [(tlx, tly), (lrx, tly), (lrx, lry), (tlx, lry)]

                bo_box = "MULTIPOLYGON ((({} {}, {} {}, {} {}, {} {}, {} {})))".format(
                        tlx,
                        tly,
                        lrx,
                        tly,
                        lrx,
                        lry,
                        tlx,
                        lry,
                        tlx,
                        tly
                    )
                bat_file.write("cd {} \n".format(config.get("GruMlOrto", "TempPath")))
                bat_file.write("gdal_translate -of AAIGrid -projwin {} {} {} {} {} {dem_path}\n".format(
                    str(tlx - (float(res) * 20)),
                    str(tly + (float(res) * 20)),
                    str(lrx + (float(res) * 20)),
                    str(lry - (float(res) * 20)),
                    config.get("GruMlOrto", "VrtFile"),
                    dem_path
                ))
                bat_file.write("{} {}\n".format(
                    config.get("GruMlOrto", "CowsExecutable"),
                    def_name
                ))
                bat_file.write("gdal_translate -b 1 -b 2 -b 3 -of PNG {} {}.png\n".format(
                    calc_path + o_name,
                    jpeg_path + o_name.rstrip(".tif")
                ))
                bat_file.write("REM *** Move Output *** \n")
                bat_file.write("copy {}.png.aux.xml {} \n".format(
                    jpeg_path + o_name.rstrip(".tif"),
                    final_dst
                ))
                bat_file.write("copy {}.png {} \n".format(
                    jpeg_path + o_name.rstrip(".tif"),
                    final_dst
                ))
                bat_file.write(gdal_translate_str(0, 0, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(0, 500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(0, 1000, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(0, 1500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(0, 2000, 500, 500, jpeg_path, o_name, final_dst))
                
                bat_file.write(gdal_translate_str(500, 0, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(500, 500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(500, 1000, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(500, 1500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(500, 2000, 500, 500, jpeg_path, o_name, final_dst))
                
                bat_file.write(gdal_translate_str(1000, 0, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1000, 500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1000, 1000, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1000, 1500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1000, 2000, 500, 500, jpeg_path, o_name, final_dst))
                
                bat_file.write(gdal_translate_str(1500, 0, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1500, 500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1500, 1000, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1500, 1500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1500, 2000, 500, 500, jpeg_path, o_name, final_dst))
                
                bat_file.write(gdal_translate_str(2000, 0, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(2000, 500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(2000, 1000, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(2000, 1500, 500, 500, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(2000, 2000, 500, 500, jpeg_path, o_name, final_dst))
                
                
                bat_file.write(gdal_translate_str(0, 0, 1250, 1250, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(0, 1250, 1250, 1250, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1250, 0, 1250, 1250, jpeg_path, o_name, final_dst))
                bat_file.write(gdal_translate_str(1250, 1250, 1250, 1250, jpeg_path, o_name, final_dst))
                
                bat_file.write("IF %ERRORLEVEL% NEQ 0 (\n")
                bat_file.write("  ECHO Copy failed\n")
                
                sql = "UPDATE {}.{} SET qo_done = 'Fail' WHERE imageid = '{}'".format(schema, table, image_id)
                
                bat_file.write("  python {} '{}' \n".format(
                    config.get("GruMlOrto", "ReportScript"),
                    sql
                ))
                bat_file.write(") ELSE (\n")
                bat_file.write("  ECHO Copy succeded\n")
                
                sql = "UPDATE {}.{} SET qo_done = 'Done' WHERE imageid = '{}'".format(schema, table, image_id)
                
                bat_file.write("  python {} '{}' \n".format(
                    config.get("GruMlOrto", "ReportScript"),
                    sql
                ))
                bat_file.write(")\n")
                bat_file.write("REM *** CleanUP *** \n")
                bat_file.write("del {}DTM_{}.*\n".format(calc_path, image_id))
                bat_file.write("del {}O{}.*\n".format(calc_path, image_id))
                bat_file.write("del {}O{}.*\n".format(jpeg_path, image_id))
                bat_file.write("python {} {} 101 \n".format(
                    config.get("GruMlOrto", "ProgressScript"),
                    job_name
                ))
                query = "UPDATE {}.{} SET qo_done = 'Pending' WHERE imageid = '{}'".format(schema, table, image_id)
                print("Database call to update {}: \n{}\n".format(table, query))
                cur.execute(query)
                conn.commit()

            create_def(def_name, img_path, dem_path, ort_name, io, eo, polyg, res)
            minion_manager("Orto_ML", orto_batfile, "GRU", bo_box, priority, conf)
        print("Job id: {} - bat file created\n".format(image_id))
        return 1, "JobBuilt", "ML orto image"
    except(psycopg2.ProgrammingError):
        print("Error during ML orto")
        return -1, "Error", "ML orto image"

def gru_sentinel_download(schema, table_senti, table_tile, priority, conf : Config):
    try:
        conn = get_db_conn(conf)
        cur = conn.cursor()
        config = conf.get()

        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = {})".format(table_senti))

        if cur.fetchone()[0]:
            print("Footprint database found")
        else:
            print("Footprint database not found")
        
        cur2 = conn.cursor()
        cur2.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = {})".format(table_tile))
        if cur2.fetchone()[0]:
            print("Tile database found")
        else:
            print("Tile database not found")

        cur.execute("SELECT uuid, beginposit, title, ST_AsText(geom) FROM {}.{} WHERE s2_done = 'New'".format(schema, table_senti))
        
        if cur.rowcount == 0:
            print("No new tiles, will now fool around for a minute - " + str(datetime.now()))
            return -1, "NoNew"
        else:
            result = cur.fetchone()
            sentinel = str(result[0]) # TODO: Fix
            scene_time = result[2]
            scene_uuid = result[1]
            scene_title = result[3]
            bo_box = result[4]

            print(scene_time)
            print(scene_uuid)

            tile_time = scene_title.split("_")[2][0:8]
            tile_id = scene_title.split("_")[5]

            base_path = config.get("GruSentinelDownload", "BasePath")
            temp_disc = config.get("GruSentinelDownload", "TempPath")
            # Set destination folder
            ftp_path = config.get("GruSentinelDownload", "FtpPath")
            sentinel_tile_batfile = base_path + scene_title + ".bat"
            zip_file = config.get("GruSentinelDownload", "ZipFileName")
            
            with open(sentinel_tile_batfile, "w") as bat_file:
                job_name = sentinel
                bat_file.write("@ECHO OFF \n")
                bat_file.write("python {} {} 50 \n".format(
                    config.get("GruSentinelDownload", "ProgressScript"),
                    job_name
                ))
                bat_file.write("python {} {} {}\n".format(
                    config.get("GruSentinelDownload", "DownloaderScript"),
                    tile_id, 
                    tile_time
                ))
                bat_file.write("REM *** Download scene from SciHub *** \n")
                bat_file.write("python {} {} {} {}\n".format(
                    config.get("GruSentinelDownload", "FtpUploadScript"),
                    temp_disc + zip_file, 
                    ftp_path + zip_file, 
                    sentinel
                ))
                bat_file.write("IF %ERRORLEVEL% NEQ 0 (\n")
                bat_file.write("  ECHO ftp upload failed\n")
                
                sql = "UPDATE {}.{} SET oblique_tile_done = 'Fail' WHERE centroid_tile = '{}'".format(schema, table_senti, sentinel)
                
                bat_file.write("  python {} \"{}\" \n".format(
                    config.get("GruSentinelDownload", "ProgressScript"),
                    sql
                ))
                bat_file.write(") ELSE (\n")
                bat_file.write("  ECHO ftp upload succeded\n")
                
                sql = "UPDATE {}.{} SET oblique_tile_done = 'Done' WHERE centroid_tile = '{}'".format(schema, table_senti, sentinel)
                
                bat_file.write("  python {} \"{}\" \n".format(
                    config.get("GruSentinelDownload", "ProgressScript"),
                    sql
                ))
                bat_file.write(")\n")
                bat_file.write("REM *** CleanUP *** \n")
                bat_file.write("del {}\n".format(temp_disc + zip_file))
                bat_file.write("python {} {} 101 \n".format(
                    config.get("GruSentinelDownload", "ProgressScript"),
                    job_name
                ))
                query = "UPDATE {}.{} SET oblique_tile_done = 'Pending' WHERE centroid_tile = '{}'".format(schema, table_senti, sentinel)
                cur.execute(query)
                conn.commit()

            minion_manager("Sentinel2_tile", sentinel_tile_batfile, "GRU", bo_box, priority, conf)
        return 1, "JobBuilt", "sentinel download"
    except(psycopg2.ProgrammingError):
        print("DB error creating sentinel2 download batfile")
        return -1, "Error", "sentinel download"

def gru_gnet_calc(schema, table_gnet, table_tile, conf : Config):
    try:
        conn = get_db_conn(conf)
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name={})".format(table_gnet))
        if cur.fetchone()[0]:
            print("Footprint database found")
        else:
            print("Footprint database not found")
        
        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name={})".format(table_tile))
        if cur.fetchone()[0]:
            print("Tile database found")
        else:
            print("Tile database not found")

        return 1, "JobBuilt", "GNET uncertaincy"
    except(psycopg2.ProgrammingError):
        print("Error during gnet calculation")
        return -1, "Error", "GNET uncertaincy"
