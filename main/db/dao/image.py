from main.db.dao.utils import *

def get_image_name_list():
    return list(ImageModel.select(ImageModel.image_name.distinct()).scalars())