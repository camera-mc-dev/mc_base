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

