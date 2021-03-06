import harfang as hg
import json
from utils import *
from screen_specs import *


def wireframe_json_to_segment_list(filename=None):
	segment_list = []

	if filename is not None and hg.GetFilesystem().Exists(filename):
		with open(hg.GetFilesystem().MapToAbsolute(filename), 'r') as fp:
			data = json.load(fp)

		# print(data)

		for _object in data:
			_object_dict = data[_object]['object']

			_object_name = _object_dict['object_name']
			print('Found an object, named \'%s\'' % _object_name)

			for _segment in _object_dict['segments']:
				for _vertex_as_array in _segment:
					# print(_vertex_as_array)
					segment_list.append(_vertex_as_array)
					# _vertex = Vector3()

				if len(_object_dict['segments']) > 0:
					segment_list.append(_object_dict['segments'][-1])

	print("found total " + str(len(segment_list)) + " segment(s).")
	return segment_list


def get_sprite_seq_max_frame(filename_base, file_extension=".png"):
	n = 0
	while hg.GetFilesystem().Exists("@assets/" + filename_base + str(n) + file_extension):
		n += 1

	return n


def render_strings_array(strings=None, fade=1.0, fonts_dict={}, plus=None):
	if plus is None:
		return

	rsys = plus.GetRenderSystem()
	plus.GetRenderer().EnableBlending(True)
	plus.GetRenderer().EnableDepthTest(False)

	for line in strings:
		font_key = line[4] + "_" + str(line[5])
		if not (font_key in fonts_dict):
			fonts_dict[font_key] = hg.RasterFont("@assets/" + line[4] + ".ttf", int(line[5] * zoom_size() / 3), 512)

		rect = fonts_dict[font_key].GetTextRect(rsys, line[0])
		x = (demo_screen_size[0] - rect.GetWidth()) * 0.5
		y = (amiga_screen_size[1] - line[1]) * zoom_size()
		plus.Text2D(x, y, line[0], int(line[5] * zoom_size() / 3), hg.Color.White * fade, "@assets/" + line[4] + ".ttf")

	plus.GetRenderer().EnableBlending(False)

	# underline ?
	for line in strings:
		if line[3] == 1:
			font_key = line[4] + "_" + str(line[5])
			rect = fonts_dict[font_key].GetTextRect(rsys, line[0])
			x = (demo_screen_size[0] - rect.GetWidth()) * 0.5
			y = (amiga_screen_size[1] - line[1]) * zoom_size() - (line[5] * 0.2 * zoom_size() / 3)
			plus.Line2D(x, y, x + rect.GetWidth(), y, hg.Color.White * fade * fade, hg.Color.White * fade * fade)

	return fonts_dict


def render_text_screen(strings=None, duration=4.0, fade_duration=1.0, render_callback=None, plus=None, exit_callback=None):

	if strings is None:
		return

	if plus is None:
		return

	fonts_dict = {}
	fx_timer = 0.0
	while fx_timer < duration:
		if exit_callback is not None:
			exit_callback()
		dt_sec = hg.time_to_sec_f(plus.UpdateClock())
		fx_timer += dt_sec

		if fx_timer < fade_duration:
			fade = RangeAdjust(fx_timer, 0.0, fade_duration, 0.0, 1.0)
		else:
			if fx_timer < duration - fade_duration:
				fade = 1.0
			else:
				fade = RangeAdjust(fx_timer, duration - fade_duration, duration, 1.0, 0.0)

		plus.Clear()
		fonts_dict = render_strings_array(strings, fade, fonts_dict, plus=plus)
		if fade > 0.2:
			if render_callback is not None:
				render_callback()
		plus.Flip()
		plus.EndFrame()