import random
from .utils import NoneType


class bpy_struct:
    def __init__(self):
        self.id_data = ""

    def as_pointer(self):
        return random.randint(100, 999999)

    def driver_add(self, path, index=-1):
        return NoneType()
    
    def driver_remove(self, path, index=-1):
        return False
    
    def get(self, key, default=None):
        return default
    
    def is_property_hidden(self, property):
        return bool(random.randint(0, 1))

    def is_property_overridable_library(self, property):
        return False

    def is_property_readonly(self, property):
        return True

    def is_property_set(self, property, ghost=True):
        return True

    def items(self):
        return NoneType()

    def keyframe_delete(self, data_path, index=-1, frame=0, group=""):
        return False

    def keyframe_insert(self, data_path, index=-1, frame=0, group="", options=set()):
        return False
    
    def keys(self):
        return self.__dict__.keys()
    
    def path_from_id(self, property=""):
        return self.id_data

    def path_resolve(self, path, coerce=True):
        raise ValueError(f"Property not found from the path {path}")

    def pop(self, key, default=None):
        return default
    
    def property_overridable_library_set(self, property, overridable):
        return False
    
    def property_unset(self, property):
        return NoneType()
    
    def type_recast(self):
        return bpy_struct()
    
    def values(self):
        return self.__dict__.values()


class ID(bpy_struct):
    def __init__(self):
        self.is_embedded_data = False
        self.is_evaluated = False
        self.is_library_indirect = False
        self.library = Library()
        self.name = ""
        self.name_full = ""
        self.original = ID()
        self.override_library = IDOverrideLibrary()
        self.preview = ImagePreview()
        self.tag = False
        self.use_fake_user = False
        self.users = 0
    
    def evaluated_get(self, depsgraph):
        return ID()
    
    def copy(self):
        return ID()
    
    def override_create(remap_local_usages=False):
        return ID()
    
    def user_clear(self):
        return NoneType()
    
    def user_remap(self, new_id):
        self = new_id
    
    def make_local(self, clear_proxy=True):
        return ID()
    
    def user_of_id(self, id):
        return self.users
    
    def animation_data_create(self):
        return NoneType()
    
    def animation_data_clear(self):
        return NoneType()
    
    def update_tag(refresh={}):
        return NoneType()
    
    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default


class PackedFile(bpy_struct):
    data = ""
    size = 0

    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default


class Library(ID):
    def __init__(self):
        self.filepath = ""
        self.packed_file = PackedFile()
        self.parent = Library()
        self.version = (0, 0, 0)
        self.users_id = ID()

    def reload(self):
        return NoneType()

    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default


class ImagePreview(bpy_struct):
    icon_id = 0
    icon_pixels = 0
    icon_pixels_float = 0.0
    icon_size = (0, 0)
    image_pixels = 0
    image_pixels_float = 0.0
    image_size = (0, 0)
    is_icon_custom = False
    is_image_custom = False

    def reload(self):
        return NoneType()
    
    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default


class IDOverrideLibrary(bpy_struct):
    def __init__(self):
        self.properties = [IDOverrideLibraryProperty()] * random.randint(1, 10)


class IDOverrideLibraryProperty(bpy_struct):
    def __init__(self):
        self.operations = [IDOverrideLibraryPropertyOperation()] * random.randint(1, 10)
        self.rna_path = ""
    
    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default


class IDOverrideLibraryPropertyOperation(bpy_struct):
    def __init__(self):
        self.flag = "MANDATORY"
        self.operation = "REPLACE"
        self.subitem_local_index = -1
        self.subitem_local_name = ""
        self.subitem_reference_index = -1
        self.subitem_reference_name = ""
    
    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default


class View2D(bpy_struct):
    def region_to_view(self, x, y):
        return [0.0, 0.0]
    
    def view_to_region(self, x, y, clip=True):
        return [0, 0]
    
    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default


class Region(bpy_struct):
    alignment = "None"
    height = random.randint(0, 32767)
    type = "WINDOW"
    view2d = View2D()
    width = random.randint(0, 32767)
    x, y = random.randint(-32767, 32767), random.randint(-32767, 32767)

    def tag_redraw(self):
        return NoneType()
    
    @classmethod
    def bl_rna_get_subclass(cls, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(cls, id, default=None):
        return default


class Space(bpy_struct):
    show_locked_time = False
    show_region_header = False
    type = "EMPTY"

    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default
    
    def draw_handler_add(cself, allback, args, region_type, draw_type):
        return NoneType()
    
    def draw_handler_remove(self, handler, region_type):
        return NoneType()


class AreaSpaces(bpy_struct):
    active = Space()

    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default


class Area(bpy_struct):
    regions = [Region()] * random.randint(2, 20)
    show_menus = False
    spaces = [Space()] * random.randint(1, 4)
    type = "VIEW_3D"
    ui_type = ""
    x = y = width = height = 0

    def tag_redraw(self):
        return NoneType()
    
    def header_text_set(self, text):
        return NoneType()
    
    @classmethod
    def bl_rna_get_subclass(self, id, default=None):
        return default
    
    @classmethod
    def bl_rna_get_subclass_py(self, id, default=None):
        return default


class BlendData(bpy_struct):
    pass
