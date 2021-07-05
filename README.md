# gcodeTransformer
move, rotate, mirror, scale, combine and round up X and Y of gcode

**Available options**:
```
-f, --file = input file name (required)
-t, --save_to = filename in to save (if not specified, it will be the same as the original but with the prefix _new)
-x, --move_x = X offset in mm
-y, --move_y = B offset in mm
-r, --rotate = rotate angle (times 90)
-m, --mirror = axis mirroring (axis name)
-s, --scale = percentage scale, negative is supported
-c, --combine = combine code (example 2x3x10 or 1x2x8 ... where the first number on X is the second number on Y is the third indent)
-rd', --round = round up to '-rd' decimal places X and Y value, can be combined with another operation or used alone
```

based on <a href="https://github.com/tguruslan/gcode_move_and_rotate">this project</a>
