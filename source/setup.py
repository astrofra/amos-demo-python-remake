import sys
from cx_Freeze import setup, Executable


# Gather extra runtime dependencies.
def gather_extra_redist():
	import os
	import harfang
	import inspect

	path = os.path.dirname(inspect.getfile(harfang))
	files = os.listdir(path)

	out = []
	for file in files:
		name, ext = os.path.splitext(file)
		if ext in ['.dll', '.so'] and "Debug" not in name:
			out.append(os.path.join(path, file))

	return out


extra_redist = gather_extra_redist()

# Dependencies are automatically detected, but it might need fine tuning.
options = {
	'build_exe': {
		# 'compressed': True,
		'packages': ['harfang'],
		'include_files': ['file_id.diz', 'screenshot.png', 'openal32.dll', 'assets/'] + extra_redist # 'ad_coupon_AF_issue_06.jpg', 
	}
}

setup(  name = "AMOS Demo",
		version = "1.0",
		description = "PC version of the original AMOS demo released in 1989 by Mandarin Software.",
		options = options,
		executables = [Executable("main.py", targetName="AMOS-Demo.exe", icon="icon.ico")])
