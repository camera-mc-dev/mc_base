import os

#
# This script just looks to see which of the 
# other modules is available, and runs their builds, with the advantage 
# of doing it in the correct order.
#
modules = [f for f in os.listdir(".") if os.path.isdir(f) and os.path.exists("%s/SConstruct"%f) ]
print(modules)

for m in modules:
	os.chdir(m)
	print( "\033[96m" ) # cyan
	print( "----------------------------" )
	print( "            %s"%m )
	print( "----------------------------" )
	print( "\033[0m" )  # normal
	os.system('git status')
	os.chdir("..")
	print("\n\n\n")

