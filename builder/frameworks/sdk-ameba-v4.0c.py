
from os.path import isdir, join

from SCons.Script import DefaultEnvironment

from platformio import util

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-sdk-ameba-v4.0b-gcc")
assert isdir(FRAMEWORK_DIR)

PROJECTINCLUDE_DIR = util.get_projectinclude_dir()

env['CPPPATH'] = [
	'#inc',
	'#component/os/freertos',
	'#component/os/freertos/freertos_v8.1.2/Source/include',
	'#component/os/freertos/freertos_v8.1.2/Source/portable/GCC/ARM_CM4F',
	'#component/os/os_dep/include',
	'#component/common/api/network/include',
	'#component/common/api',
	'#component/common/api/at_cmd',
	'#component/common/api/platform',
	'#component/common/api/wifi',
	'#component/common/api/wifi/rtw_wpa_supplicant/src',
	'#component/common/api/wifi/rtw_wowlan',
	'#component/common/api/wifi/rtw_wpa_supplicant/wpa_supplicant',
	'#component/common/application',
	'#component/common/application/mqtt/MQTTClient',
	'#component/common/application/mqtt/MQTTPacket',
	'#component/common/example',
	'#component/common/example/wlan_fast_connect',
	'#component/common/drivers/modules',
	'#component/common/drivers/sdio/realtek/sdio_host/inc',
	'#component/common/drivers/inic/rtl8711b',
	'#component/common/drivers/usb_class/device',
	'#component/common/drivers/usb_class/device/class',
	'#component/common/drivers/wlan/realtek/include',
	'#component/common/drivers/wlan/realtek/src/osdep',
	'#component/common/drivers/wlan/realtek/src/hci',
	'#component/common/drivers/wlan/realtek/src/hal',
	'#component/common/drivers/wlan/realtek/src/hal/rtl8711b',
	'#component/common/drivers/wlan/realtek/src/hal/OUTSRC',
	'#component/common/drivers/wlan/realtek/wlan_ram_map/rom',
	'#component/common/file_system',
	'#component/common/network',
	'#component/common/network/lwip/lwip_v1.4.1/port/realtek/freertos',
	'#component/common/network/lwip/lwip_v1.4.1/src/include',
	'#component/common/network/lwip/lwip_v1.4.1/src/include/lwip',
	'#component/common/network/lwip/lwip_v1.4.1/src/include/ipv4',
	'#component/common/network/lwip/lwip_v1.4.1/port/realtek',
	'#component/common/network/ssl/polarssl-1.3.8/include',
	'#component/common/network/ssl/ssl_ram_map/rom',
	'#component/common/test',
	'#component/common/utilities',
	'#component/soc/realtek/8711b/app/monitor/include',
	'#component/soc/realtek/8711b/cmsis',
	'#component/soc/realtek/8711b/cmsis/device',
	'#component/soc/realtek/8711b/fwlib',
	'#component/soc/realtek/8711b/fwlib/include',
	'#component/soc/realtek/8711b/fwlib/ram_lib/crypto',
	'#component/soc/realtek/8711b/fwlib/rom_lib',
	'#component/soc/realtek/8711b/swlib/os_dep/include',
	'#component/soc/realtek/8711b/swlib/std_lib/include',
	'#component/soc/realtek/8711b/swlib/std_lib/libc/include',
	'#component/soc/realtek/8711b/swlib/std_lib/libc/rom/string',
	'#component/soc/realtek/8711b/swlib/std_lib/libgcc/rtl8195a/include',
	'#component/soc/realtek/8711b/swlib/rtl_lib',
	'#component/soc/realtek/8711b/misc',
	'#component/soc/realtek/8711b/misc/os',
	'#component/common/mbed/api',
	'#component/common/mbed/hal',
	'#component/common/mbed/hal_ext',
	'#component/common/mbed/targets/cmsis',
	'#component/common/mbed/targets/hal/rtl8711b',
	'#project/altek_8195a_gen_project/rtl8195a/sw/lib/sw_lib/mbed/api',
	'#component/common/application/mqtt/MQTTClient',
	'#component/common/network/websocket',
	]
#		PROJECTINCLUDE_DIR padaryt prepend prie CPPPATH

	env.Prepend(
	LIBPATH=[
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "misc", "bsp", "lib", "common", "GCC")
	],

	LIBS=[
		"_platform", "_wlan", "_wps", "_dct", "_rtlstd", "m", "c", "nosys", "gcc", "_websocket", "_http", "_mdns"
	]
#	libm libc libnosys libgcc nera LIBPATH direktorijoj
)

#env.Append(
#	LIBSOURCE_DIRS=[
#		join(FRAMEWORK_DIR, "component", "common", "application", "mqtt", "MQTTClient")
#	]
#)

# GALI SKIRTIS
env.Replace(
	LDSCRIPT_PATH=[join(FRAMEWORK_DIR, "project", "realtek_amebaz_va0_example", "GCC-RELEASE", "rlx8711B-symbol-v02-img2_xip1.ld")],


#	GALI SKIRTIS
#	UPLOADER="openocd",
#	UPLOADERFLAGS=["-s", platform.get_package_dir("tool-openocd") or ""] + debug_tools.get(upload_protocol).get("server").get("arguments", []) + ["-c", "program {{$SOURCE}} %s verify reset; shutdown;" % env.BoardConfig().get("upload").get("flash_start", "")],
#	UPLOADCMD="$UPLOADER $UPLOADERFLAGS"


)

libs= []

libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkAmeba"),
        join(FRAMEWORK_DIR, "component")
#	join(FRAMEWORK_DIR, "component", "common", "api"),
#	join(FRAMEWORK_DIR, "component", "common", "api", "at_cmd"),
#	join(FRAMEWORK_DIR, "component", "common", "api", "network", "src"),
#	join(FRAMEWORK_DIR, "component", "common", "api", "wifi"),
#	join(FRAMEWORK_DIR, "component", "common", "api", "wifi", "rtw_wpa_supplicant", "wpa_supplicant"),
#	join(FRAMEWORK_DIR, "component", "common", "application", "mqtt", "MQTTClient"),
#	join(FRAMEWORK_DIR, "component", "common", "application", "mqtt", "MQTTPacket"),
#	join(FRAMEWORK_DIR, "component", "common", "application", "uart_adapter"),
#	join(FRAMEWORK_DIR, "component", "common", "drivers", "wlan", "realtek", "src", "osdep"),
#	join(FRAMEWORK_DIR, "component", "common", "example"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "bcast"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "dct"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "eap"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "get_beacon_frame"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "high_load_memory_use"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "httpc"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "http_client"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "httpd"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "http_download"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "mcast"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "mdns"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "mqtt"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "nonblock_connect"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "rarp"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "sntp_showtime"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "socket_select"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "ssl_download"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "ssl_server"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "tcp_keepalive"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "uart_atcmd"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "uart_firmware_update"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "websocket"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "wifi_mac_monitor"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "wlan_fast_connect"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "wlan_scenario"),
#	join(FRAMEWORK_DIR, "component", "common", "example", "xml"),
#	join(FRAMEWORK_DIR, "component", "common", "mbed", "targets", "hal", "rtl8711b"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "dhcp"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "httpc"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "httpd   "),
#	join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v1.4.1", "port", "realtek", "freertos"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v1.4.1", "src", "api"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v1.4.1", "src", "core"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v1.4.1", "src", "core", "ipv4"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v1.4.1", "src", "netif"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "sntp"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "ssl", "polarssl-1.3.8", "library"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "ssl", "ssl_ram_map"),
#	join(FRAMEWORK_DIR, "component", "common", "network", "websocket  "),
#	join(FRAMEWORK_DIR, "component", "common", "utilities"),
#	join(FRAMEWORK_DIR, "component", "os", "freertos"),
#	join(FRAMEWORK_DIR, "component", "os", "freertos", "freertos_v8.1.2", "Source"),
#	join(FRAMEWORK_DIR, "component", "os", "freertos", "freertos_v8.1.2", "Source", "portable", "GCC", "ARM_CM4F"),
#	join(FRAMEWORK_DIR, "component", "os", "freertos", "freertos_v8.1.2", "Source", "portable", "MemMang"),
#	join(FRAMEWORK_DIR, "component", "os", "os_dep"),
#	join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "app", "monitor", "ram"),
#	join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "cmsis", "device"),
#	join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "fwlib", "ram_lib"),
#	join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "misc")]
	)
)


env.Prepend(LIBS=libs)

