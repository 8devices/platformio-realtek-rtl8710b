import sys
import os
from os.path import basename, join
from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default, DefaultEnvironment)
from platformio import util

env = DefaultEnvironment()

platform = env.PioPlatform()
env["PLATFORM_DIR"] = platform.get_dir()
TOOLCHAIN_DIR = platform.get_package_dir("toolchain-realtek")
GCC_TOOLCHAIN = TOOLCHAIN_DIR + "/arm-none-eabi-gcc/4_8-2014q3/bin/"
env["BOOTALL_BIN"] = ""

env.Replace(

	AR = GCC_TOOLCHAIN + "arm-none-eabi-ar",
	CC = GCC_TOOLCHAIN + "arm-none-eabi-gcc",
	CXX = GCC_TOOLCHAIN + "arm-none-eabi-g++",
	AS = GCC_TOOLCHAIN + "arm-none-eabi-as",
	NM = GCC_TOOLCHAIN + "arm-none-eabi-nm",
	LINK = GCC_TOOLCHAIN + "arm-none-eabi-gcc",
	LD = GCC_TOOLCHAIN + "arm-none-eabi-gcc",
	GDB = GCC_TOOLCHAIN + "arm-none-eabi-gdb",
	OBJCOPY = GCC_TOOLCHAIN + "arm-none-eabi-objcopy",
	OBJDUMP = GCC_TOOLCHAIN + "arm-none-eabi-objdump",
	SIZETOOL = GCC_TOOLCHAIN + "arm-none-eabi-size",

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
	],

	SIZEPROGREGEXP=r"^(?:\.ram_image2\.entry|\.ram_image2\.text|\.ram_image2\.data|\.ram_heap\.data|\.xip_image2\.text|)\s+([0-9]+).*",
	SIZEDATAREGEXP=r"^(?:\.ram_image2\.entry|\.ram_image2\.data|\.ram_heap\.data|\.ram_image2\.bss|\.ram_image2\.skb\.bss|)\s+([0-9]+).*",
	SIZECHECKCMD='$SIZETOOL -A -d $SOURCES',
	SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

	PROGSUFFIX = ".elf"
)

if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

def replace_rtl(env):
	infile = "%s/scripts/openocd/%s/rtl_gdb_flash_write.txt" % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"]))
	outfile = "%s/rtl_gdb_flash_write.txt" % (env.subst(env["BUILD_DIR"]))
	if not os.path.exists(os.path.dirname(outfile)):
		try:
			os.makedirs(os.path.dirname(outfile))
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
        with open(infile, "rt") as fin:
                with open(outfile, "wt") as fout:
                        for line in fin:
                                fout.write(line.replace('BUILD_DIR', '%s' % env.subst(env["BUILD_DIR"])).replace('SCRIPTS_DIR', '%s/scripts/openocd/%s' % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"]))))

manipulating = [
	env.VerboseAction("$NM $BUILD_DIR/firmware.elf | sort > $BUILD_DIR/firmware.nmap", "Generating $BUILD_DIR/firmware.nmap"),
	env.VerboseAction("$OBJCOPY -j .ram_image2.entry -j .ram_image2.data -j .ram_image2.bss -j .ram_image2.skb.bss -j .ram_heap.data -Obinary $BUILD_DIR/firmware.elf $BUILD_DIR/ram_2.r.bin", "Generating $BUILD_DIR/ram_2.r.bin"),
	env.VerboseAction("$OBJCOPY -j .xip_image2.text -Obinary $BUILD_DIR/firmware.elf $BUILD_DIR/xip_image2.bin", "Generating $BUILD_DIR/xip_image2.bin"),
	env.VerboseAction("chmod +rx $PICK $CHKSUM $PAD $OTA", "."),
	env.VerboseAction("$PICK 0x`grep __ram_image2_text_start__ $BUILD_DIR/firmware.nmap | gawk '{print $$1}'` 0x`grep __ram_image2_text_end__ $BUILD_DIR/firmware.nmap | gawk '{print $$1}'` $BUILD_DIR/ram_2.r.bin $BUILD_DIR/ram_2.bin raw", "."),
	env.VerboseAction("$PICK 0x`grep __ram_image2_text_start__ $BUILD_DIR/firmware.nmap | gawk '{print $$1}'` 0x`grep __ram_image2_text_end__ $BUILD_DIR/firmware.nmap | gawk '{print $$1}'` $BUILD_DIR/ram_2.bin $BUILD_DIR/ram_2.p.bin", "."),
	env.VerboseAction("$PICK 0x`grep __xip_image2_start__ $BUILD_DIR/firmware.nmap | gawk '{print $$1}'` 0x`grep __xip_image2_start__ $BUILD_DIR/firmware.nmap | gawk '{print $$1}'` $BUILD_DIR/xip_image2.bin $BUILD_DIR/xip_image2.p.bin", "."),
	env.VerboseAction("cat $BUILD_DIR/xip_image2.p.bin > $BUILD_DIR/image2_all_ota1.bin", "Generating $TARGET"),
	env.VerboseAction("cat $BUILD_DIR/ram_2.p.bin >> $BUILD_DIR/image2_all_ota1.bin", "."),
	]

uploading = [
	env.VerboseAction('echo -n "set $$" > %s/BTAsize.gdb' % (env["BUILD_DIR"]), 'Uploading binary'),
	env.VerboseAction('echo "BOOTALLFILESize = 0x$$(echo "obase=16; $$(stat -c %%s %s)"|bc)" >> %s/BTAsize.gdb' % (env["BOOTALL_BIN"], env["BUILD_DIR"]), '.'),
	env.VerboseAction('echo -n "set $$" > %s/fwsize.gdb' % (env["BUILD_DIR"]), '.'),
	env.VerboseAction('echo "RamFileSize = 0x$$(echo "obase=16; $$(stat -c %%s $BUILD_DIR/image2_all_ota1.bin)"|bc)" >> %s/fwsize.gdb' % (env["BUILD_DIR"]), '.'),
	replace_rtl(env),
	env.VerboseAction('cp %s $BUILD_DIR/boot_all.bin' % env["BOOTALL_BIN"], '.'),
	env.VerboseAction('openocd -f interface/cmsis-dap.cfg -f %s/scripts/openocd/%s/amebaz.cfg -c "init" > /dev/null 2>&1 &  export ocdpid=$! ; arm-none-eabi-gdb -batch --init-eval-command="dir %s/scripts/openocd/%s" -x %s/rtl_gdb_flash_write.txt ; kill -9 $$ocdpid' % (env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"]), env["PLATFORM_DIR"], ''.join(env["PIOFRAMEWORK"]), env["BUILD_DIR"]), '.'),
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

