import bpy
import random
import mathutils

drone_model_path= './drone.obj'
image_output_path='./drone_output_images'

# Set up the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.render.resolution_x = 400
bpy.context.scene.render.resolution_y = 400
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.world = bpy.data.worlds.new("World")
bpy.context.scene.world.use_nodes = True

# Set the render settings for alpha transparency
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# Enabling transparent film settigns
bpy.context.scene.render.film_transparent = True
bpy.context.scene.view_layers[0].use_pass_combined = True
bpy.context.scene.view_layers[0].use_pass_z = True

# Load the 3D model
bpy.ops.import_scene.obj(filepath=drone_model_path)


# Set up the light
light = bpy.data.lights.new(name="Light", type='POINT')
light_obj = bpy.data.objects.new(name="Light", object_data=light)
light_obj.location = (0.0, 0.0, 100.0)
bpy.context.scene.collection.objects.link(light_obj)

# Get the bounding box of the imported object
bbox_corners = [mathutils.Vector(corner) for corner in bpy.context.selected_objects[0].bound_box]
bbox_center = sum(bbox_corners, mathutils.Vector()) / 8.0


def create_infrared_material(random_grey):
    material = bpy.data.materials.new("InfraredMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Create nodes
    out_node = nodes.new(type='ShaderNodeOutputMaterial')
    mix_node = nodes.new(type='ShaderNodeMixShader')
    emission_node = nodes.new(type='ShaderNodeEmission')
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
    attr_node = nodes.new(type='ShaderNodeAttribute')
    math_node = nodes.new(type='ShaderNodeMath')

    # Configure nodes
    attr_node.attribute_name = "Col"
    #random_grey=0.4
    color_ramp_node.color_ramp.elements[0].color = (random_grey, random_grey, random_grey, 1) #1
    color_ramp_node.color_ramp.elements[1].color = (0, 0, 0, 1) # 0
    math_node.operation = 'MULTIPLY'
    math_node.inputs[1].default_value = 5.0

    # Link nodes
    links.new(attr_node.outputs['Color'], color_ramp_node.inputs['Fac'])
    links.new(color_ramp_node.outputs['Color'], math_node.inputs[0])
    links.new(math_node.outputs['Value'], emission_node.inputs['Strength'])
    links.new(emission_node.outputs['Emission'], mix_node.inputs[1])
    links.new(bsdf_node.outputs['BSDF'], mix_node.inputs[2])
    links.new(color_ramp_node.outputs['Color'], emission_node.inputs['Color'])
    links.new(mix_node.outputs['Shader'], out_node.inputs['Surface'])

    return material


# Render 10 images with random camera positions and light intensities
for i in range(4):
    # Set up the camera with random position and rotation
    camera_data = bpy.data.cameras.new('Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)
    camera_object.location = (random.uniform(-125, 125), random.uniform(-125, 125), random.uniform(-75, 75))

    # Calculate camera direction to face the drone object
    camera_direction = bbox_center - camera_object.location
    distance = camera_direction.length
    camera_direction = camera_direction / distance

    # Set camera position to be 250 units away from the center of the drone object
    camera_object.location = bbox_center - 250.0 * camera_direction

    # Calculate camera rotation to look at center of bounding box
    camera_rotation = camera_direction.to_track_quat('-Z', 'Y').to_euler()

    # Apply rotation to camera object
    camera_object.rotation_euler = camera_rotation

    # Add the camera to the scene collection and set as active camera
    bpy.context.scene.collection.objects.link(camera_object)
    bpy.context.scene.camera = camera_object

    # Set light intensity to a random value between 500 and 1500
    light_obj.data.energy = random.uniform(200, 300)
    
    # Set drone material
    random_grey = random.uniform(0.4, 1)
    # Apply infrared material to the drone object
    infrared_material = create_infrared_material(random_grey)
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            if not obj.data.materials:
                obj.data.materials.append(infrared_material)
            else:
                obj.data.materials[0] = infrared_material

    # Render the scene with alpha transparency and save the image
    bpy.context.scene.render.use_freestyle = False
    bpy.context.scene.render.use_compositing = False
    bpy.context.scene.render.filepath = f'./drone_output_imaegs/{i+1}.png'
    bpy.ops.render.render(write_still=True, use_viewport=True)

    # Remove the camera object from the scene
    bpy.context.scene.collection.objects.unlink(camera_object)
    bpy.data.objects.remove(camera_object)
