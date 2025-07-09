[app]

title = Snake Game
package.name = snakegame
package.domain = org.example
source.dir = .
source.include_exts = py,png
source.include_patterns = *.png
version = 1.0
requirements = python3, pygame
orientation = landscape

# Ensure compatible build tools & SDK
android.build_tools_version = 33.0.2
android.sdk = 33
android.ndk = 23b
android.arch = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 0
