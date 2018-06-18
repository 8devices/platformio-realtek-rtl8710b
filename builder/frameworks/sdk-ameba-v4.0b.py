
from os.path import isdir, join

from SCons.Script import DefaultEnvironment

from platformio import util

env = DefaultEnvironment()
platform = env.PioPlatform()

# JAU UZDEFINE'INTA MAIN SKRIPTE
FRAMEWORK_DIR = platform.get_package_dir("framework-sdk-ameba-v4.0b-gcc")
assert isdir(FRAMEWORK_DIR)

PROJECTINCLUDE_DIR = util.get_projectinclude_dir()

print("BUILD_DIR = " + env.subst(env.get("BUILD_DIR")))
print("PROGNAME = " + env.get("PROGNAME"))
print("BUILDSRC_DIR = " + env.subst(env.get("BUILDSRC_DIR")))
print("PROJECTSRC_DIR = " + env.subst(env.get("PROJECTSRC_DIR")))
print("PROJECTINCLUDE_DIR = " + env.subst(env.get("PROJECTINCLUDE_DIR")))
print(env.subst(env.get("LIBSOURCE_DIRS")))

env.PrependUnique(
	CPPPPATH = [
		PROJECTINCLUDE_DIR,
		join(FRAMEWORK_DIR, 'component/os/freertos'),
		join(FRAMEWORK_DIR, 'component/os/freertos/freertos_v8.1.2/Source/include'),
		join(FRAMEWORK_DIR, 'component/os/freertos/freertos_v8.1.2/Source/portable/GCC/ARM_CM4F'),
		join(FRAMEWORK_DIR, 'component/os/os_dep/include'),
		join(FRAMEWORK_DIR, 'component/common/api/network/include'),
		join(FRAMEWORK_DIR, 'component/common/api'),
		join(FRAMEWORK_DIR, 'component/common/api/at_cmd'),
		join(FRAMEWORK_DIR, 'component/common/api/platform'),
		join(FRAMEWORK_DIR, 'component/common/api/wifi'),
		join(FRAMEWORK_DIR, 'component/common/api/wifi/rtw_wpa_supplicant/src'),
		join(FRAMEWORK_DIR, 'component/common/api/wifi/rtw_wowlan'),
		join(FRAMEWORK_DIR, 'component/common/api/wifi/rtw_wpa_supplicant/wpa_supplicant'),
		join(FRAMEWORK_DIR, 'component/common/application'),
		join(FRAMEWORK_DIR, 'component/common/application/mqtt/MQTTClient'),
		join(FRAMEWORK_DIR, 'component/common/application/mqtt/MQTTPacket'),
		join(FRAMEWORK_DIR, 'component/common/example'),
		join(FRAMEWORK_DIR, 'component/common/example/wlan_fast_connect'),
		join(FRAMEWORK_DIR, 'component/common/drivers/modules'),
		join(FRAMEWORK_DIR, 'component/common/drivers/sdio/realtek/sdio_host/inc'),
		join(FRAMEWORK_DIR, 'component/common/drivers/inic/rtl8711b'),
		join(FRAMEWORK_DIR, 'component/common/drivers/usb_class/device'),
		join(FRAMEWORK_DIR, 'component/common/drivers/usb_class/device/class'),
		join(FRAMEWORK_DIR, 'component/common/drivers/wlan/realtek/include'),
		join(FRAMEWORK_DIR, 'component/common/drivers/wlan/realtek/src/osdep'),
		join(FRAMEWORK_DIR, 'component/common/drivers/wlan/realtek/src/hci'),
		join(FRAMEWORK_DIR, 'component/common/drivers/wlan/realtek/src/hal'),
		join(FRAMEWORK_DIR, 'component/common/drivers/wlan/realtek/src/hal/rtl8711b'),
		join(FRAMEWORK_DIR, 'component/common/drivers/wlan/realtek/src/hal/OUTSRC'),
		join(FRAMEWORK_DIR, 'component/common/drivers/wlan/realtek/wlan_ram_map/rom'),
		join(FRAMEWORK_DIR, 'component/common/file_system'),
		join(FRAMEWORK_DIR, 'component/common/network'),
		join(FRAMEWORK_DIR, 'component/common/network/lwip/lwip_v1.4.1/port/realtek/freertos'),
		join(FRAMEWORK_DIR, 'component/common/network/lwip/lwip_v1.4.1/src/include'),
		join(FRAMEWORK_DIR, 'component/common/network/lwip/lwip_v1.4.1/src/include/lwip'),
		join(FRAMEWORK_DIR, 'component/common/network/lwip/lwip_v1.4.1/src/include/ipv4'),
		join(FRAMEWORK_DIR, 'component/common/network/lwip/lwip_v1.4.1/port/realtek'),
		join(FRAMEWORK_DIR, 'component/common/network/ssl/polarssl-1.3.8/include'),
		join(FRAMEWORK_DIR, 'component/common/network/ssl/ssl_ram_map/rom'),
		join(FRAMEWORK_DIR, 'component/common/test'),
		join(FRAMEWORK_DIR, 'component/common/utilities'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/app/monitor/include'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/cmsis'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/cmsis/device'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/fwlib'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/fwlib/include'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/fwlib/ram_lib/crypto'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/fwlib/rom_lib'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/swlib/os_dep/include'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/swlib/std_lib/include'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/swlib/std_lib/libc/include'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/swlib/std_lib/libc/rom/string'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/swlib/std_lib/libgcc/rtl8195a/include'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/swlib/rtl_lib'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/misc'),
		join(FRAMEWORK_DIR, 'component/soc/realtek/8711b/misc/os'),
		join(FRAMEWORK_DIR, 'component/common/mbed/api'),
		join(FRAMEWORK_DIR, 'component/common/mbed/hal'),
		join(FRAMEWORK_DIR, 'component/common/mbed/hal_ext'),
		join(FRAMEWORK_DIR, 'component/common/mbed/targets/cmsis'),
		join(FRAMEWORK_DIR, 'component/common/mbed/targets/hal/rtl8711b'),
		join(FRAMEWORK_DIR, 'project/altek_8195a_gen_project/rtl8195a/sw/lib/sw_lib/mbed/api'),
		join(FRAMEWORK_DIR, 'component/common/application/mqtt/MQTTClient'),
		join(FRAMEWORK_DIR, 'component/common/network/websocket'),
	],


	LIBPATH=[
		"%s/component/soc/realtek/8711b/misc/bsp/lib/common/GCC" % (FRAMEWORK_DIR)
	],
# NUIMT -l IR PARASYT SKRIPTA
	LIBS=[
		"-l_platform", "-l_wlan", "-l_wps", "-l_dct", "-l_rtlstd", "-lm", "-lc", "-lnosys", "-lgcc", "-l_websocket", "-l_http", "-l_mdns"
	]
)

#env.Append(
#	LIBSOURCE_DIRS=[
#		join(FRAMEWORK_DIR, "component", "common", "application", "mqtt", "MQTTClient")
#	]
#)

env.Replace(
	LDSCRIPT_PATH=[join(FRAMEWORK_DIR, "project", "realtek_amebaz_va0_example", "GCC-RELEASE", "rlx8711B-symbol-v02-img2_xip1.ld")],

#	GALI SKIRTIS
#	UPLOADER="openocd",
#	UPLOADERFLAGS=["-s", platform.get_package_dir("tool-openocd") or ""] + debug_tools.get(upload_protocol).get("server").get("arguments", []) + ["-c", "program {{$SOURCE}} %s verify reset; shutdown;" % env.BoardConfig().get("upload").get("flash_start", "")],
#	UPLOADCMD="$UPLOADER $UPLOADERFLAGS"


)
env["AMEBA_SOURCES"] = [
		join(FRAMEWORK_DIR, "component/common/api/at_cmd/atcmd_lwip.c"),
		join(FRAMEWORK_DIR, "component/common/api/wifi/wifi_conf.c"),
		join(FRAMEWORK_DIR, "component/common/application/uart_adapter/uart_adapter.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/cmsis/device/app_start.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/fwlib/ram_lib/startup.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/cmsis/device/system_8195a.c"),
		join(FRAMEWORK_DIR, "component/common/api/at_cmd/atcmd_sys.c"),
		join(FRAMEWORK_DIR, "component/common/api/at_cmd/atcmd_wifi.c"),
		join(FRAMEWORK_DIR, "component/common/api/at_cmd/log_service.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/app/monitor/ram/low_level_io.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/app/monitor/ram/monitor.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/app/monitor/ram/rtl_consol.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/app/monitor/ram/rtl_trace.c"),
		join(FRAMEWORK_DIR, "component/common/api/wifi/rtw_wpa_supplicant/wpa_supplicant/wifi_eap_config.c"),
		join(FRAMEWORK_DIR, "component/common/api/wifi/rtw_wpa_supplicant/wpa_supplicant/wifi_wps_config.c"),
		join(FRAMEWORK_DIR, "component/common/api/wifi/wifi_ind.c"),
		join(FRAMEWORK_DIR, "component/common/api/wifi/wifi_promisc.c"),
		join(FRAMEWORK_DIR, "component/common/api/wifi/wifi_simple_config.c"),
		join(FRAMEWORK_DIR, "component/common/api/wifi/wifi_util.c"),
		join(FRAMEWORK_DIR, "component/common/api/lwip_netconf.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTClient/MQTTClient.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTConnectClient.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTConnectServer.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTDeserializePublish.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTFormat.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTClient/MQTTFreertos.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTPacket.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTSerializePublish.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTSubscribeClient.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTSubscribeServer.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTUnsubscribeClient.c"),
		join(FRAMEWORK_DIR, "component/common/application/mqtt/MQTTPacket/MQTTUnsubscribeServer.c"),
		join(FRAMEWORK_DIR, "component/common/api/network/src/ping_test.c"),
		join(FRAMEWORK_DIR, "component/common/utilities/ssl_client.c"),
		join(FRAMEWORK_DIR, "component/common/utilities/tcptest.c"),
		join(FRAMEWORK_DIR, "component/common/api/network/src/wlan_network.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/api/api_lib.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/api/api_msg.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/api/err.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/api/netbuf.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/api/netdb.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/api/netifapi.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/api/sockets.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/api/tcpip.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/autoip.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/icmp.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/igmp.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/inet.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/inet_chksum.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/ip.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/ip_addr.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/ip_frag.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/def.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/dhcp.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/dns.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/init.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/lwip_timers.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/mem.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/memp.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/netif.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/pbuf.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/raw.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/stats.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/sys.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/tcp.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/tcp_in.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/tcp_out.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/core/udp.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/src/netif/etharp.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/port/realtek/freertos/ethernetif.c"),
		join(FRAMEWORK_DIR, "component/common/drivers/wlan/realtek/src/osdep/lwip_intf.c"),
		join(FRAMEWORK_DIR, "component/common/network/lwip/lwip_v1.4.1/port/realtek/freertos/sys_arch.c"),
		join(FRAMEWORK_DIR, "component/common/network/websocket/wsclient_tls.c"),  
		join(FRAMEWORK_DIR, "component/common/network/dhcp/dhcps.c"),
		join(FRAMEWORK_DIR, "component/common/network/sntp/sntp.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/aesni.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/blowfish.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/camellia.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/ccm.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/certs.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/cipher.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/cipher_wrap.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/debug.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/ecp_ram.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/entropy.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/entropy_poll.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/error.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/gcm.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/havege.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/md2.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/md4.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/memory_buffer_alloc.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/net.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/padlock.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/pbkdf2.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/pkcs11.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/pkcs12.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/pkcs5.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/pkparse.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/platform.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/ripemd160.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/ssl_cache.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/ssl_ciphersuites.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/ssl_cli.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/ssl_srv.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/ssl_tls.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/threading.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/timing.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/version.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/version_features.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/x509.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/x509_create.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/x509_crl.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/x509_crt.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/x509_csr.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/x509write_crt.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/x509write_csr.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/polarssl-1.3.8/library/xtea.c"),
		join(FRAMEWORK_DIR, "component/common/network/ssl/ssl_ram_map/ssl_ram_map.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/freertos_v8.1.2/Source/portable/MemMang/heap_5.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/freertos_v8.1.2/Source/portable/GCC/ARM_CM4F/port.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/cmsis_os.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/freertos_v8.1.2/Source/croutine.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/freertos_v8.1.2/Source/event_groups.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/freertos_service.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/freertos_v8.1.2/Source/list.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/freertos_v8.1.2/Source/queue.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/freertos_v8.1.2/Source/tasks.c"),
		join(FRAMEWORK_DIR, "component/os/freertos/freertos_v8.1.2/Source/timers.c"),
		join(FRAMEWORK_DIR, "component/os/os_dep/device_lock.c"),
		join(FRAMEWORK_DIR, "component/os/os_dep/osdep_service.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/analogin_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/dma_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/efuse_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/flash_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/gpio_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/gpio_irq_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/i2c_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/i2s_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/nfc_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/pinmap.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/pinmap_common.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/port_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/pwmout_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/rtc_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/serial_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/sleep.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/spi_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/sys_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/timer_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/us_ticker.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/us_ticker_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/wait_api.c"),
		join(FRAMEWORK_DIR, "component/common/mbed/targets/hal/rtl8711b/wdt_api.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_dsleepcfg.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_dstandbycfg.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_intfcfg.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/misc/rtl8710b_ota.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_pinmapcfg.c"),
		join(FRAMEWORK_DIR, "component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_sleepcfg.c"),
		join(FRAMEWORK_DIR, "component/common/example/bcast/example_bcast.c"),
		join(FRAMEWORK_DIR, "component/common/example/dct/example_dct.c"),
		join(FRAMEWORK_DIR, "component/common/example/eap/example_eap.c"),
		join(FRAMEWORK_DIR, "component/common/example/example_entry.c"),
		join(FRAMEWORK_DIR, "component/common/example/get_beacon_frame/example_get_beacon_frame.c"),
		join(FRAMEWORK_DIR, "component/common/example/high_load_memory_use/example_high_load_memory_use.c"),
		join(FRAMEWORK_DIR, "component/common/example/http_client/example_http_client.c"),
		join(FRAMEWORK_DIR, "component/common/example/httpc/example_httpc.c"),
		join(FRAMEWORK_DIR, "component/common/example/httpd/example_httpd.c"),
		join(FRAMEWORK_DIR, "component/common/example/http_download/example_http_download.c"),
		join(FRAMEWORK_DIR, "component/common/example/mcast/example_mcast.c"),
		join(FRAMEWORK_DIR, "component/common/example/mdns/example_mdns.c"),
		join(FRAMEWORK_DIR, "component/common/example/mqtt/example_mqtt.c"),
		join(FRAMEWORK_DIR, "component/common/example/nonblock_connect/example_nonblock_connect.c"),
		join(FRAMEWORK_DIR, "component/common/example/rarp/example_rarp.c"),
		join(FRAMEWORK_DIR, "component/common/example/sntp_showtime/example_sntp_showtime.c"),
		join(FRAMEWORK_DIR, "component/common/example/socket_select/example_socket_select.c"),
		join(FRAMEWORK_DIR, "component/common/example/ssl_download/example_ssl_download.c"),
		join(FRAMEWORK_DIR, "component/common/example/ssl_server/example_ssl_server.c"),
		join(FRAMEWORK_DIR, "component/common/example/tcp_keepalive/example_tcp_keepalive.c"),
		join(FRAMEWORK_DIR, "component/common/example/uart_atcmd/example_uart_atcmd.c"),
		join(FRAMEWORK_DIR, "component/common/example/wifi_mac_monitor/example_wifi_mac_monitor.c"),
		join(FRAMEWORK_DIR, "component/common/example/wlan_fast_connect/example_wlan_fast_connect.c"),
		join(FRAMEWORK_DIR, "component/common/example/wlan_scenario/example_wlan_scenario.c"),
		join(FRAMEWORK_DIR, "component/common/example/websocket/example_wsclient.c"),
		join(FRAMEWORK_DIR, "component/common/example/xml/example_xml.c"),
		join(FRAMEWORK_DIR, "component/common/example/uart_firmware_update/example_uart_update.c"),
		join(FRAMEWORK_DIR, "component/common/network/httpc/httpc_tls.c"),
		join(FRAMEWORK_DIR, "component/common/network/httpd/httpd_tls.c"),   
		join(FRAMEWORK_DIR, "component/common/utilities/cJSON.c"),
		join(FRAMEWORK_DIR, "component/common/utilities/http_client.c"),
		join(FRAMEWORK_DIR, "component/common/utilities/uart_socket.c"),
		join(FRAMEWORK_DIR, "component/common/utilities/webserver.c"),
		join(FRAMEWORK_DIR, "component/common/utilities/xml.c"),
		]
# "env.subst" nes be jo BUILD_DIR isskleistu kaip "$PROJECTBUILD_DIR/$PIOENV"
libs= []
'''
libs.append(env.StaticLibrary(
	env.subst(join("$BUILD_DIR", "FrameworkAmeba")),
	env["AMEBA_SOURCES"]
	)
)
'''
"""
libs.append(env.BuildLibrary(
	join("$BUILD_DIR", "FrameworkAmeba"),
	join(FRAMEWORK_DIR, "component")
	)
)
"""
'''
env.Prepend(LIBS=libs)
'''
