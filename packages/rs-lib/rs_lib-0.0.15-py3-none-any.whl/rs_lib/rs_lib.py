import math

def ray(io, eo, z, col, row):
    x_ppa = io[0]
    y_ppa = io[1]
    focal_length = io[2]
    pixel_size = io[3]
    image_extent_x = io[4]
    image_extent_y = io[5]
    
    x0 = eo[0]
    y0 = eo[1]
    z0 = eo[2]
    ome = eo[3]
    phi = eo[4]
    kap = eo[5]
    
    o = math.radians(ome)
    p = math.radians(phi)
    k = math.radians(kap)
    
    d11 = math.cos(p) * math.cos(k)
    d12 = - math.cos(p) * math.sin(k)
    d13 = math.sin(p)
    d21 = math.cos(o) * math.sin(k) + math.sin(o) * math.sin(p) * math.cos(k)
    d22 = math.cos(o) * math.cos(k) - math.sin(o) * math.sin(p) * math.sin(k)
    d23 = - math.sin(o) * math.cos(p)
    d31 = math.sin(o) * math.sin(k) - math.cos(o) * math.sin(p) * math.cos(k)
    d32 = math.sin(o) * math.cos(k) + math.cos(o) * math.sin(p) * math.sin(k)
    d33 = math.cos(o) * math.cos(p)

    x_dot = ((col*pixel_size) - image_extent_x*-1) - x_ppa
    y_dot = ((row*pixel_size) - image_extent_y*-1) - y_ppa

    kx = (d11*x_dot + d12*y_dot + d13*focal_length) / (d31*x_dot + d32*y_dot + d33*focal_length)
    ky = (d21*x_dot + d22*y_dot + d23*focal_length) / (d31*x_dot + d32*y_dot + d33*focal_length)

    x = (z-z0) * kx+x0
    y = (z-z0) * ky+y0

    return(x, y)


def rayverse(io, eo, x, y, z):
    x_ppa = io[0]
    y_ppa = io[1]
    focal_length = io[2]
    pixel_size = io[3]
    image_extent_x = io[4]
    image_extent_y = io[5]

    x0 = eo[0]
    y0 = eo[1]
    z0 = eo[2]
    ome = eo[3]
    phi = eo[4]
    kap = eo[5]
    
    o = math.radians(ome)
    p = math.radians(phi)
    k = math.radians(kap)
    
    d11 = math.cos(p) * math.cos(k)
    d12 = - math.cos(p) * math.sin(k)
    d13 = math.sin(p)
    d21 = math.cos(o) * math.sin(k) + math.sin(o) * math.sin(p) * math.cos(k)
    d22 = math.cos(o) * math.cos(k) - math.sin(o) * math.sin(p) * math.sin(k)
    d23 = - math.sin(o) * math.cos(p)
    d31 = math.sin(o) * math.sin(k) - math.cos(o) * math.sin(p) * math.cos(k)
    d32 = math.sin(o) * math.cos(k) + math.cos(o) * math.sin(p) * math.sin(k)
    d33 = math.cos(o) * math.cos(p)

    x_dot = (-1)*focal_length*((d11*(x-x0) + d21*(y-y0) + d31*(z-z0)) / (d13*(x-x0) + d23*(y-y0) + d33*(z-z0)))
    y_dot = (-1)*focal_length*((d12*(x-x0) + d22*(y-y0) + d32*(z-z0)) / (d13*(x-x0) + d23*(y-y0) + d33*(z-z0)))

    col = ((x_dot-x_ppa) + (image_extent_x))*(-1) / pixel_size
    row = ((y_dot-y_ppa) + (image_extent_y))*(-1) / pixel_size

    return(col, row)


def create_sure(out_path, img_path, io, eo):
    x_ppa = io[0]
    y_ppa = io[1]
    focal_length = io[2] * (-1)
    pixel_size = io[3]
    image_extent_x = int(io[4]*-2 / pixel_size)
    image_extent_y = int(io[5]*-2 / pixel_size)

    x = eo[0]
    y = eo[1]
    z = eo[2]
    omega = eo[3]
    phi = eo[4]
    kappa = eo[5]

    pri_x_pix = (image_extent_x / 2) + ((x_ppa / pixel_size))
    pri_y_pix = (image_extent_y / 2) + ((y_ppa / pixel_size))

    r = math.pi / 180

    so = math.sin(omega * r)
    co = math.cos(omega * r)
    sp = math.sin(phi * r)
    cp = math.cos(phi * r)
    ck = math.cos(kappa * r)
    sk = math.sin(kappa * r)

    rot0 = cp * ck
    rot1 = co*sk + so*sp*ck
    rot2 = so*sk - co*sp*ck
    rot3 = cp * sk
    rot4 = -co*ck + so*sp*sk
    rot5 = -so*ck - co*sp*sk
    rot6 = -sp
    rot7 = so * cp
    rot8 = -co * cp

    cc_pix = focal_length / pixel_size

    with open(out_path, "w") as text_file:
        text_file.write("$ImageID___________________________________________________(ORI_Ver_1.0)" + " \n")
        text_file.write("\t" + img_path + " \n")
        text_file.write("$IntOri_FocalLength_________________________________________________[mm]" + " \n")
        text_file.write("\t" + str(focal_length) + " \n")
        text_file.write("$IntOri_PixelSize______(x|y)________________________________________[mm]" + " \n")
        text_file.write("\t" + str(pixel_size) + "\t " + str(pixel_size) + " \n")
        text_file.write("$IntOri_SensorSize_____(x|y)_____________________________________[pixel]" + " \n")
        text_file.write("\t" + str(image_extent_x) + "\t " + str(image_extent_y) + " \n")
        text_file.write("$IntOri_PrincipalPoint_(x|y)_____________________________________[pixel]" + " \n")
        text_file.write("\t" + str(pri_x_pix) + "\t " + str(pri_y_pix) + " \n")
        text_file.write("$IntOri_CameraMatrix_____________________________(ImageCoordinateSystem)" + " \n")
        text_file.write("\t" + str(cc_pix) + "\t " + "0.00000000" + "\t " + str(pri_x_pix) + " \n")
        text_file.write("\t" + "0.00000000" + "\t " + str(cc_pix) + "\t " + str(pri_y_pix) + " \n")
        text_file.write("\t" + "0.00000000" + "\t" + " 0.00000000" + "\t" + " 1.00000000" + " \n")
        text_file.write("$ExtOri_RotationMatrix____________________(World->ImageCoordinateSystem)" + " \n")
        text_file.write("\t" + str(rot0) + "\t " + str(rot1) + "\t " + str(rot2) + " \n")
        text_file.write("\t" + str(rot3) + "\t " + str(rot4) + "\t " + str(rot5) + " \n")
        text_file.write("\t" + str(rot6) + "\t " + str(rot7) + "\t " + str(rot8) + " \n")
        text_file.write("$ExtOri_TranslationVector________________________(WorldCoordinateSystem)" + " \n")
        text_file.write("\t" + str(x) + "\t " + str(y) + "\t " + str(z) + " \n")
        text_file.write("$IntOri_Distortion_____(Model|ParameterCount|(Parameters))______________" + " \n")
        text_file.write("\t" + "none 0")
        text_file.close()


def create_footprint(io, eo):
    pixel_size = io[3]
    image_extent_x = io[4]
    image_extent_y = io[5]

    xy1 = ray(io, eo, 0, 0, 0)
    xy2 = ray(io, eo, 0, image_extent_x*-2 / pixel_size, 0)
    xy3 = ray(io, eo, 0, image_extent_x*-2 / pixel_size, image_extent_y*-2 / pixel_size)
    xy4 = ray(io, eo, 0, 0, image_extent_y*-2 / pixel_size)

    poly = [xy1, xy2, xy3, xy4]

    return(xy1, xy2, xy3, xy4, poly)


def create_def(def_name, img_path, dem_path, ort_path, io, eo, poly, res):
    x_ppa = io[0]
    y_ppa = io[1]
    focal_length = io[2]
    pixel_size = io[3]
    image_extent_x = io[4]
    image_extent_y = io[5]
    mount_rotation = io[6]

    # Calculate Orto Extents
    bbox = bounding_box(poly)
    
    tlx = int(round((bbox[0] / float(res)), 0) * float(res))
    tly = int(round((bbox[3] / float(res)), 0) * float(res))
    lrx = int(round((bbox[1] / float(res)), 0) * float(res))
    lry = int(round((bbox[2] / float(res)), 0) * float(res))
        
    szx = (lrx - tlx) / float(res)
    szt = (tly - lry) / float(res)

    # Adjust for camera rotation
    if mount_rotation == 0:
        il1 = "0.000 " + str(pixel_size)
        il2 = str(pixel_size) + " 0.000 "
        il3 = str(image_extent_x) + " " + str(image_extent_y)
        pri_y = str(x_ppa)
        pri_x = str(y_ppa)

    elif mount_rotation == 180:
        il1 = " 0.000 " + str(pixel_size)
        il2 = str(pixel_size) + " 0.000 "
        il3 = str(image_extent_y) + " " + str(image_extent_x * (-1))
        pri_y = str(x_ppa)
        pri_x = str(y_ppa)

    elif mount_rotation == 90:
        il1 = str(pixel_size) + " 0.000"
        il2 = "0.000 " + str(pixel_size * (-1))
        il3 = str(image_extent_y) + " " + str(image_extent_x*(-1))
        pri_y = str(y_ppa)
        pri_x = str(x_ppa)

    elif mount_rotation == 270:
        il1 = str(pixel_size) + " 0.000"
        il2 = "0.000 " + str(pixel_size * (-1))
        il3 = str(image_extent_x) + " " + str(image_extent_y*(-1))
        pri_y = str(y_ppa)
        pri_x = str(x_ppa)

    elif mount_rotation == 999:
        il1 = str(pixel_size) + " 0.000"
        il2 = "0.000 " + str(pixel_size * (-1))
        il3 = str(image_extent_y*(-1)) + " " + str(image_extent_x)
        pri_y = str(y_ppa)
        pri_x = str(x_ppa)
    else:
        print ("Illegal Camera Rotation" + str(mount_rotation))
        exit()

    # Write DEF file
    with open(def_name, "w") as text_file:
        text_file.write("PRJ= nill.apr" + " \n")
        text_file.write("ORI= nill.txt" + " \n")
        text_file.write("RUN= 0" + " \n")
        text_file.write("DEL= NO" + " \n")
        text_file.write("IMG= " + img_path + " \n")
        text_file.write("DTM= " + dem_path + " \n")
        text_file.write("ORT= " + ort_path + " \n")
        text_file.write("TLX= " + str(tlx) + " \n")
        text_file.write("TLY= " + str(tly) + " \n")
        text_file.write("RES= " + str(res) + " \n")
        text_file.write("SZX= " + str(math.trunc(szx)) + " \n")
        text_file.write("SZY= " + str(math.trunc(szt)) + " \n")
        text_file.write("R34= NO" + " \n")
        text_file.write("INT= CUB -1" + " \n")
        text_file.write("CON= " + str(focal_length / 1000) + " \n")  # 0.1005
        text_file.write("XDH= " + pri_x + " \n")  #str(x_ppa) + " \n")  # -0.18
        text_file.write("YDH= " + pri_y + " \n")  #str(y_ppa) + " \n")
        text_file.write("IL1= " + il1 + " \n")   #str(pixel_size) + " 0.000 \n")
        text_file.write("IL2= " + il2 + " \n")   #"0.000 " + str(pixel_size * (-1)) + " \n")
        text_file.write("IL3= " + il3 + " \n")   #str(image_extent_x*-pixel_size/2) + " " + str(image_extent_y*pixel_size/2) + " \n")
        text_file.write("X_0= " + str(eo[0]) + " \n")
        text_file.write("Y_0= " + str(eo[1]) + " \n")
        text_file.write("Z_0= " + str(eo[2]) + " \n")
        text_file.write("DRG= DEG" + " \n")
        text_file.write("OME= " + str(eo[3]) + " \n")
        text_file.write("PHI= " + str(eo[4]) + " \n")
        text_file.write("KAP= " + str(eo[5]) + " \n")
        text_file.write("MBF= 870" + " \n")
        text_file.write("BBF= 999999" + " \n")
        text_file.write("STR= NO" + " \n")

        text_file.close()

    return


def bounding_box(poly):
    min_x = min_y = float("inf")
    max_x = max_y = float("-inf")
    
    for x, y in poly:
        # Set min coords
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
    
        # Set max coords
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    
    return [min_x, max_x, min_y, max_y]

def utm_to_lat_lng(zone, easting, northing, northernHemisphere=True):
    if not northernHemisphere:
        northing = 10000000 - northing

    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996

    arc = northing / k0
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0-3 * math.pow(e, 4) / 64.0-5 * math.pow(e, 6) / 256.0))

    ei = (1 - math.pow((1 - e*e), (1 / 2.0))) / (1 + math.pow((1 - e*e), (1 / 2.0)))

    ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

    cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    cc = 151 * math.pow(ei, 3) / 96
    cd = 1097 * math.pow(ei, 4) / 512
    phi1 = mu + ca*math.sin(2 * mu) + cb*math.sin(4 * mu) + cc*math.sin(6 * mu) + cd*math.sin(8 * mu)

    n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

    r0 = a * (1 - e*e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
    fact1 = n0 * math.tan(phi1) / r0

    a1 = 500000 - easting
    dd0 = a1 / (n0 * k0)
    fact2 = dd0*dd0 / 2

    t0 = math.pow(math.tan(phi1), 2)
    q0 = e1sq * math.pow(math.cos(phi1), 2)
    fact3 = (5 + 3*t0 + 10*q0 - 4*q0*q0 - 9*e1sq) * math.pow(dd0, 4) / 24

    fact4 = (61 + 90*t0 + 298*q0 + 45*t0*t0 - 252*e1sq - 3*q0*q0) * math.pow(dd0, 6) / 720

    lof1 = a1 / (n0 * k0)
    lof2 = (1 + 2*t0 + q0) * math.pow(dd0, 3) / 6.0
    lof3 = (5 - 2*q0 + 28*t0 - 3*math.pow(q0, 2) + 8*e1sq + 24*math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
    a3 = a2*180 / math.pi

    latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

    if not northernHemisphere:
        latitude = -latitude

    longitude = ((zone > 0) and (6*zone - 183.0) or 3.0) - a3

    if (zone > 29):
        longitude = longitude * (-1)

    return (latitude, longitude)

def sunAngle(self, datotiden, lati, longi):
    import math
    import datetime
    datotiden = datotiden.replace('-', ':')
    patterndatetime1 = re.compile("[0-9]{4}:[0-9]{2}:[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{0,3}")
    if patterndatetime1.match(datotiden):
        DateTime = datetime.datetime.strptime(datotiden, '%Y:%m:%d %H:%M:%S.%f')
    else:
        DateTime = datetime.datetime.strptime(datotiden, '%Y:%m:%d %H:%M:%S')

    dayOfYear = DateTime.timetuple().tm_yday
    hour = DateTime.hour
    mins = DateTime.minute
    sec = DateTime.second
    timeZone = 0

    gamma = (2 * math.pi / 365) * ((dayOfYear + 1) + (hour - 12) / 24)
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
    declin = 0.006918 - (0.399912 * math.cos(gamma)) + 0.070257 * math.sin(gamma) - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)
    tOffset = eqtime - 4 * longi + 60 * timeZone
    tst = hour * 60 + mins + sec / 60 + tOffset
    sh = (tst / 4) - 180
    zenit = math.degrees(math.acos(((math.sin(math.radians(lati)) * math.sin(declin)) + (math.cos(math.radians(lati)) * math.cos(declin) * math.cos(math.radians(sh))))))
    sunVinkel = 90 - zenit

    return sunVinkel
