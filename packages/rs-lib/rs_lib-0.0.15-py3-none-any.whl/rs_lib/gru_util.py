def gdal_translate_str(x_off, y_off, x_size, y_size, jpeg_path, o_name, final_dst):
    return "gdal_translate -srcwin {}, {}, {}, {} {}.png {}tiles_{}\\{}{}_{}.png\n".format(
            x_off,
            y_off,
            x_size,
            y_size,
            jpeg_path + o_name.rstrip(".tif"),
            final_dst,
            x_size,
            o_name.rstrip(".tif"),
            x_off,
            y_off
        )