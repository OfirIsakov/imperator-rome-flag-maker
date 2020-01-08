# Python 3.7
from flag import Flag
from color import Color
from emblem import Emblem
import yaml
import re


SIZE = 512
COLORS_FILE = 'colors.txt'
NAMES_LANGUAGE = 'l_english'
NAMES_FILE = 'names.yml'
FLAGS_FILE = 'countries.txt'


def parse_names() -> 'dict of names':
	with open(NAMES_FILE, 'r') as names_file:
		raw_data = names_file.readlines()
	
	# remove all the comments in the yaml file, comments cause it to fail
	for line in range(len(raw_data)):
		if '#' in raw_data[line]:
			raw_data[line] = []

	raw_data = ''.join(list(filter(None, raw_data)))

	raw_data = re.sub('[0-9]', '', raw_data)
	with open(NAMES_FILE, 'w') as names_file:
		names_file.write(raw_data)

	# load yaml file into dict
	with open(NAMES_FILE, 'r') as names_file:
		names = yaml.safe_load(names_file)
	return names[NAMES_LANGUAGE]


def parse_colors() -> 'dict of Color objects':
	# read raw file
	with open(COLORS_FILE, 'r') as color_file:
		raw_file = color_file.readlines()

	# parse and remove comments- starts with #
	raw_colors = {}
	for line_number in range(len(raw_file)):
		try:
			raw_file[line_number] = re.findall(r'.*(?=#)', raw_file[line_number])[0]
		except Exception:
			pass
		color = []
		color = re.split(r"\s*=\s*", raw_file[line_number])
		if len(color) == 2:
			raw_colors[color[0]] = color[1]

	# parse the raw colors into color objects
	colors = {}
	for color in raw_colors.keys():
		if '{' in raw_colors[color] and '}' in raw_colors[color]:
			current_color = re.findall(r'(?={\s*).*(?=\s*})', raw_colors[color])[0]
			current_color = re.split(r' +', current_color)[1:]
			new_color = []
			# filter(lambda c: if c is not '': new_color.append(float(c)), current_color)
			for c in current_color:
				if c is not '':
					new_color.append(float(c))	
			color = color.replace('\t', '').replace(' ', '')
			colors[color] = Color(tuple(new_color))
	return colors


def parse_emblem(chunk: str, colors_dict: dict, defaults: "dict of default colors in case countries file don't specify") -> 'list of Emblem objects':
	emblems = []

	# find instance count
	instances_count = chunk.count('instance')
	chunk = list(filter(None, ''.join(chunk).split('}')))
	chunk = list(filter(None, '\n'.join(chunk).split('{')))
	chunk = list(filter(None, '\n'.join(chunk).split('\n')))[1:]
	while not chunk == []:
		is_instance = False
		colors = []
		# defining the default properties
		# ignoring depth because I have no clue what it does
		scale = (1, 1)
		rotation = 0
		position = (0.5, 0.5)

		while True:
			try:
				info = chunk[0]
			except Exception:
				break
			if not re.findall(r'(colored_emblem|texture_emblem|textured_emblem)', info) == []:
				break
			if 'texture' in info:
				texture = re.findall(r'([A-z0-9_]*\.dds|[A-z0-9_]*\.tga)', info)[0]
			if 'instance' in info:
				if is_instance:
					emblems.append(Emblem(texture, colors, position, scale, rotation))
					# defining the default properties
					# ignoring depth because I have no clue what it does
					scale = (1, 1)
					rotation = 0
					position = (0.5, 0.5)
				is_instance = True
			if 'position' in info:
				position = re.split(r' +', chunk[1])
				position = tuple([float(number) for number in tuple(filter(None, position))])
			if 'scale' in info:
				scale = re.split(r' +', chunk[1])
				scale = tuple([float(number) for number in tuple(filter(None, scale))])
			if 'rotation' in info:
				rotation = re.split(r'= *', info)[1]
				rotation = re.findall(r'-?[0-9]*', rotation)
				rotation = float(rotation[0])
			if 'color' in info:
				colors.append(colors_dict[info.split('=')[-1].replace('"', '').replace(' ', '')])
			chunk.pop(0)
		try:
			chunk.pop(0)
		except Exception:
			pass
		emblems.append(Emblem(texture, colors, position, scale, rotation))
	return emblems


def parse_flag_chunk(chunk: list, colors_dict: dict, names: dict) -> Flag:
	name = re.match(r'[A-Z]*_*[A-Z]*', chunk[0])[0]
	chunk.pop(0)

	try:
		name = names[name]
	except Exception:
		pass

	# scan for the background elements
	background = re.split(r'(colored_emblem|texture_emblem|textured_emblem)\s*=\s*{', ''.join(chunk))[0]
	background = '\n'.join(background.split('\t'))

	# parsing pattern
	pattern = re.findall(r'pattern\s*=\s*"?.*"?', background)
	pattern = re.findall(r'[A-z0-9]*[.]tga', pattern[0])[0]

	# parsing background colors
	colors = re.findall(r'color[0-9]\s*=\s*"?.*"?(?=\t)?', background)
	colors = [colors_dict[color.split('=')[-1].replace('"', '').replace(' ', '')] for color in colors]

	# make flag object
	flag = Flag(name, pattern, colors, size=SIZE)

	# scan for emblems and add them to the flag object
	defaults = {
	'colors': colors
	}
	emblems = []
	chunk = '\n'.join(chunk).replace('\t', '\n').replace('    ', '\n')
	chunk = re.split(r'(colored_emblem|texture_emblem|textured_emblem)\s*=\s*{', ''.join(chunk))[1:]
	while not chunk == []:
		chunk = ''.join(chunk)
		emblems = parse_emblem(re.split(r'(colored_emblem|texture_emblem|textured_emblem)\s*=\s*{', chunk)[0], colors_dict, defaults)
		chunk = re.split(r'(colored_emblem|texture_emblem)\s*=\s*{', chunk)[1:]

	flag.set_emblems(emblems)
	return flag


def main():
	# read brackets with counter, start with 0, +1 every: { and -1 every: }
	# maybe recursion to do this every time, like for the emblem inside

	names = parse_names()
	colors = parse_colors()
	with open(FLAGS_FILE, 'r') as f:
		raw_data = f.readlines()


	flag_count = 0
	bracket_count = 0
	chunk = []
	for line in raw_data:
		bracket_count += line.count('{')
		bracket_count -= line.count('}')
		if bracket_count == 0:
			if not chunk == []:
				flag = parse_flag_chunk(chunk, colors, names)
				print(f'{flag_count}: {flag.name}')
				flag.export_flag()
				chunk = []
				flag_count += 1
		elif bracket_count > 0:
			chunk.append(line)



if __name__ == "__main__":
	main()
