import os

#
# This script just looks to see which of the 
# other modules is available, and runs their builds, with the advantage 
# of doing it in the correct order.
#
modules = [f for f in os.listdir(".") if os.path.isdir(f) and os.path.exists("%s/SConstruct"%f) ]
print(modules)

for m in modules:
	SConscript('%s/SConstruct'%m)

#
# We'll also get it to do a basic "install",
# Edit this to say where you want to install to
#
def Install( target, source, env ):
	installRoot = "/opt/mc_bin/"
	for m in modules:
		d = "%s/%s"%(installRoot,m)
		print(d)
		if os.path.exists(d) and not os.path.isdir(d):
			print( "binary install dir '%' exists but is not a directory!" )
			exit(0)
		if not os.path.exists(d):
			os.makedirs(d)
		
		# todo: use shutil or something, not system!
		cmd = "cp -r %s/build/optimised/bin/* %s"%(m, d)
		os.system(cmd)

installCommand = Command('install', [], Install )
Depends( installCommand, BUILD_TARGETS )
if 'install' not in BUILD_TARGETS:
	BUILD_TARGETS.append('install')

