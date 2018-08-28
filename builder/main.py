import sys
import os
import re
from os.path import basename, join, getsize
from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default, DefaultEnvironment)
from platformio import util

env = DefaultEnvironment()

platform = env.PioPlatform()
env["PLATFORM_DIR"] = platform.get_dir()
TOOLCHAIN_DIR = platform.get_package_dir("toolchain-gccarmnoneeabi")
GCC_TOOLCHAIN = join(TOOLCHAIN_DIR, "bin")
env["BOOTALL_BIN"] = ""

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
		"-Wl,-Map=" + join("$BUILD_DIR", "application.map"),
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

	PROGSUFFIX = ".elf"
)

if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

def get_addr(string, file):
#	if not os.path.exists(os.path.dirname(file)):
#		try:
#			os.makedirs(os.path.dirname(file))
#		except OSError as exc:
#			if exc.errno != errno.EEXIST:
#				raise
	res = ""
	with open(file, "a+") as fin:
		for line in fin:
			if re.search(string, line):
				res = line.split(" ")[0]
	return res
	
def replace_rtl(env):
	infile = join(env["PLATFORM_DIR"], "scripts", "openocd", ''.join(env["PIOFRAMEWORK"]), "rtl_gdb_flash_write.txt")
	outfile = join(env.subst(env["BUILD_DIR"]), "rtl_gdb_flash_write.txt")
	if not os.path.exists(os.path.dirname(outfile)):
		try:
			os.makedirs(os.path.dirname(outfile))
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
	with open(infile, "rt") as fin:
		with open(outfile, "wt") as fout:
			for line in fin:
				fout.write(line.replace('BUILD_DIR', '%s' % env.subst(env["BUILD_DIR"])).replace('SCRIPTS_DIR', join(env["PLATFORM_DIR"], "scripts", "openocd", ''.join(env["PIOFRAMEWORK"]))))
								
def get_size(file):
	print file
	size = getsize("C:\\Users\\tautvydas\\.platformio\\packages\\framework-sdk-ameba-v4.0b-gcc\\component\\soc\\realtek\\8711b\\misc\\bsp\\image\\boot_all.bin")
	print size
	print env["BOOTALL_BIN"]
#def decimal_to_hex():
				
manipulating = [
	env.VerboseAction("$NM " + join("$BUILD_DIR", "firmware.elf") + " | sort > " + join("$BUILD_DIR", "firmware.nmap"), "Generating " + join("$BUILD_DIR", "firmware.nmap")),
	env.VerboseAction("$OBJCOPY -j .ram_image2.entry -j .ram_image2.data -j .ram_image2.bss -j .ram_image2.skb.bss -j .ram_heap.data -Obinary " + join("$BUILD_DIR", "firmware.elf") + " " + join("$BUILD_DIR", "ram_2.r.bin"), "Generating " + join("$BUILD_DIR", "ram_2.r.bin")),
	env.VerboseAction("$OBJCOPY -j .xip_image2.text -Obinary " + join("$BUILD_DIR", "firmware.elf") + " " + join("$BUILD_DIR", "xip_image2.bin"), "Generating " + join("$BUILD_DIR", "xip_image2.bin")),
	env.VerboseAction("chmod +rx $PICK $CHKSUM $PAD $OTA", "."),
	env.VerboseAction("$PICK 0x%s 0x%s " % (get_addr("__ram_image2_text_start__", join(env.subst(env["BUILD_DIR"]), "firmware.nmap")), get_addr("__ram_image2_text_end__", join(env.subst(env["BUILD_DIR"]), "firmware.nmap"))) + join("$BUILD_DIR", "ram_2.r.bin") + " " + join("$BUILD_DIR", "ram_2.bin") + " raw", "."),
	env.VerboseAction("$PICK 0x%s 0x%s " % (get_addr("__ram_image2_text_start__", join(env.subst(env["BUILD_DIR"]), "firmware.nmap")), get_addr("__ram_image2_text_end__", join(env.subst(env["BUILD_DIR"]), "firmware.nmap"))) + join("$BUILD_DIR", "ram_2.bin") + " " + join("$BUILD_DIR", "ram_2.p.bin"), "."),
	env.VerboseAction("$PICK 0x%s 0x%s " % (get_addr("__xip_image2_start__", join(env.subst(env["BUILD_DIR"]), "firmware.nmap")), get_addr("__xip_image2_start__", join(env.subst(env["BUILD_DIR"]), "firmware.nmap"))) + join("$BUILD_DIR", "xip_image2.bin") + " " + join("$BUILD_DIR", "xip_image2.p.bin"), "."),	
	env.VerboseAction("cat " + join("$BUILD_DIR", "xip_image2.p.bin") + " > " + join("$BUILD_DIR", "image2_all_ota1.bin"), "Generating $TARGET"),
	env.VerboseAction("cat " + join("$BUILD_DIR", "ram_2.p.bin") + " >> " + join("$BUILD_DIR", "image2_all_ota1.bin"), "."),
	]

uploading = [
	get_size(env["BOOTALL_BIN"]),
	env.VerboseAction('echo -n "set $$" > %s/BTAsize.gdb' % (env["BUILD_DIR"]), 'Uploading binary'),
	env.VerboseAction('echo "BOOTALLFILESize = 0x$$(echo "obase=16; $$(stat -c %%s %s)"|bc)" >> %s/BTAsize.gdb' % (env["BOOTALL_BIN"], env["BUILD_DIR"]), '.'),
	env.VerboseAction('echo -n "set $$" > %s/fwsize.gdb' % (env["BUILD_DIR"]), '.'),
	env.VerboseAction('echo "RamFileSize = 0x$$(echo "obase=16; $$(stat -c %%s $BUILD_DIR/image2_all_ota1.bin)"|bc)" >> %s/fwsize.gdb' % (env["BUILD_DIR"]), '.'),
	replace_rtl(env),
	env.VerboseAction("cp %s " % env["BOOTALL_BIN"] + join("$BUILD_DIR", "boot_all.bin"), '.'),
	env.VerboseAction('openocd -f interface/cmsis-dap.cfg -f %s/scripts/openocd/%s/amebaz.cfg -c "init" > /dev/null 2>&1 &  export ocdpid=$! ; arm-none-eabi-gdb -batch --init-eval-command="dir %s/scripts/openocd/%s" -x %s/rtl_gdb_flash_write.txt ; kill -9 $$ocdpid' % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"]), env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"]), env["BUILD_DIR"]), '.'),
	]

env.Append(
	BUILDERS = dict(
		Manipulate = Builder(
			action = env.VerboseAction(manipulating, "Manipulating images")),
		)
)

lala_b = env.VerboseAction("ls", "Testing")
AlwaysBuild(lala_b)
program_b = env.BuildProgram()
manipulate_images_b = env.Manipulate("$BUILD_DIR/image2_all_ota1.bin", [program_b])
upload = env.Alias("upload", manipulate_images_b, uploading)
AlwaysBuild(upload)

Default(lala_b)
#Default([manipulate_images_b])

