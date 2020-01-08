from PIL import Image, ImageOps


class Emblem():
	"""
	A class that represents an emblem, the images on the flag
	:param texture: name of emblem file + ending
	:type texture: str
	:param colors: list of Color objects
	:type colors: list
	:param position: position in %
	:type position: tuple
	:param scale: size in %, negative means to the other direction
	:type scale: tuple
	:param rotation: rotation in degrees
	:type rotation: int
	"""

	def __init__(self, texture, colors, position=(0, 0), scale=(1, 1), rotation=0):
		self.texture = texture
		self.colors = colors
		self.position = position
		self.rotation = int(rotation)
		self.scale = scale

	def make_emblem(self, size: int):
		try:
			raw_texture = Image.open(f'colored_emblems/{self.texture}')
		except Exception:
			raw_texture = Image.open(f'textured_emblems/{self.texture}')
		emblem = raw_texture.convert('RGBA')

		if self.scale[0] < 0:
			emblem = ImageOps.mirror(emblem)
		if self.scale[1] < 0:
			emblem = ImageOps.flip(emblem)

		# resize
		emblem = emblem.resize((
			abs(int(size * self.scale[0])),
			abs(int(size * self.scale[1]))
		))
		# rotated
		emblem = emblem.rotate(self.rotation)

		#TODO: recolor

		return emblem

	def __str__(self) -> 'To print the emblem':
		return_string = []
		return_string.append(f'self.texture => {str(self.texture)}') 
		return_string.append(f'self.colors => {str([str(color) for color in self.colors])}') 
		return_string.append(f'self.position => {str(self.position)}') 
		return_string.append(f'self.rotation => {str(self.rotation)}') 
		return_string.append(f'self.scale => {str(self.scale)}') 

		return '\n'.join(return_string)
