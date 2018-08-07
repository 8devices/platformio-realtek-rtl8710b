import sys
from os.path import basename, join
from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default, DefaultEnvironment)
from platformio import util

env = DefaultEnvironment()

try:
	env["SRC_FILTER"]
except KeyError:
	env["SRC_FILTER"] = [
		"+<*>",
		"-<.git/>",
		"-<svn/>",
		"-<example/>",
		"-<examples/>",
		"-<test/>",
		"-<tests/>"]

#env["CPPDEFINES"] = []
GCC_TOOLCHAIN = ""

env.Replace(

	AR = GCC_TOOLCHAIN + "arm-none-eabi-ar",
	CC = GCC_TOOLCHAIN + "arm-none-eabi-gcc",
	CXX = GCC_TOOLCHAIN + "arm-none-eabi-g++",
	AS = GCC_TOOLCHAIN + "arm-none-eabi-as",
	NM = GCC_TOOLCHAIN + "arm-none-eabi-nm",
	LD = GCC_TOOLCHAIN + "arm-none-eabi-gcc",
	GDB = GCC_TOOLCHAIN + "arm-none-eabi-gdb",
	OBJCOPY = GCC_TOOLCHAIN + "arm-none-eabi-objcopy",
	OBJDUMP = GCC_TOOLCHAIN + "arm-none-eabi-objdump",

#	BOARD_CONFIG?
	CCFLAGS = [
		"-mcpu=cortex-m4",
		"-mthumb",
		"-mfloat-abi=hard",
		"-mfpu=fpv4-sp-d16",
		"-g2",
		"-w",
		"-fno-common",
		"-fmessage-length=0",
		"-ffunction-sections",
		"-fdata-sections",
		"-fomit-frame-pointer",
		"-fno-short-enums",

#	MANO
#	//MANO
	],
	CFLAGS = [
#	MANO
		"-std=gnu99",
#	//MANO
		"-fsigned-char",
		"-Wno-pointer-sign",
	],
	CXXFLAGS = [
#	MANO
		"-fno-exceptions",
		"-std=c++11",
		"-fno-rtti",
#	//MANO
	],
	CPPDEFINES = [
		"M3",
		"CONFIG_PLATFORM_8711B",
		"F_CPU=166000000L",
	],
#	//BOARD_CONFIG?

	LINKFLAGS = [
		"-mcpu=cortex-m4",
		"-mthumb",
		"-mfloat-abi=hard",
		"-mfpu=fpv4-sp-d16",
		"-g",
		"--specs=nano.specs",
		"-nostartfiles",
		"-Wl,-Map=" + "$BUILD_DIR" + "/application.map",
		"-Os",
		"-Wl,--gc-sections",
		"-Wl,--cref",
		"-Wl,--entry=Reset_Handler",
		"-Wl,--no-enum-size-warning",
		"-Wl,--no-wchar-size-warning",
		"-Wl,-wrap,malloc",
		"-Wl,-wrap,free",
		"-Wl,-wrap,realloc",
	]
)

def prefix_cppdefines(env):
	prefix = "-D"
	env["CPPDEFINES"] = [prefix + s for s in env["CPPDEFINES"]]
	return env["CPPDEFINES"]

def prefix_includes(env):
	prefix = "-I"
	env["CPPPATH"] = [prefix + s for s in env["CPPPATH"]]
	return env["CPPPATH"]

def prefix_libs(env):
	prefix = "-l"
	env["LIBS"] = [prefix + s for s in env["LIBS"]]
	return env["LIBS"]

def prefix_libpaths(env):
	prefix = "-L"
	env["LIBPATH"] = [prefix + s for s in env["LIBPATH"]]
	return env["LIBPATH"]

def replace_rtl(env):
	with open("%s/scripts/openocd/%s/_rtl_gdb_flash_write.txt" % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"])), "rt") as fin:
		with open("%s/scripts/openocd/%s/rtl_gdb_flash_write.txt" % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"])), "wt") as fout:
			for line in fin:
				fout.write(line.replace('BUILD_DIR', '%s' % env.subst(env["BUILD_DIR"])).replace('SCRIPTS_DIR', '%s/scripts/openocd/%s' % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"]))))

def replace_ld(env):
	with open("%s/scripts/ld/%s/_rlx8711B-symbol-v02-img2_xip1.ld" % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"])), "rt") as fin:
		with open("%s/scripts/ld/%s/rlx8711B-symbol-v02-img2_xip1.ld" % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"])), "wt") as fout:
			for line in fin:
				fout.write(line.replace('PLATFORMDIR', '%s' % env.subst(env["PLATFORM_DIR"])).replace('FRAMEWORK', '%s' % ''.join(env["PIOFRAMEWORK"])))

def board_flags(env):
	if "BOARD" in env and "build.extra_flags" in env.BoardConfig():
		env.ProcessFlags(env.BoardConfig().get("build.extra_flags"))

prerequirement = [
	env.ProcessFlags(env.get("BUILD_FLAGS")),
	board_flags(env),
	env.BuildFrameworks(env.get("PIOFRAMEWORK")),
	replace_ld(env),
	env.ProcessUnFlags(env.get("BUILD_UNFLAGS")),
	#prefix_cppdefines(env),
	#prefix_includes(env),
	env.VerboseAction("chmod 777 %s" % env["BOOTALL_BIN"], "Executing prerequirements"),
	env.VerboseAction("$OBJCOPY -I binary -O elf32-littlearm -B arm %s $BUILD_DIR/boot_all.o" % env["BOOTALL_BIN"], "Generating $TARGET"),
		]

manipulating = [
	env.VerboseAction("$NM $BUILD_DIR/program.axf | sort > $BUILD_DIR/program.nmap", "Generating $BUILD_DIR/program.nmap"),
	env.VerboseAction("$OBJCOPY -j .ram_image2.entry -j .ram_image2.data -j .ram_image2.bss -j .ram_image2.skb.bss -j .ram_heap.data -Obinary $BUILD_DIR/program.axf $BUILD_DIR/ram_2.r.bin", "Generating $BUILD_DIR/ram_2.r.bin"),
	env.VerboseAction("$OBJCOPY -j .xip_image2.text -Obinary $BUILD_DIR/program.axf $BUILD_DIR/xip_image2.bin", "Generating $BUILD_DIR/xip_image2.bin"),
	env.VerboseAction("chmod +rx $PICK $CHKSUM $PAD $OTA", "."),
	env.VerboseAction("$PICK 0x`grep __ram_image2_text_start__ $BUILD_DIR/program.nmap | gawk '{print $$1}'` 0x`grep __ram_image2_text_end__ $BUILD_DIR/program.nmap | gawk '{print $$1}'` $BUILD_DIR/ram_2.r.bin $BUILD_DIR/ram_2.bin raw", "."),
	env.VerboseAction("$PICK 0x`grep __ram_image2_text_start__ $BUILD_DIR/program.nmap | gawk '{print $$1}'` 0x`grep __ram_image2_text_end__ $BUILD_DIR/program.nmap | gawk '{print $$1}'` $BUILD_DIR/ram_2.bin $BUILD_DIR/ram_2.p.bin", "."),
	env.VerboseAction("$PICK 0x`grep __xip_image2_start__ $BUILD_DIR/program.nmap | gawk '{print $$1}'` 0x`grep __xip_image2_start__ $BUILD_DIR/program.nmap | gawk '{print $$1}'` $BUILD_DIR/xip_image2.bin $BUILD_DIR/xip_image2.p.bin", "."),
	env.VerboseAction("cat $BUILD_DIR/xip_image2.p.bin > $BUILD_DIR/image2_all_ota1.bin", "Generating $TARGET"),
	env.VerboseAction("cat $BUILD_DIR/ram_2.p.bin >> $BUILD_DIR/image2_all_ota1.bin", "."),
	]

uploading = [
	env.VerboseAction('echo -n "set $$" > %s/scripts/openocd/%s/BTAsize.gdb' % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"])), 'Uploading binary'),
	env.VerboseAction('echo "BOOTALLFILESize = 0x$$(echo "obase=16; $$(stat -c %%s %s)"|bc)" >> %s/scripts/openocd/%s/BTAsize.gdb' % (env["BOOTALL_BIN"], env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"])), '.'),
	env.VerboseAction('echo -n "set $$" > %s/scripts/openocd/%s/fwsize.gdb' % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"])), '.'),
	env.VerboseAction('echo "RamFileSize = 0x$$(echo "obase=16; $$(stat -c %%s $BUILD_DIR/image2_all_ota1.bin)"|bc)" >> %s/scripts/openocd/%s/fwsize.gdb' % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"])), '.'),
	replace_rtl(env),
	env.VerboseAction('cp %s $BUILD_DIR/boot_all.bin' % env["BOOTALL_BIN"], '.'),
	env.VerboseAction('openocd -f interface/cmsis-dap.cfg -f %s/scripts/openocd/%s/amebaz.cfg -c "init" > /dev/null 2>&1 &  export ocdpid=$! ; arm-none-eabi-gdb -batch --init-eval-command="dir %s/scripts/openocd/%s" -x %s/scripts/openocd/%s/rtl_gdb_flash_write.txt ; kill -9 $$ocdpid' % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"]), env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"]), env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"])), '.'),
	]

env.Append(
	BUILDERS = dict(
		Prerequirement = Builder(
			action = env.VerboseAction(prerequirement, "Executing prerequirements")),
		Linker = Builder(
			action = env.VerboseAction("$LD $LINKFLAGS -o $TARGET $SOURCES %s %s -T$LDSCRIPT_PATH" % (' '.join(prefix_libpaths(env)), ' '.join(prefix_libs(env))), "Linking $TARGET")),
#		Compiler = Builder(
#			action = env.VerboseAction("$CC %s $CCFLAGS %s -c $SOURCES -o $TARGET" % (' '.join(prefix_cppdefines(env)), ' '.join(prefix_includes(env))), "Compiling $TARGET"),
#			suffix = ".o",
#			single_source = 1),
		Manipulate = Builder(
			action = env.VerboseAction(manipulating, "Manipulating images")),
		)
)
prerequirement_b = env.Prerequirement(("$BUILD_DIR/boot_all.o"), (env["BOOTALL_BIN"]))
compiler_b = env.Object(env["SOURCE_LIST"])
#compiler_b = env.Compiler(env["SOURCE_LIST"])
linker_b = env.Linker("$BUILD_DIR/program.axf", [prerequirement_b, compiler_b])
manipulate_images_b = env.Manipulate("$BUILD_DIR/image2_all_ota1.bin", linker_b)
#env.AddPreAction(prerequirement_b, "ls")

upload = env.Alias("upload", [manipulate_images_b, env["BOOTALL_BIN"]], uploading)

AlwaysBuild(upload)

Default([manipulate_images_b])

