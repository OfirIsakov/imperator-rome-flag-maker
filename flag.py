from PIL import Image


# some constants, the average RGB of the first 2 colors on the flag background individually - red and yellow
FLAG_COLORS = {
	'color1': 128,
	'color2': 213,
}


class Flag():
	"""
	A class that represents an emblem, the images on the flag
	:param name: name of flag
	:type name: str
	:param pattern: name of pattern file + ending
	:type pattern: str
	:param colors: list of Color obj
	:type colors: list
	:param colored_emblems: list of Emblem objects
	:type colored_emblems: list
	:param size: size of the flag in pixels
	:type size: int
	"""

	def __init__(self, name, pattern, colors, colored_emblems=[], size=1024):
		self.name = name
		self.pattern = pattern
		self.colors = colors
		self.colored_emblems = colored_emblems
		self.size = size

	def make_background(self):
		raw_pattern = Image.open(f'patterns/{self.pattern}')
		background = raw_pattern.convert('RGBA')

		background = background.resize((self.size, self.size))

		background_data = background.load()

		for y in range(background.size[1]):
			for x in range(background.size[0]):
				flag_sum = 0
				for i in background_data[x, y][:3]:
					flag_sum += int(i) 
				flag_sum //= 3
				if flag_sum <= FLAG_COLORS['color1']:
					background_data[x, y] = self.colors[0].rgb
				elif FLAG_COLORS['color1'] < flag_sum <= FLAG_COLORS['color2']:
					background_data[x, y] = self.colors[1].rgb
				else:
					background_data[x, y] = self.colors[2].rgb

		return background

	def attach_emblems(self, background: Image):
		flag = background
		i = 0
		for emblem in self.colored_emblems:
			i += 1
			# turn emblem object into image
			current_emblem = emblem.make_emblem(self.size)

			# calculate the offset to paste the image onto
			offset = (
				int((self.size * emblem.position[0])) - (current_emblem.width // 2),
				int((self.size * emblem.position[1])) - (current_emblem.height // 2)
			)

			# paste emblem on background
			flag.paste(current_emblem, offset, current_emblem)
		return flag

	def set_emblems(self, colored_emblems: 'emblem list'):
		self.colored_emblems = colored_emblems

	def export_flag(self):
		background = self.make_background()

		flag = self.attach_emblems(background)

		flag.save(f'flags/{self.name}.png', 'png')

	def __str__(self) -> 'str to print the flag':
		flag_description = []
		flag_description.append(f'Name: {self.name}') 
		flag_description.append(f'Pattern: {self.pattern}') 
		flag_description.append(f'Colors: {self.colors}') 
		flag_description.append(f'Colored_emblems: ' + str([str(em.__str__()) for em in self.colored_emblems])) 


		return '\n'.join(flag_description)
