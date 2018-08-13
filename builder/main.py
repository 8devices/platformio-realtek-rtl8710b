import sys
from os.path import basename, join
from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default, DefaultEnvironment)
from platformio import util

env = DefaultEnvironment()

GCC_TOOLCHAIN = ""
platform = env.PioPlatform()
env["PLATFORM_DIR"] = platform.get_dir()

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

	PROGSUFFIX = ".elf"
)

if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

frameworks = {
	"sdk-ameba-v4.0b":env["PIOHOME_DIR"] + "/packages/framework-sdk-ameba-v4.0b-gcc/component/soc/realtek/8711b/misc/bsp/image/boot_all.bin"
}

def get_bootallbin_dir(env):
	env["BOOTALL_BIN"] = join(frameworks.get(''.join(env["PIOFRAMEWORK"]), ""))
	if not env["BOOTALL_BIN"]:
		raise Exception("Framework '%s' is invalid\r\n" % ''.join(env["PIOFRAMEWORK"]))

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

prerequirement = [
	get_bootallbin_dir(env),
	replace_ld(env),
	env.VerboseAction("chmod 777 %s" % env["BOOTALL_BIN"], "Executing prerequirements"),
	env.VerboseAction("$OBJCOPY -I binary -O elf32-littlearm -B arm %s $BUILD_DIR/boot_all.o" % env["BOOTALL_BIN"], "Generating $TARGET"),
	env.Append(PIOBUILDFILES = "%s/boot_all.o" % env["BUILD_DIR"])
		]

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
		Manipulate = Builder(
			action = env.VerboseAction(manipulating, "Manipulating images")),
		)
)

prerequirement_b = env.Prerequirement("$BUILD_DIR/boot_all.o", env["BOOTALL_BIN"])
program_b = env.BuildProgram()
manipulate_images_b = env.Manipulate("$BUILD_DIR/image2_all_ota1.bin", [program_b, prerequirement_b])
upload = env.Alias("upload", manipulate_images_b, uploading)
AlwaysBuild(upload)
Default([manipulate_images_b])



