import sys
from os.path import basename, join
from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default, DefaultEnvironment)
from platformio import util

env = DefaultEnvironment()
platform = env.PioPlatform()

# CIA IS PLATFORMIO.INI "upload_flags"
#print(env["UPLOAD_FLAGS"])

env.Replace(

	AR = "arm-none-eabi-ar",
	CC = "arm-none-eabi-gcc",
	AS = "arm-none-eabi-as",
	NM = "arm-none-eabi-nm",
	LD = "arm-none-eabi-gcc",
	GDB = "arm-none-eabi-gdb",
	OBJCOPY = "arm-none-eabi-objcopy",
	OBJDUMP = "arm-none-eabi-objdump",

	CFLAGS = [
		"-DM3",
		"-DCONFIG_PLATFORM_8711B",
		"-mcpu=cortex-m4",
		"-mthumb",
		"-mfloat-abi=hard",
		"-mfpu=fpv4-sp-d16",
		"-g2",
		"-w",
		"-O2",
		"-Wno-pointer-sign",
		"-fno-common",
		"-fmessage-length=0",
		"-ffunction-sections",
		"-fdata-sections",
		"-fomit-frame-pointer",
		"-fno-short-enums",
		"-DF_CPU=166000000L",
		"-std=gnu99",
		"-fsigned-char"
	],
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
		"-Wl,-wrap,realloc"
	]
)
def printenv(target, source, env):
#	ENV KINTAMIEJI (VELIAU ISTRINT)
#	print(env.subst("$AMEBA_SOURCES")) - atskirta tarpais
#	print(env["AMEBA_SOURCES"])        - lauztiniuose skliaustuose, kiekvienas kabutese, atskirta kableliais
#	print(env.get("$AMEBA_SOURCES"))   - nieko
	print('--')
#	print(env["SOURCE_LIST"])
#	print(SOURCES_LIST)

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
	with open("%s/openocd/scripts/_rtl_gdb_flash_write.txt" % env["FRAMEWORK_DIR"], "rt") as fin:
		with open("%s/openocd/scripts/rtl_gdb_flash_write.txt" % env["FRAMEWORK_DIR"], "wt") as fout:
			for line in fin:
				fout.write(line.replace('BUILD_DIR', '%s' % env.subst(env["BUILD_DIR"])).replace('SCRIPTS_DIR', '%s/openocd/scripts' % env["FRAMEWORK_DIR"]))

prerequirement = [
	env.BuildFrameworks(env.get("PIOFRAMEWORK")),
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
	env.VerboseAction('echo -n "set $$" > %s/openocd/scripts/BTAsize.gdb' % env["FRAMEWORK_DIR"], 'Uploading binary'),
	env.VerboseAction('echo "BOOTALLFILESize = 0x$$(echo "obase=16; $$(stat -c %%s %s)"|bc)" >> %s/openocd/scripts/BTAsize.gdb' % (env["BOOTALL_BIN"], env["FRAMEWORK_DIR"]), '.'),
	env.VerboseAction('echo -n "set $$" > %s/openocd/scripts/fwsize.gdb' % env["FRAMEWORK_DIR"], '.'),
	env.VerboseAction('echo "RamFileSize = 0x$$(echo "obase=16; $$(stat -c %%s $BUILD_DIR/image2_all_ota1.bin)"|bc)" >> %s/openocd/scripts/fwsize.gdb' % env["FRAMEWORK_DIR"], '.'),
	replace_rtl(env),
	env.VerboseAction('cp %s $BUILD_DIR/boot_all.bin' % env["BOOTALL_BIN"], '.'),
	env.VerboseAction('export FRAMEWORK_DIR="%s"; sh %s/openocd/scripts/openocd.sh' % (env["FRAMEWORK_DIR"], env["FRAMEWORK_DIR"]), '.'),
	]

env.Append(
	BUILDERS = dict(
		Prerequirement = Builder(
			action = env.VerboseAction(prerequirement, "Executing prerequirements")),
		Linker = Builder(
			action = env.VerboseAction("$LD $LINKFLAGS -o $TARGET $SOURCES %s %s -T$LDSCRIPT_PATH" % (' '.join(prefix_libpaths(env)), ' '.join(prefix_libs(env))), "Linking $TARGET")),
		Compiler = Builder(
			action = env.VerboseAction("$CC $CFLAGS %s -c $SOURCES -o $TARGET" % ' '.join(prefix_includes(env)), "Compiling $TARGET"),
			suffix = ".o",
			single_source = 1),
		Manipulate = Builder(
			action = env.VerboseAction(manipulating, "Manipulating images")),
		)
)
prerequirement_b = env.Prerequirement(("$BUILD_DIR/boot_all.o"), (env["BOOTALL_BIN"]))
compiler_b = env.Compiler(env["SOURCE_LIST"])
linker_b = env.Linker("$BUILD_DIR/program.axf", [prerequirement_b, compiler_b])
manipulate_images_b = env.Manipulate("$BUILD_DIR/image2_all_ota1.bin", linker_b)
#env.AddPreAction(prerequirement_b, "ls")

upload = env.Alias("upload", [manipulate_images_b, env["BOOTALL_BIN"]], uploading)

AlwaysBuild(upload)

Default([manipulate_images_b])

