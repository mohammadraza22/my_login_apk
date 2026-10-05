[app]
title = My Login App
package.name = myloginapp
package.domain = org.myapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0.0
requirements = python3,kivy
orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
