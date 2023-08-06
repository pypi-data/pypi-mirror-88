import moderngl as mgl
import numpy.core as np
from collections import namedtuple

from .mathutils import fvec3, fvec4
from .rendering import Display
from .common import ressourcedir
from . import settings

SVertex = namedtuple('SVertex', ['space', 'pos', 'normal', 'color', 'layer', 'track', 'flags'])

class Scheme:
	def __init__(self, vertices=None, spaces=None, primitives=None, annotation=True, **kwargs):
		self.vertices = vertices or [] # list of vertices
		self.spaces = spaces or []	# definition of each space
		self.primitives = primitives or {} # list of indices for each shader
		self.components = []	# displayables associated to spaces
		self.annotation = annotation	# flag saying if this object is an annotation
		# for creation: last vertex inserted
		self.current = {'color':settings.display['annotation_color'], 'flags':0, 'layer':0, 'space':0, 'shader':'wire', 'track':0}
		self.set(**kwargs)
		
	def set(self, *args, **kwargs):
		''' change the specified attributes in the current default vertex definition '''
		if args:
			if len(args) == 1 and isinstance(args[0], dict):
				kwargs = args[0]
			else:
				raise TypeError('Scheme.set expects keywords argument or one unique dictionnary argument')
		self.current.update(kwargs)
		# register the space if not already known
		if not isinstance(self.current['space'], int):
			try:	i = self.spaces.index(self.current['space'])
			except IndexError:	
				i = len(self.spaces)
				self.spaces.append(self.current['space'])
			self.current['space'] = i
	
	def add(self, obj, **kwargs):
		''' add an object to the scheme
			if it is a mesh it's merged in the current buffers 
			else it is added as a component to the current space
		'''
		self.set(kwargs)
		l = len(self.faces)
		
		if isinstance(obj, Container):
			self.vertices.extend((SVertex(pos=p, **self.current)  for p in obj.points))
		if isinstance(obj, Mesh):
			faces = self.primitives[self.current['shader']]
			faces.extend(((a+l, b+l, c+l)  for a,b,c in obj.faces))
			for f, track in zip(obj.faces, obj.tracks):
				for p in f:
					self.vertices[p+l].track = track
			for i,n in enumerate(obj.vertexnormals()):
				self.vertices[i+l].normal = n
		elif isinstance(obj, Web):
			edges = self.primitives[self.current['shader']]
			edges.extend(((a+l, b+l)  for a,b in obj.edges))
			for e, track in zip(obj.edges, obj.tracks):
				for p in e:
					self.vertices[p+i].track = track
		elif isinstance(obj, Wire):
			self.add(web(obj))
		
		elif hasattr(obj, '__iter__'):
			for obj in obj:
				handled = True
				if isinstance(obj, fvec3):
					self.vertices.append(SVertex(pos=obj))
				elif isinstance(obj, tuple):
					self.vertices.append(SVertex(*obj))
				elif isinstance(obj, SVertex):
					self.vertices.append(obj)
				else:
					self.add(obj)
					handled = False
				if handled:
					self.primitives[self.current['shader']]
		else:
			self.component(obj)
	
	def component(self, obj, **kwargs):
		''' add an object as component associated to the current space '''
		self.set(**kwargs)
		self.components.append((self.current['space'], mesh))
	
	class display(Display):
		''' display for schemes
			
			attributes:
			:spaces:       numpy array of matrices for each space, sent as uniform to the shader
			:vb_vertices:  vertex buffer for vertices
			:vas:          vertex array associated to each shader
		'''
		def __init__(self, scene, sch):
			ctx = scene.ctx
			# set display params
			self.annotation = sch.annotation
			
			# load the ressources
			self.shaders, self.shader_ident = scene.ressource('scheme', self.load)
			
			# switch to array indexed spaces
			self.spaceindex = {}
			self.spacegens = list(sch.spaces)
			self.spaces = np.empty((len(sch.spaces), 4,4), 'f4')
			
			# prepare the buffer of vertices
			vertices = np.empty(len(sch.vertices), 'u1, 3f4, 3f4, 4u1, f4, u2, u1')
			for i,v in enumerate(sch.vertices):
				vertices[i][0] = (
					*v[:3],
					bvec3(glm.round(v.color*255)), 
					*v[4:]
					)
			self.vb_vertices = ctx.buffer(vertices)
			verticesdef = [(self.vb_vertices, 'u1, 3f4, 3f4, 4f1, f4, u2, u1', 
								'space', 
								'v_position', 
								'v_normal', 
								'v_color', 
								'layer', 
								'ident', 
								'flags')]
			
			# prepare the rending commands
			ident_triangles = []
			ident_lines = []
			self.vas = {}
			self.vai_triangles = None
			self.vai_lines = None
			for shname,batch in sch.primitives.items():
				if not batch:	continue
				if shname not in shader:	raise KeyError('no shader for name {}'.format(repr(shname)))
				
				prim, shader = self.shaders[shname]
				vb_indices = ctx.buffer(np.array(batch, 'u4'))
				vas[shname] = ctx.vertex_array(shader, verticesdef, vb_indices)
				if prim == mgl.LINES:			ident_triangles.extend(batch)
				elif prim == mgl.TRIANGLES:		ident_lines.extend(batch)
			
			if ident_triangles:	self.vai_triangles	= ctx.vertex_array(self.shader_ident, verticesdef, ctx.buffer(np.array(ident_triangles, 'u4')))
			if ident_lines:		self.vai_lines 		= ctx.vertex_array(self.shader_ident, verticesdef, ctx.buffer(np.array(ident_lines, 'u4')))
			
		
		def load(self, scene):
			''' load shaders and all static data for the current opengl context '''
			shader_ident = scene.ctx.program(
						vertex_shader=open(ressourcedir+'/shaders/scheme_ident.vert').read(),
						fragment_shader=open(ressourcedir+'/shaders/scheme_ident.frag').read(),
						)
			shaders = {
				'wire': (glm.LINES, scene.ctx.program(
						vertex_shader=open(ressourcedir+'/shaders/scheme.vert').read(),
						fragment_shader=open(ressourcedir+'/shaders/scheme_uniform.frag').read(),
						)),
				'uniform': (glm.TRIANGLES, scene.ctx.program(
						vertex_shader=open(ressourcedir+'/shaders/scheme.vert').read(),
						fragment_shader=open(ressourcedir+'/shaders/scheme_uniform.frag').read(),
						)),
				'transp': (glm.TRIANGLES, scene.ctx.program(
						vertex_shader=open(ressourcedir+'/shaders/scheme.vert').read(),
						fragment_shader=open(ressourcedir+'/shaders/scheme_transp.frag').read(),
						)),
				}
			return shaders, shader_ident
			
		def compute_spaces(self, view):
			''' computes the new spaces for this frame
				this is meant to be overriden when new spaces are required 
			'''
			view.uniforms['world'] = self.world
			for i,gen in enumerate(self.spacegens):
				self.spaces[i] = gen(self)
		
		def render(self, view):
			''' render each va in self.vas '''
			self.compute_spaces(view)
			for name in self.vas:
				shader = self.shaders[name]
				prim, va = self.vas[name]
				shader['spaces'].write(self.spaces)
				shader['proj'].write(view.uniforms['proj'])
				va.render(prim)
		
		def identify(self, view):
			''' render all the triangles and lines for identification '''
			self.shader_ident['startident'] = view.identstep(1)
			self.shader_ident['spaces'].write(self.spaces)
			self.shader_ident['proj'].write(view.uniforms['proj'])
			
			if self.vai_lines:		self.vai_lines.render(mgl.LINES)
			if self.vai_triangles:	self.vai_triangles.render(mgl.TRIANGLES)
		
		def stack(self, scene):
			return (	((), 'screen', 1, self.render), 
						((), 'ident', 1, self.identify),   )

# create standard spaces

def view(view):
	proj = view.uniforms['proj']
	return fmat4(1/proj[0][0],  0,0,0,
				0, 1/proj[1][1], 0,0,
				0,0,1,0,
				0,0,0,1)

def screen(view):
	return fmat4(view.width()/2,0,0,0,
				0,view.height()/2,0,0,
				0,0,1,0,
				0,0,0,1)

def world(view):
	return view.uniforms['view'] * view.uniforms['world']

def halo_world(position):
	def mat(view):
		center = view.uniforms['view'] * view.uniforms['world'] * position
		m = fmat4(1)
		m[3] = fvec4(center,1)
		return m
	return mat
def halo_view(position):
	def mat(view):
		center = view.uniforms['view'] * view.uniforms['world'] * position
		proj = view.uniforms['proj']
		m = fmat4(1)
		m[0][0] = center.z/proj[0][0]
		m[1][1] = center.z/proj[1][1]
		return m
	return mat
def halo_screen(position)
	def mat(view):
		center = view.uniforms['view'] * view.uniforms['world'] * position
		proj = view.uniforms['proj']
		m = fmat4(1)
		m[0][0] = center.z/view.width()
		m[1][1] = center.z/view.height()
		return m
	return mat

		

sch = Scheme(color=settings.display['annotation'])
textspace = halo_screen(textpos)
sch.set(shader='wire', space=textspace)
sch.add([vec3(0,bottom,0), vec3(0,top,0), vec3(width,top,0), vec3(width,bottom,0)])
sch.add([	(world, vec3(0,0,0)), 
			(textspace, vec3(10,10,0)), 
			(textspace, vec3(10)),
			])
sch.set(space=halo_screen(textpos), shader='bold')
sch.add(cone((o-10*z,-z), 5, 10))
sch.add(Web(...), space=world)
