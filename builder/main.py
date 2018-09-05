import sys
import os
import re
from os.path import basename, join, getsize
from SCons.Action import FunctionAction
from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default, DefaultEnvironment)
from platformio import util

env = DefaultEnvironment()
platform = env.PioPlatform()
OPENOCD_DIR = platform.get_package_dir("tool-openocd")
GCC_TOOLCHAIN = join(platform.get_package_dir("toolchain-gccarmnoneeabi"), "bin")

if os.name == "nt":
	EXECUTABLE_SUFFIX = r".exe"
	PATH_SEPARATOR = r"\\"
	COPY = "copy"
	env["OPENOCDCMD"] = "START /B $OPENOCD -s %s\\scripts -f interface\\cmsis-dap.cfg -f %s -c \"init\"" % (OPENOCD_DIR , join("$PLATFORM_DIR", "scripts", "openocd", ''.join(env["PIOFRAMEWORK"]), "amebaz.cfg"))
	env["GDBCMD"] = "$GDB -q -batch --init-eval-command=\"dir %s\"" % join("$PLATFORM_DIR", "scripts", "openocd", ''.join(env["PIOFRAMEWORK"])) + " -x $BUILD_DIR\\rtl_gdb_flash_write.txt"
	env["UPLOADCMD"] ="$OPENOCDCMD & $GDBCMD"
	env["OPENOCD_KILL"] = " & (for /f \"TOKENS=1,2,*\" %a in ('tasklist /fi \"IMAGENAME eq openocd.exe\"') do (Taskkill /f /pid %b)) > nul 2>&1"
else:
	EXECUTABLE_SUFFIX = ""
	PATH_SEPARATOR = "/"
	COPY = "cp"
	env["OPENOCDCMD"] = "$OPENOCD -s %s/scripts -f interface/cmsis-dap.cfg -f $PLATFORM_DIR/scripts/openocd/%s/amebaz.cfg -c \"init\" > /dev/null 2>&1 & export ocdpid=$!" % (OPENOCD_DIR, ''.join(env["PIOFRAMEWORK"]))
	env["GDBCMD"] = "$GDB -batch --init-eval-command=\"dir $PLATFORM_DIR/scripts/openocd/%s\" -x $BUILD_DIR/rtl_gdb_flash_write.txt" % ''.join(env["PIOFRAMEWORK"])
	env["UPLOADCMD"] ="$OPENOCDCMD ; $GDBCMD"
	env["OPENOCD_KILL"] = " ; kill -9 $$ocdpid"

env.Replace(
	AR = join(GCC_TOOLCHAIN, "arm-none-eabi-ar" + EXECUTABLE_SUFFIX),
	CC = join(GCC_TOOLCHAIN, "arm-none-eabi-gcc" + EXECUTABLE_SUFFIX),
	CXX = join(GCC_TOOLCHAIN, "arm-none-eabi-g++" + EXECUTABLE_SUFFIX),
	AS = join(GCC_TOOLCHAIN, "arm-none-eabi-as" + EXECUTABLE_SUFFIX),
	NM = join(GCC_TOOLCHAIN, "arm-none-eabi-nm" + EXECUTABLE_SUFFIX),
	LINK = join(GCC_TOOLCHAIN, "arm-none-eabi-gcc" + EXECUTABLE_SUFFIX),
	LD = join(GCC_TOOLCHAIN, "arm-none-eabi-gcc" + EXECUTABLE_SUFFIX),
	GDB = join(GCC_TOOLCHAIN, "arm-none-eabi-gdb" + EXECUTABLE_SUFFIX),
	OBJCOPY = join(GCC_TOOLCHAIN, "arm-none-eabi-objcopy" + EXECUTABLE_SUFFIX),
	OBJDUMP = join(GCC_TOOLCHAIN, "arm-none-eabi-objdump" + EXECUTABLE_SUFFIX),
	SIZETOOL = join(GCC_TOOLCHAIN, "arm-none-eabi-size" + EXECUTABLE_SUFFIX),
	OPENOCD = join(OPENOCD_DIR, "bin", "openocd" + EXECUTABLE_SUFFIX),

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
		"-Wl,-Map=" + join(env.subst("$BUILD_DIR"), "application.map"),
		"-Os",
		"-Wl,--gc-sections",
		"-Wl,--cref",
		"-Wl,--entry=gImage2EntryFun0",
		"-Wl,--no-enum-size-warning",
		"-Wl,--no-wchar-size-warning",
		"-Wl,-wrap,malloc",
		"-Wl,-wrap,free",
		"-Wl,-wrap,realloc",
	],

	CP = COPY,
	
	SIZEPROGREGEXP = r"^(?:\.ram_image2\.entry|\.ram_image2\.text|\.ram_image2\.data|\.ram_heap\.data|\.xip_image2\.text|)\s+([0-9]+).*",
	SIZEDATAREGEXP = r"^(?:\.ram_image2\.entry|\.ram_image2\.data|\.ram_heap\.data|\.ram_image2\.bss|\.ram_image2\.skb\.bss|)\s+([0-9]+).*",
	SIZECHECKCMD = '$SIZETOOL -A -d $SOURCES',
	SIZEPRINTCMD = '$SIZETOOL -B -d $SOURCES',
	
	PROGSUFFIX = ".elf",
	
	PLATFORM_DIR = platform.get_dir(),
)

if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")
	
def pick(target, source, env):
	section = [
		"__ram_image2_text_start__",
		"__ram_image2_text_end__",
		"__xip_image2_start__",
			]
	addr = [None] * 3
	with open(join(env.subst("$BUILD_DIR"), "firmware.nmap"), "rt") as fin:
		for line in fin:
			for num, string in enumerate(section):
				if re.search(string, line):
					addr[num] = line.split(" ")[0]

	build_dir = env.subst("$BUILD_DIR")
	pick = [
		"$PICK 0x%s 0x%s %s %s raw" % (addr[0], addr[1], join(build_dir, "ram_2.r.bin"), join(build_dir, "ram_2.bin")),
		"$PICK 0x%s 0x%s %s %s" % (addr[0], addr[1], join(build_dir, "ram_2.bin"), join(build_dir, "ram_2.p.bin")),
		"$PICK 0x%s 0x%s %s %s" % (addr[2], addr[2], join(build_dir, "xip_image2.bin"), join(build_dir, "xip_image2.p.bin"))
	]
	for p in pick:
		status = env.Execute(p)
		if status:
			return status

def replace_rtl(**kw):
	infile = join(env.subst("$PLATFORM_DIR"), "scripts", "openocd", ''.join(env["PIOFRAMEWORK"]), "rtl_gdb_flash_write.txt")
	outfile = join(env.subst("$BUILD_DIR/"), "rtl_gdb_flash_write.txt")
	with open(infile, "rt") as fin:
		with open(outfile, "wt") as fout:
			for line in fin:
				fout.write(line.replace('BUILD_DIR/', env.subst("$BUILD_DIR").replace("\\", "\\\\") + PATH_SEPARATOR).replace('SCRIPTS_DIR/', join(env.subst("$PLATFORM_DIR"), "scripts", "openocd", ''.join(env["PIOFRAMEWORK"])).replace("\\", "\\\\") + PATH_SEPARATOR))

def BTAsize_create(**kw):
	bin_size = getsize(env["BOOTALL_BIN"])
	with open(join(env.subst(env["BUILD_DIR"]), "BTAsize.gdb"), "wt") as fout:
		fout.write("set $BOOTALLFILESize = 0x%X" % bin_size)
		
def fwsize_create(**kw):
	bin_size = getsize(join(env.subst(env["BUILD_DIR"]), "image2_all_ota1.bin"))
	with open(join(env.subst(env["BUILD_DIR"]), "fwsize.gdb"), "wt") as fout:
		fout.write("set $RamFileSize = 0x%X" % bin_size)

def cat(target, source, env):
	xip = open(join(env.subst("$BUILD_DIR"), "xip_image2.p.bin"), "rb")
	ram = open(join(env.subst("$BUILD_DIR"), "ram_2.p.bin"), "rb")
	target = open(join(env.subst("$BUILD_DIR"), "image2_all_ota1.bin"), "wb")
	target.write(xip.read())
	target.write(ram.read())

manipulating = [
	env.VerboseAction("$NM " + join(env.subst("$BUILD_DIR"), "firmware.elf") + " | sort > " + join(env.subst("$BUILD_DIR"), "firmware.nmap"), "Generating " + join(env.subst("$BUILD_DIR"), "firmware.nmap")),
	env.VerboseAction("$OBJCOPY -j .ram_image2.entry -j .ram_image2.data -j .ram_image2.bss -j .ram_image2.skb.bss -j .ram_heap.data -Obinary " + join(env.subst("$BUILD_DIR"), "firmware.elf") + " " + join(env.subst("$BUILD_DIR"), "ram_2.r.bin"), "Generating " + join(env.subst("$BUILD_DIR"), "ram_2.r.bin")),
	env.VerboseAction("$OBJCOPY -j .xip_image2.text -Obinary " + join(env.subst("$BUILD_DIR"), "firmware.elf") + " " + join(env.subst("$BUILD_DIR"), "xip_image2.bin"), "Generating " + join(env.subst("$BUILD_DIR"), "xip_image2.bin")),
	env.VerboseAction(pick, "Calculating section addresses"),
	env.VerboseAction(cat, "Generating $TARGET"),
	]

uploading = [
	env.VerboseAction(BTAsize_create, "Generating " + join(env.subst("$BUILD_DIR"), "BTAsize.gdb")),
	env.VerboseAction(fwsize_create, "Generating " + join(env.subst("$BUILD_DIR"), "fwsize.gdb")),
	env.VerboseAction(replace_rtl, "Generating " + join(env.subst("$BUILD_DIR"), "rtl_gdb_flash_write.txt")),
	env.VerboseAction("$CP $BOOTALL_BIN " + join(env.subst("$BUILD_DIR"), "boot_all.bin"), '.'),
	env.VerboseAction(env.subst("$UPLOADCMD").replace("\\", "\\\\") + env["OPENOCD_KILL"], "Uploading binary to flash"),
	]

env.Append(
	BUILDERS = dict(
		Manipulate = Builder(
			action = env.VerboseAction(manipulating, "Manipulating images")),
		)
)

program_b = env.BuildProgram()
manipulate_images_b = env.Manipulate("$BUILD_DIR/image2_all_ota1.bin", [program_b])
upload = env.Alias("upload", manipulate_images_b, uploading)
AlwaysBuild(upload)

Default([manipulate_images_b])
