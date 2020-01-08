import colorsys


class Color():
	"""docstring for Color"""

	def __init__(self, color: tuple):
		if (color[0] + color[1] + color[2]) / 3 == 0 or (color[0] + color[1] + color[2]) / 3 >= 1:
			self.rgb = tuple(int(c) for c in color)
		else:
			self.rgb = self.hsv_to_rgb(*color)

	def hsv_to_rgb(self, h, s, v):
		return tuple(int(round(i * 255)) for i in colorsys.hsv_to_rgb(h, s, v))

	def __str__(self) -> 'To print the color':
		return str(self.rgb)
