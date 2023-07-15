bl_info = {
    "name": "Mesh Bones, Cosines, Collision Tag and Image Properties Panels",
    "author": "DGIorio",
    "version": (2, 5),
    "blender": (3, 1, 0),
    "location": "Properties Panel > Object Data Properties",
    "description": "Quick access to vertex bones, edge cosines, collision tag and image properties",
    "category": "UI",
}


import bpy
import bmesh
from struct import unpack


class ImagePropertiesPanel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Custom Properties"
	bl_idname = "IMAGE_PT_ImageProperties"
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = 'UI'
	bl_category = "Image"
	bl_description = "Set the image custom properties"
	bl_order = 1
	
	def draw(self, context):	# https://docs.blender.org/api/current/bpy.context.html
		layout = self.layout
		
		col = layout.column()
		row = col.row()
		row.prop(context.edit_image, "is_shared_asset")
		
		row = col.row(heading="dimension")
		row.enabled = not context.edit_image.is_shared_asset
		row.prop(context.edit_image, "dimension", text="")
		
		row = col.row(heading="main_mipmap")
		row.enabled = not context.edit_image.is_shared_asset
		row.prop(context.edit_image, "main_mipmap", text="")
		
		row = col.row(heading="unk_0x34")
		row.enabled = not context.edit_image.is_shared_asset
		row.prop(context.edit_image, "unk_0x34", text="")
		
		row = col.row(heading="unk_0x38")
		row.enabled = not context.edit_image.is_shared_asset
		row.prop(context.edit_image, "unk_0x38", text="")
		
		row = col.row(heading="flags")
		row.enabled = not context.edit_image.is_shared_asset
		row.prop(context.edit_image, "flags", text="")


class NodePropertiesPanel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Custom Properties"
	bl_idname = "NODE_PT_NodeProperties"
	bl_space_type = 'NODE_EDITOR'
	bl_region_type = 'UI'
	bl_category = "Node"
	bl_description = "Set the node custom properties"
	bl_order = 1
	
	@classmethod
	def poll(self, context):
		if context.active_node == None:
			return False
		return context.active_node.bl_idname == "ShaderNodeTexImage"
		
	
	def draw(self, context):	# https://docs.blender.org/api/current/bpy.context.html
		layout = self.layout
		me = context.active_node
		
		if me != None and me.bl_idname == "ShaderNodeTexImage":
		#if me.bl_idname == "ShaderNodeTexImage":
			col = layout.column()
			row = col.row()
			row.prop(me, "is_shared_asset")
			
			row = col.row(heading="addressing_mode")
			row.enabled = not me.is_shared_asset
			row.prop(me, "addressing_mode", text="")
			
			row = col.row(heading="filter_types")
			row.enabled = not me.is_shared_asset
			row.prop(me, "filter_types", text="")
			
			row = col.row(heading="min_max_lod")
			row.enabled = not me.is_shared_asset
			row.prop(me, "min_max_lod", text="")
			
			row = col.row(heading="max_anisotropy")
			row.enabled = not me.is_shared_asset
			row.prop(me, "max_anisotropy", text="")
			
			row = col.row(heading="mipmap_lod_bias")
			row.enabled = not me.is_shared_asset
			row.prop(me, "mipmap_lod_bias", text="")
			
			row = col.row(heading="comparison_function")
			row.enabled = not me.is_shared_asset
			row.prop(me, "comparison_function", text="")
			
			#row = col.row(heading="is_border_color_white")
			row = col.row()
			row.enabled = not me.is_shared_asset
			row.prop(me, "is_border_color_white", text="is_border_color_white")
			
			row = col.row(heading="unk1")
			row.enabled = not me.is_shared_asset
			row.prop(me, "unk1", text="")


class BlendIndicesPanel(bpy.types.Panel):
	"""Creates a Panel in the Mesh properties window"""
	bl_label = "Blend Indices"
	bl_idname = "OBJECT_PT_BlendIndices"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"
	ebm = dict()
	
	@classmethod
	def poll(cls, context):
		if context.mode == 'EDIT_MESH':
			me = context.edit_object.data
			fl = me.vertex_layers_int.get("blend_index1") or me.vertex_layers_int.new(name="blend_index1")
			f2 = me.vertex_layers_int.get("blend_index2") or me.vertex_layers_int.new(name="blend_index2")
			f3 = me.vertex_layers_int.get("blend_index3") or me.vertex_layers_int.new(name="blend_index3")
			f4 = me.vertex_layers_int.get("blend_index4") or me.vertex_layers_int.new(name="blend_index4")

			ret = False
			if fl:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			if f2:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			if f3:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			if f4:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True

			if ret == True:
				return True

		cls.ebm.clear()
		return False

	def draw(self, context):
		layout = self.layout
		me = context.edit_object.data
		layout.prop(me, "blend_index1")
		layout.prop(me, "blend_index2")
		layout.prop(me, "blend_index3")
		layout.prop(me, "blend_index4")


class BlendWeightsPanel(bpy.types.Panel):
	"""Creates a Panel in the Mesh properties window"""
	bl_label = "Blend Weights"
	bl_idname = "OBJECT_PT_BlendWeights"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"
	ebm = dict()

	@classmethod
	def poll(cls, context):
		if context.mode == 'EDIT_MESH':
			me = context.edit_object.data
			fl = me.vertex_layers_float.get("blend_weight1") or me.vertex_layers_float.new(name="blend_weight1")
			f2 = me.vertex_layers_float.get("blend_weight2") or me.vertex_layers_float.new(name="blend_weight2")
			f3 = me.vertex_layers_float.get("blend_weight3") or me.vertex_layers_float.new(name="blend_weight3")
			f4 = me.vertex_layers_float.get("blend_weight4") or me.vertex_layers_float.new(name="blend_weight4")

			ret = False
			if fl:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			if f2:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			if f3:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			if f4:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True

			if ret == True:
				return True

		cls.ebm.clear()
		return False

	def draw(self, context):
		layout = self.layout
		me = context.edit_object.data
		layout.prop(me, "blend_weight1")
		layout.prop(me, "blend_weight2")
		layout.prop(me, "blend_weight3")
		layout.prop(me, "blend_weight4")


class EdgeCosinesPanel(bpy.types.Panel):
	"""Creates a Panel in the Mesh properties window"""
	bl_label = "Edge Cosines"
	bl_idname = "OBJECT_PT_EdgeCosines"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"
	ebm = dict()
	
	@classmethod
	def poll(cls, context):
		if context.mode == 'EDIT_MESH':
			me = context.edit_object.data
			fl = me.polygon_layers_int.get("edge_cosine1") or me.polygon_layers_int.new(name="edge_cosine1")
			f2 = me.polygon_layers_int.get("edge_cosine2") or me.polygon_layers_int.new(name="edge_cosine2")
			f3 = me.polygon_layers_int.get("edge_cosine3") or me.polygon_layers_int.new(name="edge_cosine3")
			f4 = me.polygon_layers_int.get("edge_cosine4") or me.polygon_layers_int.new(name="edge_cosine4")

			ret = False
			if fl:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			if f2:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			if f3:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			if f4:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True

			if ret == True:
				return True

		cls.ebm.clear()
		return False

	def draw(self, context):
		layout = self.layout
		me = context.edit_object.data
		layout.prop(me, "edge_cosine1")
		layout.prop(me, "edge_cosine2")
		layout.prop(me, "edge_cosine3")
		layout.prop(me, "edge_cosine4")


class CollisionTagPanel(bpy.types.Panel):
	"""Creates a Panel in the Mesh properties window"""
	bl_label = "Collision Tag"
	bl_idname = "OBJECT_PT_CollisionTag"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"
	ebm = dict()
	
	@classmethod
	def poll(cls, context):
		if context.mode == 'EDIT_MESH':
			me = context.edit_object.data
			#fl = me.polygon_layers_int.get("collision_tag0") or me.polygon_layers_int.new(name="collision_tag0")
			fl = me.polygon_layers_int.get("collision_tag1") or me.polygon_layers_int.new(name="collision_tag1")
			
			ret = False
			if fl:
				cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
				ret = True
				#return True
			
			if ret == True:
				return True
		
		cls.ebm.clear()
		return False
	
	def draw(self, context):
		layout = self.layout
		me = context.edit_object.data
		#layout.prop(me, "collision_tag0")
		layout.prop(me, "collision_tag1")


def set_int_blend_index1(self, value):
	bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the bone indices layer
	blend_index = (bm.verts.layers.int.get("blend_index1") or bm.verts.layers.int.new("blend_index1"))

	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			af = elem
			break
	if af:
		af[blend_index] = value
		bmesh.update_edit_mesh(self)

def set_int_blend_index2(self, value):
	bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the bone indices layer
	blend_index = (bm.verts.layers.int.get("blend_index2") or bm.verts.layers.int.new("blend_index2"))

	#af = bm.verts.active
	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			#print("Active vertex:", elem)
			af = elem
			break
	if af:
		af[blend_index] = value
		bmesh.update_edit_mesh(self)

def set_int_blend_index3(self, value):
	bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the bone indices layer
	blend_index = (bm.verts.layers.int.get("blend_index3") or bm.verts.layers.int.new("blend_index3"))

	#af = bm.verts.active
	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			#print("Active vertex:", elem)
			af = elem
			break
	if af:
		af[blend_index] = value
		bmesh.update_edit_mesh(self)

def set_int_blend_index4(self, value):
	bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the bone indices layer
	blend_index = (bm.verts.layers.int.get("blend_index4") or bm.verts.layers.int.new("blend_index4"))

	#af = bm.verts.active
	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			#print("Active vertex:", elem)
			af = elem
			break
	if af:
		af[blend_index] = value
		bmesh.update_edit_mesh(self)

def get_int_blend_index1(self):
	bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	blend_index = bm.verts.layers.int.get("blend_index1") or bm.verts.layers.int.new("blend_index1")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			return(elem[blend_index])
	
	return 0

def get_int_blend_index2(self):
	bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	blend_index = bm.verts.layers.int.get("blend_index2") or bm.verts.layers.int.new("blend_index2")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			return(elem[blend_index])
	
	return 0

def get_int_blend_index3(self):
	bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	blend_index = bm.verts.layers.int.get("blend_index3") or bm.verts.layers.int.new("blend_index3")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			return(elem[blend_index])
	
	return 0

def get_int_blend_index4(self):
	bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	blend_index = bm.verts.layers.int.get("blend_index4") or bm.verts.layers.int.new("blend_index4")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			return(elem[blend_index])
	
	return 0


def set_float_blend_weight1(self, value):
	bm = BlendWeightsPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the bone weights layer
	blend_weight = (bm.verts.layers.float.get("blend_weight1") or bm.verts.layers.float.new("blend_weight1"))

	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			af = elem
			break
	if af:
		af[blend_weight] = value
		bmesh.update_edit_mesh(self)

def set_float_blend_weight2(self, value):
	bm = BlendWeightsPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the bone weights layer
	blend_weight = (bm.verts.layers.float.get("blend_weight2") or bm.verts.layers.float.new("blend_weight2"))

	#af = bm.verts.active
	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			#print("Active vertex:", elem)
			af = elem
			break
	if af:
		af[blend_weight] = value
		bmesh.update_edit_mesh(self)

def set_float_blend_weight3(self, value):
	bm = BlendWeightsPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the bone weights layer
	blend_weight = (bm.verts.layers.float.get("blend_weight3") or bm.verts.layers.float.new("blend_weight3"))

	#af = bm.verts.active
	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			#print("Active vertex:", elem)
			af = elem
			break
	if af:
		af[blend_weight] = value
		bmesh.update_edit_mesh(self)

def set_float_blend_weight4(self, value):
	bm = BlendWeightsPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the bone weights layer
	blend_weight = (bm.verts.layers.float.get("blend_weight4") or bm.verts.layers.float.new("blend_weight4"))

	#af = bm.verts.active
	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			#print("Active vertex:", elem)
			af = elem
			break
	if af:
		af[blend_weight] = value
		bmesh.update_edit_mesh(self)

def get_float_blend_weight1(self):
	bm = BlendWeightsPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	blend_weight = bm.verts.layers.float.get("blend_weight1") or bm.verts.layers.float.new("blend_weight1")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			return(elem[blend_weight])
	
	return 0

def get_float_blend_weight2(self):
	bm = BlendWeightsPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	blend_weight = bm.verts.layers.float.get("blend_weight2") or bm.verts.layers.float.new("blend_weight2")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			return(elem[blend_weight])
	
	return 0

def get_float_blend_weight3(self):
	bm = BlendWeightsPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	blend_weight = bm.verts.layers.float.get("blend_weight3") or bm.verts.layers.float.new("blend_weight3")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			return(elem[blend_weight])
	
	return 0

def get_float_blend_weight4(self):
	bm = BlendWeightsPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	blend_weight = bm.verts.layers.float.get("blend_weight4") or bm.verts.layers.float.new("blend_weight4")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMVert):
			return(elem[blend_weight])
	
	return 0


# def set_int_blend_indices(self, value):
	# bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# # get the bone indices layer
	# blend_index1 = (bm.verts.layers.int.get("blend_index1") or bm.verts.layers.int.new("blend_index1"))
	# blend_index2 = (bm.verts.layers.int.get("blend_index2") or bm.verts.layers.int.new("blend_index2"))
	# blend_index3 = (bm.verts.layers.int.get("blend_index3") or bm.verts.layers.int.new("blend_index3"))
	# blend_index4 = (bm.verts.layers.int.get("blend_index4") or bm.verts.layers.int.new("blend_index4"))

	# af = None
	# for elem in reversed(bm.select_history):
		# if isinstance(elem, bmesh.types.BMVert):
			# af = elem
			# break
	# if af:
		# af[blend_index1] = value[0]
		# af[blend_index2] = value[1]
		# af[blend_index3] = value[2]
		# af[blend_index4] = value[3]
		# bmesh.update_edit_mesh(self)

# def get_int_blend_indices(self):
	# bm = BlendIndicesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# # get the int layer
	# blend_index1 = bm.verts.layers.int.get("blend_index1")
	# blend_index2 = bm.verts.layers.int.get("blend_index2")
	# blend_index3 = bm.verts.layers.int.get("blend_index3")
	# blend_index4 = bm.verts.layers.int.get("blend_index4")

	# af = None
	# for elem in reversed(bm.select_history):
		# if isinstance(elem, bmesh.types.BMVert):
			# af = elem
			# break
	# if af:
		# return([af[blend_index1], af[blend_index2], af[blend_index3], af[blend_index4]])


def set_int_edge_cosine1(self, value):
	bm = EdgeCosinesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the edge cosine layer
	edge_cosine = (bm.faces.layers.int.get("edge_cosine1") or bm.faces.layers.int.new("edge_cosine1"))

	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			af = elem
			break
	if af:
		af[edge_cosine] = value
		bmesh.update_edit_mesh(self)

def set_int_edge_cosine2(self, value):
	bm = EdgeCosinesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the edge cosine layer
	edge_cosine = (bm.faces.layers.int.get("edge_cosine2") or bm.faces.layers.int.new("edge_cosine2"))

	#af = bm.faces.active
	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			#print("Active face:", elem)
			af = elem
			break
	if af:
		af[edge_cosine] = value
		bmesh.update_edit_mesh(self)

def set_int_edge_cosine3(self, value):
	bm = EdgeCosinesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the edge cosine layer
	edge_cosine = (bm.faces.layers.int.get("edge_cosine3") or bm.faces.layers.int.new("edge_cosine3"))

	#af = bm.faces.active
	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			#print("Active face:", elem)
			af = elem
			break
	if af:
		af[edge_cosine] = value
		bmesh.update_edit_mesh(self)

def set_int_edge_cosine4(self, value):
	bm = EdgeCosinesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the edge cosine layer
	edge_cosine = (bm.faces.layers.int.get("edge_cosine4") or bm.faces.layers.int.new("edge_cosine4"))

	#af = bm.faces.active
	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			#print("Active face:", elem)
			af = elem
			break
	if af:
		af[edge_cosine] = value
		bmesh.update_edit_mesh(self)

def get_int_edge_cosine1(self):
	bm = EdgeCosinesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	edge_cosine = bm.faces.layers.int.get("edge_cosine1") or bm.faces.layers.int.new("edge_cosine1")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			return(elem[edge_cosine])
	
	return 0

def get_int_edge_cosine2(self):
	bm = EdgeCosinesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	edge_cosine = bm.faces.layers.int.get("edge_cosine2") or bm.faces.layers.int.new("edge_cosine2")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			return(elem[edge_cosine])
	
	return 0

def get_int_edge_cosine3(self):
	bm = EdgeCosinesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	edge_cosine = bm.faces.layers.int.get("edge_cosine3") or bm.faces.layers.int.new("edge_cosine3")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			return(elem[edge_cosine])
	
	return 0

def get_int_edge_cosine4(self):
	bm = EdgeCosinesPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	edge_cosine = bm.faces.layers.int.get("edge_cosine4") or bm.faces.layers.int.new("edge_cosine4")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			return(elem[edge_cosine])
	
	return 0


def set_int_collision_tag0(self, value):
	bm = CollisionTagPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the collision tag layer
	collision_tag = (bm.faces.layers.int.get("collision_tag0") or bm.faces.layers.int.new("collision_tag0"))

	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			af = elem
			break
	if af:
		af[collision_tag] = value
		bmesh.update_edit_mesh(self)

def get_int_collision_tag0(self):
	bm = CollisionTagPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	collision_tag = bm.faces.layers.int.get("collision_tag0") or bm.faces.layers.int.new("collision_tag0")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			return(elem[collision_tag])
	
	return 0


def set_int_collision_tag1(self, value):
	bm = CollisionTagPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

	# get the collision tag layer
	collision_tag = (bm.faces.layers.int.get("collision_tag1") or bm.faces.layers.int.new("collision_tag1"))

	af = None
	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			af = elem
			break
	if af:
		af[collision_tag] = value
		bmesh.update_edit_mesh(self)

def get_int_collision_tag1(self):
	bm = CollisionTagPanel.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))
	collision_tag = bm.faces.layers.int.get("collision_tag1") or bm.faces.layers.int.new("collision_tag1")

	for elem in reversed(bm.select_history):
		if isinstance(elem, bmesh.types.BMFace):
			return(elem[collision_tag])
	
	return 0

def register():
	for klass in CLASSES:
		bpy.utils.register_class(klass)
	
	bpy.types.Mesh.blend_index1 = bpy.props.IntProperty(name="Index 1", description="Index of a tagpoint or drivenpoint", min=0, max=255, get=get_int_blend_index1, set=set_int_blend_index1)
	bpy.types.Mesh.blend_index2 = bpy.props.IntProperty(name="Index 2", description="Index of a tagpoint or drivenpoint", min=0, max=255, get=get_int_blend_index2, set=set_int_blend_index2)
	bpy.types.Mesh.blend_index3 = bpy.props.IntProperty(name="Index 3", description="Index of a tagpoint or drivenpoint", min=0, max=255, get=get_int_blend_index3, set=set_int_blend_index3)
	bpy.types.Mesh.blend_index4 = bpy.props.IntProperty(name="Index 4", description="Index of a tagpoint or drivenpoint", min=0, max=255, get=get_int_blend_index4, set=set_int_blend_index4)
	#bpy.types.Mesh.blend_indices = bpy.props.IntVectorProperty(name="Indices", description="Indices of tagpoints or drivenpoints", min=0, max=255, size=4, get=get_int_blend_indices, set=set_int_blend_indices)
	
	bpy.types.Mesh.blend_weight1 = bpy.props.FloatProperty(name="Weight 1", description="Weight to a tagpoint or drivenpoint", min=0.0, max=100.0, get=get_float_blend_weight1, set=set_float_blend_weight1)
	bpy.types.Mesh.blend_weight2 = bpy.props.FloatProperty(name="Weight 2", description="Weight to a tagpoint or drivenpoint", min=0.0, max=100.0, get=get_float_blend_weight2, set=set_float_blend_weight2)
	bpy.types.Mesh.blend_weight3 = bpy.props.FloatProperty(name="Weight 3", description="Weight to a tagpoint or drivenpoint", min=0.0, max=100.0, get=get_float_blend_weight3, set=set_float_blend_weight3)
	bpy.types.Mesh.blend_weight4 = bpy.props.FloatProperty(name="Weight 4", description="Weight to a tagpoint or drivenpoint", min=0.0, max=100.0, get=get_float_blend_weight4, set=set_float_blend_weight4)
	
	bpy.types.Mesh.edge_cosine1 = bpy.props.IntProperty(name="Edge cosine 1", description="Edge cosine", min=0, max=255, get=get_int_edge_cosine1, set=set_int_edge_cosine1)
	bpy.types.Mesh.edge_cosine2 = bpy.props.IntProperty(name="Edge cosine 2", description="Edge cosine", min=0, max=255, get=get_int_edge_cosine2, set=set_int_edge_cosine2)
	bpy.types.Mesh.edge_cosine3 = bpy.props.IntProperty(name="Edge cosine 3", description="Edge cosine", min=0, max=255, get=get_int_edge_cosine3, set=set_int_edge_cosine3)
	bpy.types.Mesh.edge_cosine4 = bpy.props.IntProperty(name="Edge cosine 4", description="Edge cosine", min=0, max=255, get=get_int_edge_cosine4, set=set_int_edge_cosine4)
	
	#bpy.types.Mesh.collision_tag0 = bpy.props.IntProperty(name="Collision tag 0", description="Collision tag", min=0, max=0xFFFF, get=get_int_collision_tag0, set=set_int_collision_tag0)
	bpy.types.Mesh.collision_tag1 = bpy.props.IntProperty(name="Collision tag 1", description="Collision tag", min=0, max=0xFFFF, get=get_int_collision_tag1, set=set_int_collision_tag1)
	
	bpy.types.Image.is_shared_asset = bpy.props.BoolProperty(name='is_shared_asset', description="Define if the data is a shared asset or not", default=False)
	bpy.types.Image.dimension = bpy.props.IntProperty(name='dimension', description='Textures array size or texture type of the image', min=0, max=0xFFFF, default=1)
	bpy.types.Image.main_mipmap = bpy.props.IntProperty(name='main_mipmap', description='Textures main mipmap number', min=0, max=0xFF, default=-1)
	bpy.types.Image.unk_0x34 = bpy.props.IntProperty(name='unk_0x34', description='unk_0x34', default=0x5C0C0)
	bpy.types.Image.unk_0x38 = bpy.props.IntProperty(name='unk_0x38', description='unk_0x38', default=0x7AFEE50)
	bpy.types.Image.flags = bpy.props.IntProperty(name='flags', description='flags', default=-1)
	
	bpy.types.ShaderNodeTexImage.is_shared_asset = bpy.props.BoolProperty(name='is_shared_asset', description="Define if the data is a shared asset or not", default=False)
	bpy.types.ShaderNodeTexImage.addressing_mode = bpy.props.IntVectorProperty(name='addressing_mode', description="Technique used for resolving texture coordinates outside of texture's boundaries (U, V, W)", size=3, min=1, max=5, default=(1, 1, 1))
	bpy.types.ShaderNodeTexImage.filter_types = bpy.props.IntVectorProperty(name='filter_types', description="Type of magnification or minification sampler filter (magnification, minification, mipmap)", size=3, min=0, max=1, default=(1, 1, 1))
	bpy.types.ShaderNodeTexImage.min_max_lod = bpy.props.FloatVectorProperty(name='min_max_lod', description="Minimum lod and maximum lod", size=2, default=unpack("<ff", b'\xFF\xFF\x7F\xFF\xFF\xFF\x7F\x7F'))
	bpy.types.ShaderNodeTexImage.max_anisotropy = bpy.props.IntProperty(name='max_anisotropy', description="Maximum anisotropy", default=1)
	bpy.types.ShaderNodeTexImage.mipmap_lod_bias = bpy.props.FloatProperty(name='mipmap_lod_bias', description="Mipmap lod bias", default=-0.9)
	bpy.types.ShaderNodeTexImage.comparison_function = bpy.props.IntProperty(name='comparison_function', description="Type of comparison option", min=-1, max=8, default=-1)
	bpy.types.ShaderNodeTexImage.is_border_color_white = bpy.props.BoolProperty(name='is_border_color_white', description="Is border color white", default=False)
	bpy.types.ShaderNodeTexImage.unk1 = bpy.props.IntProperty(name='unk1', description="unk1 (0x30)", default=1)


def unregister():
	for klass in CLASSES:
		bpy.utils.unregister_class(klass)
	
	delattr(bpy.types.Mesh, "blend_index1")
	delattr(bpy.types.Mesh, "blend_index2")
	delattr(bpy.types.Mesh, "blend_index3")
	delattr(bpy.types.Mesh, "blend_index4")
	
	delattr(bpy.types.Mesh, "blend_weight1")
	delattr(bpy.types.Mesh, "blend_weight2")
	delattr(bpy.types.Mesh, "blend_weight3")
	delattr(bpy.types.Mesh, "blend_weight4")
	
	delattr(bpy.types.Mesh, "edge_cosine1")
	delattr(bpy.types.Mesh, "edge_cosine2")
	delattr(bpy.types.Mesh, "edge_cosine3")
	delattr(bpy.types.Mesh, "edge_cosine4")
	
	#delattr(bpy.types.Mesh, "collision_tag0")
	delattr(bpy.types.Mesh, "collision_tag1")
	
	delattr(bpy.types.Image, "is_shared_asset")
	delattr(bpy.types.Image, "dimension")
	delattr(bpy.types.Image, "unk_0x34")
	delattr(bpy.types.Image, "unk_0x38")
	delattr(bpy.types.Image, "flags")
	
	delattr(bpy.types.ShaderNodeTexImage, "is_shared_asset")
	delattr(bpy.types.ShaderNodeTexImage, "addressing_mode")
	delattr(bpy.types.ShaderNodeTexImage, "filter_types")
	delattr(bpy.types.ShaderNodeTexImage, "min_max_lod")
	delattr(bpy.types.ShaderNodeTexImage, "max_anisotropy")
	delattr(bpy.types.ShaderNodeTexImage, "mipmap_lod_bias")
	delattr(bpy.types.ShaderNodeTexImage, "comparison_function")
	delattr(bpy.types.ShaderNodeTexImage, "is_border_color_white")
	delattr(bpy.types.ShaderNodeTexImage, "unk1")


CLASSES = [BlendIndicesPanel, BlendWeightsPanel, EdgeCosinesPanel, CollisionTagPanel, ImagePropertiesPanel, NodePropertiesPanel]


if __name__ == "__main__":
	register()
