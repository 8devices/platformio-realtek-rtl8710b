import sys
import os
import re
from os.path import basename, join, getsize
from SCons.Action import FunctionAction
from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default, DefaultEnvironment)
from platformio import util

env = DefaultEnvironment()

platform = env.PioPlatform()
#env["PLATFORM_DIR"] = platform.get_dir()
TOOLCHAIN_DIR = platform.get_package_dir("toolchain-gccarmnoneeabi")
GCC_TOOLCHAIN = join(TOOLCHAIN_DIR, "bin")

env.Replace(
	#SHELL = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",

	AR = join(GCC_TOOLCHAIN, "arm-none-eabi-ar.exe"),
	CC = join(GCC_TOOLCHAIN, "arm-none-eabi-gcc.exe"),
	CXX = join(GCC_TOOLCHAIN, "arm-none-eabi-g++.exe"),
	AS = join(GCC_TOOLCHAIN, "arm-none-eabi-as.exe"),
	NM = join(GCC_TOOLCHAIN, "arm-none-eabi-nm.exe"),
	LINK = join(GCC_TOOLCHAIN, "arm-none-eabi-gcc.exe"),
	LD = join(GCC_TOOLCHAIN, "arm-none-eabi-gcc.exe"),
	GDB = join(GCC_TOOLCHAIN, "arm-none-eabi-gdb.exe"),
	OBJCOPY = join(GCC_TOOLCHAIN, "arm-none-eabi-objcopy.exe"),
	OBJDUMP = join(GCC_TOOLCHAIN, "arm-none-eabi-objdump.exe"),
	SIZETOOL = join(GCC_TOOLCHAIN, "arm-none-eabi-size.exe"),

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
		"-Wl,--entry=Reset_Handler",
		"-Wl,--no-enum-size-warning",
		"-Wl,--no-wchar-size-warning",
		"-Wl,-wrap,malloc",
		"-Wl,-wrap,free",
		"-Wl,-wrap,realloc",
	],

	SIZEPROGREGEXP=r"^(?:\.ram_image2\.entry|\.ram_image2\.text|\.ram_image2\.data|\.ram_heap\.data|\.xip_image2\.text|)\s+([0-9]+).*",
	SIZEDATAREGEXP=r"^(?:\.ram_image2\.entry|\.ram_image2\.data|\.ram_heap\.data|\.ram_image2\.bss|\.ram_image2\.skb\.bss|)\s+([0-9]+).*",
	SIZECHECKCMD='$SIZETOOL -A -d $SOURCES',
	SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

	PROGSUFFIX = ".elf",
	
	PLATFORM_DIR = platform.get_dir(),
)

if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

def get_addr(source, target, env):
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
	env.Replace(
		__RAM_IMAGE2_TEXT_START__ = addr[0],
		__RAM_IMAGE2_TEXT_END__	  = addr[1],
		__XIP_IMAGE2_START__	  = addr[2],
	)
	
def replace_rtl(**kw):
	infile = join(env.subst("$PLATFORM_DIR"), "scripts", "openocd", ''.join(env["PIOFRAMEWORK"]), "rtl_gdb_flash_write.txt")
	outfile = join(env.subst("$BUILD_DIR"), "rtl_gdb_flash_write.txt")
	with open(infile, "rt") as fin:
		with open(outfile, "wt") as fout:
			for line in fin:
				fout.write(line.replace('BUILD_DIR', env.subst("$BUILD_DIR")).replace('SCRIPTS_DIR', join("$PLATFORM_DIR", "scripts", "openocd", ''.join(env["PIOFRAMEWORK"]))))

def BTAsize_create(**kw):
	bin_size = getsize(env["BOOTALL_BIN"])
	with open(join(env.subst(env["BUILD_DIR"]), "BTAsize.gdb"), "wt") as fout:
		fout.write("set $BOOTALLFILESize = 0x%X" % bin_size)
		
def fwsize_create(**kw):
	bin_size = getsize(join(env.subst(env["BUILD_DIR"]), "image2_all_ota1.bin"))
	with open(join(env.subst(env["BUILD_DIR"]), "fwsize.gdb"), "wt") as fout:
		fout.write("set $RamFileSize = 0x%X" % bin_size)

manipulating = [
	env.VerboseAction("$NM " + join(env.subst("$BUILD_DIR"), "firmware.elf") + " | sort > " + join(env.subst("$BUILD_DIR"), "firmware.nmap"), "Generating " + join(env.subst("$BUILD_DIR"), "firmware.nmap")),
	env.VerboseAction("$OBJCOPY -j .ram_image2.entry -j .ram_image2.data -j .ram_image2.bss -j .ram_image2.skb.bss -j .ram_heap.data -Obinary " + join(env.subst("$BUILD_DIR"), "firmware.elf") + " " + join(env.subst("$BUILD_DIR"), "ram_2.r.bin"), "Generating " + join(env.subst("$BUILD_DIR"), "ram_2.r.bin")),
	env.VerboseAction("$OBJCOPY -j .xip_image2.text -Obinary " + join(env.subst("$BUILD_DIR"), "firmware.elf") + " " + join(env.subst("$BUILD_DIR"), "xip_image2.bin"), "Generating " + join(env.subst("$BUILD_DIR"), "xip_image2.bin")),
	env.VerboseAction("chmod +rx $PICK $CHKSUM $PAD $OTA", "."),
	env.VerboseAction(get_addr, "Calculating section addresses"),
	#FunctionAction(get_addr, {}),
	env.VerboseAction("$PICK 0x$__RAM_IMAGE2_TEXT_START__ 0x$__RAM_IMAGE2_TEXT_END__ " + join(env.subst("$BUILD_DIR"), "ram_2.r.bin") + " " + join(env.subst("$BUILD_DIR"), "ram_2.bin") + " raw", "."),
	env.VerboseAction("$PICK 0x$__RAM_IMAGE2_TEXT_START__ 0x$__RAM_IMAGE2_TEXT_END__ " + join(env.subst("$BUILD_DIR"), "ram_2.bin") + " " + join(env.subst("$BUILD_DIR"), "ram_2.p.bin"), "."),
	env.VerboseAction("$PICK 0x$__XIP_IMAGE2_START__ 0x$__XIP_IMAGE2_START__ " + join(env.subst("$BUILD_DIR"), "xip_image2.bin") + " " + join(env.subst("$BUILD_DIR"), "xip_image2.p.bin"), "."),	
	env.VerboseAction("cat " + join(env.subst("$BUILD_DIR"), "xip_image2.p.bin") + " > " + join(env.subst("$BUILD_DIR"), "image2_all_ota1.bin"), "Generating $TARGET"),
	env.VerboseAction("cat " + join(env.subst("$BUILD_DIR"), "ram_2.p.bin") + " >> " + join(env.subst("$BUILD_DIR"), "image2_all_ota1.bin"), "."),
	]

uploading = [
	FunctionAction(BTAsize_create, {}),
	FunctionAction(fwsize_create, {}),
	FunctionAction(replace_rtl, {}),
	env.VerboseAction("cp $BOOTALL_BIN " + join(env.subst("$BUILD_DIR"), "boot_all.bin"), '.'),
#	env.VerboseAction('openocd -f interface/cmsis-dap.cfg -f %s/scripts/openocd/%s/amebaz.cfg -c "init" > /dev/null 2>&1 &  export ocdpid=$! ; arm-none-eabi-gdb -batch --init-eval-command="dir %s/scripts/openocd/%s" -x %s/rtl_gdb_flash_write.txt ; kill -9 $$ocdpid' % ("$PLATFORM_DIR", ''.join(env["PIOFRAMEWORK"]), "$PLATFORM_DIR", ''.join(env["PIOFRAMEWORK"]), env["BUILD_DIR"]), '.'),
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

