# Simple build system based on Python

Similar to [meson](https://mesonbuild.com), but with actual Python integration. This project is by no means close to where meson currently is, so it's definitely not a replacement, especially not in production environments.

Just a hobby project of mine.

# Check out the sample

See [`samples/simple_main/pymake.yml`](samples/simple_main/pymake.yml).

Requires: The `g++` or `clang++` compiler and everything else it needs, since [`samples/simple_main/main.cpp`](samples/simple_main/main.cpp) is C++ code. If you have both compilers installed, `pymake` will currently attempt to build with both of them separately.

# make.py

The file [`make.py`](samples/simple_main/make.py) is where you can hook into certain events that `pymake` fires:

| Event # | Event hook | Event description |
|---|---|---|
| 1 | `PreConfigureProject` | after metadata is parsed, before target data is parsed |
| 2 | `PreConfigureTarget` | before target data is parsed |
| 3 | `PostConfigureTarget` | after target data is parsed |
| 4 | `PostConfigureProject` | after all data of all targets has been parsed |
| 5 | `PreBuildProject` | ready to build targets |
| 6 | `PreBuildTarget` | before a target is built |
| 7 | `PostBuildTarget` | after a target is built |
| 8 | `PostBuildProject` | after all targets have been built |

# What's missing?
A lot!

- Target dependency management
- Build output types other than `executable`
- Linker configuration
- ...

# Build the sample

```
git clone https://github.com/thetredev/pymake.git
cd pymake/samples/simple_main
python3 ../../pymake.py
```

Example output:
```
PreConfigureProject: . build

PreConfigureTarget: SimpleMain

[WARN] Could not find toolchain executable: clang++. Skipping this one...
PostConfigureTarget: <SimpleMain: [build/simple_main] as [executable]>

PostConfigureProject: <Simple Main> First PyMake sample
 in: ../pymake/samples/simple_main/build

PreBuildProject: <Simple Main> First PyMake sample
 in: ../pymake/samples/simple_main/build

PreBuildTarget: <SimpleMain: [build/simple_main] as [executable]>
 /usr/bin/g++ -D PYMAKE_SAMPLE -D SOME_NEW_MACRO -D SOME_INT=3 -D SOME_INT_AS_STR=\"5\" -D PYMAKE_TOOLCHAIN=\"g++\" -std=c++11 main.cpp -o build/g++/simple_main

PostBuildTarget: <SimpleMain: [build/simple_main] as [executable]>
 /usr/bin/g++ -D PYMAKE_SAMPLE -D SOME_NEW_MACRO -D SOME_INT=3 -D SOME_INT_AS_STR=\"5\" -D PYMAKE_TOOLCHAIN=\"g++\" -std=c++11 main.cpp -o build/g++/simple_main

PostBuildProject: <Simple Main> First PyMake sample
 in: ../pymake/samples/simple_main/build
```
