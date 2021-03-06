import os
from os.path import isdir, join
from SCons.Script import DefaultEnvironment
from platformio import util

EXECUTABLE_SUFFIX = ""
if os.name == "nt":
	EXECUTABLE_SUFFIX = r".exe"

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-sdk-ameba-v4.0b-gcc")
assert isdir(FRAMEWORK_DIR)
AMEBA_TOOLDIR = join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "misc", "iar_utility", "common", "tools")
FLASH_TOOLDIR = join(FRAMEWORK_DIR, "component", "soc", "realtek", "8195a", "misc", "gcc_utility")
FLASHDOWNLOAD_TOOLDIR = join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "misc", "gnu_utility", "flash_download", "image")
DEBUG_TOOLDIR = join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "misc", "gcc_utility")

env.Append(
	CPPPATH = [
		env.subst("$PROJECTINCLUDE_DIR"),
		join(FRAMEWORK_DIR, "project", "realtek_amebaz_va0_example", "inc"),
		join(FRAMEWORK_DIR, "component", "os", "freertos"),
		join(FRAMEWORK_DIR, "component", "os", "freertos", "freertos_v8.1.2", "Source", "include"),
		join(FRAMEWORK_DIR, "component", "os", "freertos", "freertos_v8.1.2", "Source", "portable", "GCC", "ARM_CM4F"),
		join(FRAMEWORK_DIR, "component", "os", "os_dep", "include"),
		join(FRAMEWORK_DIR, "component", "common", "api", "network", "include"),
		join(FRAMEWORK_DIR, "component", "common", "api"),
		join(FRAMEWORK_DIR, "component", "common", "api", "at_cmd"),
		join(FRAMEWORK_DIR, "component", "common", "api", "platform"),
		join(FRAMEWORK_DIR, "component", "common", "api", "wifi"),
		join(FRAMEWORK_DIR, "component", "common", "api", "wifi", "rtw_wpa_supplicant", "src"),
		join(FRAMEWORK_DIR, "component", "common", "api", "wifi", "rtw_wowlan"),
		join(FRAMEWORK_DIR, "component", "common", "api", "wifi", "rtw_wpa_supplicant", "wpa_supplicant"),
		join(FRAMEWORK_DIR, "component", "common", "application"),
		join(FRAMEWORK_DIR, "component", "common", "application", "mqtt", "MQTTClient"),
		join(FRAMEWORK_DIR, "component", "common", "application", "mqtt", "MQTTPacket"),
		join(FRAMEWORK_DIR, "component", "common", "example"),
		join(FRAMEWORK_DIR, "component", "common", "example", "wlan_fast_connect"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "modules"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "sdio", "realtek", "sdio_host", "inc"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "inic", "rtl8711b"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "usb_class", "device"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "usb_class", "device", "class"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "wlan", "realtek", "include"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "wlan", "realtek", "src", "osdep"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "wlan", "realtek", "src", "hci"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "wlan", "realtek", "src", "hal"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "wlan", "realtek", "src", "hal", "rtl8711b"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "wlan", "realtek", "src", "hal", "OUTSRC"),
		join(FRAMEWORK_DIR, "component", "common", "drivers", "wlan", "realtek", "wlan_ram_map", "rom"),
		join(FRAMEWORK_DIR, "component", "common", "file_system"),
		join(FRAMEWORK_DIR, "component", "common", "network"),
		join(FRAMEWORK_DIR, "component", "common", "network", "ssl", "polarssl-1.3.8", "include"),
		join(FRAMEWORK_DIR, "component", "common", "network", "ssl", "ssl_ram_map", "rom"),
		join(FRAMEWORK_DIR, "component", "common", "test"),
		join(FRAMEWORK_DIR, "component", "common", "utilities"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "app", "monitor", "include"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "cmsis"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "cmsis", "device"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "fwlib"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "fwlib", "include"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "fwlib", "ram_lib", "crypto"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "fwlib", "rom_lib"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "swlib", "os_dep", "include"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "swlib", "std_lib", "include"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "swlib", "std_lib", "libc", "include"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "swlib", "std_lib", "libc", "rom", "string"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "swlib", "std_lib", "libgcc", "rtl8195a", "include"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "swlib", "rtl_lib"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "misc"),
		join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "misc", "os"),
		join(FRAMEWORK_DIR, "component", "common", "mbed", "api"),
		join(FRAMEWORK_DIR, "component", "common", "mbed", "hal"),
		join(FRAMEWORK_DIR, "component", "common", "mbed", "hal_ext"),
		join(FRAMEWORK_DIR, "component", "common", "mbed", "targets", "cmsis"),
		join(FRAMEWORK_DIR, "component", "common", "mbed", "targets", "hal", "rtl8711b"),
		join(FRAMEWORK_DIR, "component", "common", "network", "websocket"),
	],

	LIBPATH=[
		FRAMEWORK_DIR + "/component/soc/realtek/8711b/misc/bsp/lib/common/GCC",
		env["PLATFORM_DIR"] + "/scripts/ld/sdk-ameba-v4.0b",
	],

	LIBS=[
		"_platform", "_wps", "_rtlstd", "_dct", "m", "c", "nosys", "_websocket", "_http", "_mdns"
	]
)

if "PIO_FRAMEWORK_AMEBAZ_USE_MP" in env.Flatten(env["CPPDEFINES"]):
    env.Append(
            LIBS=["_wlan_mp"])
else:
    env.Append(
            LIBS=["_wlan"])

env.Replace(
	LDSCRIPT_PATH = [
		env["PLATFORM_DIR"] + "/scripts/ld/sdk-ameba-v4.0b/rlx8711B-symbol-v02-img2_xip1.ld",
			],

	PICK = join(AMEBA_TOOLDIR, "pick" + EXECUTABLE_SUFFIX),
	PAD  = join(AMEBA_TOOLDIR, "padding" + EXECUTABLE_SUFFIX),
	CHKSUM = join(AMEBA_TOOLDIR, "checksum" + EXECUTABLE_SUFFIX),
	OTA = join(AMEBA_TOOLDIR, "ota" + EXECUTABLE_SUFFIX),
)

sources = [
	"+<" + FRAMEWORK_DIR + "/component/common/api/at_cmd/atcmd_lwip.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/wifi/wifi_conf.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/uart_adapter/uart_adapter.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/cmsis/device/app_start.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/startup.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/cmsis/device/system_8195a.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/at_cmd/atcmd_sys.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/at_cmd/atcmd_wifi.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/at_cmd/log_service.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/app/monitor/ram/low_level_io.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/app/monitor/ram/monitor.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/app/monitor/ram/rtl_consol.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/app/monitor/ram/rtl_trace.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/wifi/rtw_wpa_supplicant/wpa_supplicant/wifi_eap_config.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/wifi/rtw_wpa_supplicant/wpa_supplicant/wifi_wps_config.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/wifi/wifi_ind.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/wifi/wifi_promisc.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/wifi/wifi_simple_config.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/wifi/wifi_util.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/lwip_netconf.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTClient/MQTTClient.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTConnectClient.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTConnectServer.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTDeserializePublish.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTFormat.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTClient/MQTTFreertos.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTPacket.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTSerializePublish.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTSubscribeClient.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTSubscribeServer.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTUnsubscribeClient.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTUnsubscribeServer.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/network/src/ping_test.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/utilities/ssl_client.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/utilities/tcptest.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/api/network/src/wlan_network.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/drivers/wlan/realtek/src/osdep/lwip_intf.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/websocket/wsclient_tls.c>",  
	"+<" + FRAMEWORK_DIR + "/component/common/network/dhcp/dhcps.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/sntp/sntp.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/aesni.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/blowfish.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/camellia.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ccm.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/certs.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/cipher.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/cipher_wrap.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/debug.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ecp_ram.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/entropy.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/entropy_poll.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/error.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/gcm.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/havege.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/md2.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/md4.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/memory_buffer_alloc.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/net.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/padlock.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pbkdf2.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pkcs11.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pkcs12.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pkcs5.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pkparse.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/platform.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ripemd160.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_cache.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_ciphersuites.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_cli.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_srv.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_tls.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/threading.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/timing.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/version.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/version_features.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509_create.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509_crl.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509_crt.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509_csr.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509write_crt.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509write_csr.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/xtea.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/ssl/ssl_ram_map/ssl_ram_map.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/portable/GCC/ARM_CM4F/port.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/freertos/cmsis_os.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/croutine.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/event_groups.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/freertos/freertos_service.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/list.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/queue.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/tasks.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/timers.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/os_dep/device_lock.c>",
	"+<" + FRAMEWORK_DIR + "/component/os/os_dep/osdep_service.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/analogin_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/dma_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/efuse_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/flash_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/gpio_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/gpio_irq_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/i2c_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/i2s_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/nfc_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/pinmap.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/pinmap_common.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/port_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/pwmout_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/rtc_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/serial_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/sleep.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/spi_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/sys_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/timer_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/us_ticker.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/us_ticker_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/wait_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/wdt_api.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_dsleepcfg.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_dstandbycfg.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_intfcfg.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/misc/rtl8710b_ota.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_pinmapcfg.c>",
	"+<" + FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_sleepcfg.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/bcast/example_bcast.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/dct/example_dct.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/eap/example_eap.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/example_entry.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/get_beacon_frame/example_get_beacon_frame.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/high_load_memory_use/example_high_load_memory_use.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/http_client/example_http_client.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/httpc/example_httpc.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/httpd/example_httpd.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/http_download/example_http_download.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/mcast/example_mcast.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/mdns/example_mdns.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/mqtt/example_mqtt.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/nonblock_connect/example_nonblock_connect.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/rarp/example_rarp.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/sntp_showtime/example_sntp_showtime.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/socket_select/example_socket_select.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/ssl_download/example_ssl_download.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/ssl_server/example_ssl_server.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/tcp_keepalive/example_tcp_keepalive.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/uart_atcmd/example_uart_atcmd.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/wifi_mac_monitor/example_wifi_mac_monitor.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/wlan_fast_connect/example_wlan_fast_connect.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/wlan_scenario/example_wlan_scenario.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/websocket/example_wsclient.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/xml/example_xml.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/example/uart_firmware_update/example_uart_update.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/httpc/httpc_tls.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/httpd/httpd_tls.c>",   
	"+<" + FRAMEWORK_DIR + "/component/common/utilities/cJSON.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/utilities/http_client.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/utilities/uart_socket.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/utilities/webserver.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/utilities/xml.c>",
	]

lwip_sources = list("")
lwip_version = "1.4.1"
for i, val in enumerate(env.Flatten(env["CPPDEFINES"])):
    if val == "PIO_FRAMEWORK_AMEBAZ_LWIP":
        lwip_version = str(env.Flatten(env["CPPDEFINES"])[i + 1])
        break

if lwip_version != "CUSTOM":
	env.Append(
		CPPPATH = [
			join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v" + lwip_version, "port", "realtek", "freertos"),
			join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v" + lwip_version, "src", "include"),
			join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v" + lwip_version, "src", "include", "lwip"),
			join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v" + lwip_version, "src", "include", "ipv4"),
        		join(FRAMEWORK_DIR, "component", "common", "network", "lwip", "lwip_v" + lwip_version, "port", "realtek"),
			]
		)
	lwip_sources = [
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/api/api_lib.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/api/api_msg.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/api/err.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/api/netbuf.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/api/netdb.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/api/netifapi.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/api/sockets.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/api/tcpip.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/ipv4/autoip.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/ipv4/icmp.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/ipv4/igmp.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/ipv4/inet.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/ipv4/inet_chksum.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/ipv4/ip.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/ipv4/ip_addr.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/ipv4/ip_frag.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/def.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/dhcp.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/dns.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/init.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/lwip_timers.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/mem.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/memp.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/netif.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/pbuf.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/raw.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/stats.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/sys.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/tcp.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/tcp_in.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/tcp_out.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/core/udp.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/src/netif/etharp.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/port/realtek/freertos/ethernetif.c>",
	"+<" + FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v" + lwip_version + "/port/realtek/freertos/sys_arch.c>",

		]
sources = sources + lwip_sources

freertos_sources = list("")
heap_version = "5"
for i, val in enumerate(env.Flatten(env["CPPDEFINES"])):
    if val == "PIO_FRAMEWORK_AMEBAZ_FREERTOS_HEAP":
        heap_version = str(env.Flatten(env["CPPDEFINES"])[i + 1])
        break
freertos_sources = ["+<" + FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/portable/MemMang/heap_" + heap_version + ".c>"]
sources = sources + freertos_sources

env.Replace(
	BOOTALL_BIN = join(FRAMEWORK_DIR, "component", "soc", "realtek", "8711b", "misc", "bsp", "image", "boot_all.bin")
)

prerequirement = [
	env.VerboseAction("$OBJCOPY -I binary -O elf32-littlearm -B arm $BOOTALL_BIN " + join(env.subst(env["BUILD_DIR"]), "boot_all.o"), "Generating $TARGET")
		]
env.Append(BUILDERS = dict(Prerequirement = Builder(action = env.VerboseAction(prerequirement, "Generating boot_all.o"))))
prerequirement_b = env.Prerequirement(join(env.subst(env["BUILD_DIR"]), "boot_all.o"), env["BOOTALL_BIN"]) 

libs = []
libs.append(env.BuildLibrary(join("$BUILD_DIR", "SDK"), FRAMEWORK_DIR, sources))
libs.append(env.StaticLibrary(join("$BUILD_DIR", "boot_all"), prerequirement_b))
env.Prepend(LIBS=libs)


