# gcodeTransformer
move, rotate, mirror, scale, combine and round up X and Y of gcode

**Available options**:
```
-f, --file = input file name (required)
-o, --output_file = output file name (if not specified, it will return the code generated)
-x, --move_x = X offset in mm
-y, --move_y = B offset in mm
-r, --rotate = rotate angle (times 90)
-k', --keep_space, to keep empty space around gcode (page size) on rotate if not will gcode will fit to the axe')
-w', --width, page width require if --keep_space used
-h', --height, page height require if --keep_space used
-m, --mirror = axis mirroring (axis name)
-s, --scale = percentage scale, negative is supported
-c, --combine = combine code (example 2x3x10 or 1x2x8 ... where the first number on X is the second number on Y is the third indent)
-rd', --round = round up to '-rd' decimal places X and Y value, can be combined with another operation or used alone
```

based on <a href="https://github.com/tguruslan/gcode_move_and_rotate">this project</a>
