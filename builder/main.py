import sys
from os.path import basename, join
from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default, DefaultEnvironment)
from platformio import util

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-sdk-ameba-v4.0b-gcc")
BOOTALL_BIN = FRAMEWORK_DIR + "/component/soc/realtek/8711b/misc/bsp/image/boot_all.bin"

AMEBA_TOOLDIR = join(FRAMEWORK_DIR, "component/soc/realtek/8711b/misc/iar_utility/common/tools")
FLASH_TOOLDIR = join(FRAMEWORK_DIR, "component/soc/realtek/8195a/misc/gcc_utility")
FLASHDOWNLOAD_TOOLDIR = join(FRAMEWORK_DIR, "component/soc/realtek/8711b/misc/gnu_utility/flash_download/image")
DEBUG_TOOLDIR = join(FRAMEWORK_DIR, "component/soc/realtek/8711b/misc/gcc_utility")
PROJECTINCLUDE_DIR = util.get_projectinclude_dir()

# CIA IS PLATFORMIO.INI "upload_flags"
#print(env["UPLOAD_FLAGS"])

env["AMEBA_SOURCES"] = []
env["CPPPPATH"] = []

CPPPATH = [
	PROJECTINCLUDE_DIR,
	FRAMEWORK_DIR + "/component/os/freertos",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/include",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/portable/GCC/ARM_CM4F",
	FRAMEWORK_DIR + "/component/os/os_dep/include",
	FRAMEWORK_DIR + "/component/common/api/network/include",
	FRAMEWORK_DIR + "/component/common/api",
	FRAMEWORK_DIR + "/component/common/api/at_cmd",
	FRAMEWORK_DIR + "/component/common/api/platform",
	FRAMEWORK_DIR + "/component/common/api/wifi",
	FRAMEWORK_DIR + "/component/common/api/wifi/rtw_wpa_supplicant/src",
	FRAMEWORK_DIR + "/component/common/api/wifi/rtw_wowlan",
	FRAMEWORK_DIR + "/component/common/api/wifi/rtw_wpa_supplicant/wpa_supplicant",
	FRAMEWORK_DIR + "/component/common/application",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTClient",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket",
	FRAMEWORK_DIR + "/component/common/example",
	FRAMEWORK_DIR + "/component/common/example/wlan_fast_connect",
	FRAMEWORK_DIR + "/component/common/drivers/modules",
	FRAMEWORK_DIR + "/component/common/drivers/sdio/realtek/sdio_host/inc",
	FRAMEWORK_DIR + "/component/common/drivers/inic/rtl8711b",
	FRAMEWORK_DIR + "/component/common/drivers/usb_class/device",
	FRAMEWORK_DIR + "/component/common/drivers/usb_class/device/class",
	FRAMEWORK_DIR + "/component/common/drivers/wlan/realtek/include",
	FRAMEWORK_DIR + "/component/common/drivers/wlan/realtek/src/osdep",
	FRAMEWORK_DIR + "/component/common/drivers/wlan/realtek/src/hci",
	FRAMEWORK_DIR + "/component/common/drivers/wlan/realtek/src/hal",
	FRAMEWORK_DIR + "/component/common/drivers/wlan/realtek/src/hal/rtl8711b",
	FRAMEWORK_DIR + "/component/common/drivers/wlan/realtek/src/hal/OUTSRC",
	FRAMEWORK_DIR + "/component/common/drivers/wlan/realtek/wlan_ram_map/rom",
	FRAMEWORK_DIR + "/component/common/file_system",
	FRAMEWORK_DIR + "/component/common/network",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/port/realtek/freertos",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/include",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/include/lwip",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/include/ipv4",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/port/realtek",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/include",
	FRAMEWORK_DIR + "/component/common/network/ssl/ssl_ram_map/rom",
	FRAMEWORK_DIR + "/component/common/test",
	FRAMEWORK_DIR + "/component/common/utilities",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/app/monitor/include",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/cmsis",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/cmsis/device",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/include",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/crypto",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/rom_lib",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/swlib/os_dep/include",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/swlib/std_lib/include",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/swlib/std_lib/libc/include",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/swlib/std_lib/libc/rom/string",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/swlib/std_lib/libgcc/rtl8195a/include",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/swlib/rtl_lib",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/misc",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/misc/os",
	FRAMEWORK_DIR + "/component/common/mbed/api",
	FRAMEWORK_DIR + "/component/common/mbed/hal",
	FRAMEWORK_DIR + "/component/common/mbed/hal_ext",
	FRAMEWORK_DIR + "/component/common/mbed/targets/cmsis",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b",
	FRAMEWORK_DIR + "/project/altek_8195a_gen_project/rtl8195a/sw/lib/sw_lib/mbed/api",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTClient",
	FRAMEWORK_DIR + "/component/common/network/websocket",
	]

LIBPATH= FRAMEWORK_DIR + "/component/soc/realtek/8711b/misc/bsp/lib/common/GCC"

LIBS=["_platform", "_wlan", "_wps", "_dct", "_rtlstd", "m", "c", "nosys", "gcc", "_websocket", "_http", "_mdns"]

LDSCRIPT_PATH= FRAMEWORK_DIR + "/project/realtek_amebaz_va0_example/GCC-RELEASE/rlx8711B-symbol-v02-img2_xip1.ld"

SOURCE_LIST = [
	env.subst("$PROJECTSRC_DIR") + "/main.c",
	FRAMEWORK_DIR + "/component/common/api/at_cmd/atcmd_lwip.c",
	FRAMEWORK_DIR + "/component/common/api/wifi/wifi_conf.c",
	FRAMEWORK_DIR + "/component/common/application/uart_adapter/uart_adapter.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/cmsis/device/app_start.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/startup.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/cmsis/device/system_8195a.c",
	FRAMEWORK_DIR + "/component/common/api/at_cmd/atcmd_sys.c",
	FRAMEWORK_DIR + "/component/common/api/at_cmd/atcmd_wifi.c",
	FRAMEWORK_DIR + "/component/common/api/at_cmd/log_service.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/app/monitor/ram/low_level_io.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/app/monitor/ram/monitor.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/app/monitor/ram/rtl_consol.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/app/monitor/ram/rtl_trace.c",
	FRAMEWORK_DIR + "/component/common/api/wifi/rtw_wpa_supplicant/wpa_supplicant/wifi_eap_config.c",
	FRAMEWORK_DIR + "/component/common/api/wifi/rtw_wpa_supplicant/wpa_supplicant/wifi_wps_config.c",
	FRAMEWORK_DIR + "/component/common/api/wifi/wifi_ind.c",
	FRAMEWORK_DIR + "/component/common/api/wifi/wifi_promisc.c",
	FRAMEWORK_DIR + "/component/common/api/wifi/wifi_simple_config.c",
	FRAMEWORK_DIR + "/component/common/api/wifi/wifi_util.c",
	FRAMEWORK_DIR + "/component/common/api/lwip_netconf.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTClient/MQTTClient.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTConnectClient.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTConnectServer.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTDeserializePublish.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTFormat.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTClient/MQTTFreertos.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTPacket.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTSerializePublish.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTSubscribeClient.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTSubscribeServer.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTUnsubscribeClient.c",
	FRAMEWORK_DIR + "/component/common/application/mqtt/MQTTPacket/MQTTUnsubscribeServer.c",
	FRAMEWORK_DIR + "/component/common/api/network/src/ping_test.c",
	FRAMEWORK_DIR + "/component/common/utilities/ssl_client.c",
	FRAMEWORK_DIR + "/component/common/utilities/tcptest.c",
	FRAMEWORK_DIR + "/component/common/api/network/src/wlan_network.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/api/api_lib.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/api/api_msg.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/api/err.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/api/netbuf.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/api/netdb.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/api/netifapi.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/api/sockets.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/api/tcpip.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/autoip.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/icmp.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/igmp.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/inet.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/inet_chksum.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/ip.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/ip_addr.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/ipv4/ip_frag.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/def.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/dhcp.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/dns.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/init.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/lwip_timers.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/mem.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/memp.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/netif.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/pbuf.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/raw.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/stats.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/sys.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/tcp.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/tcp_in.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/tcp_out.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/core/udp.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/src/netif/etharp.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/port/realtek/freertos/ethernetif.c",
	FRAMEWORK_DIR + "/component/common/drivers/wlan/realtek/src/osdep/lwip_intf.c",
	FRAMEWORK_DIR + "/component/common/network/lwip/lwip_v1.4.1/port/realtek/freertos/sys_arch.c",
	FRAMEWORK_DIR + "/component/common/network/websocket/wsclient_tls.c", 
	FRAMEWORK_DIR + "/component/common/network/dhcp/dhcps.c",
	FRAMEWORK_DIR + "/component/common/network/sntp/sntp.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/aesni.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/blowfish.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/camellia.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ccm.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/certs.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/cipher.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/cipher_wrap.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/debug.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ecp_ram.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/entropy.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/entropy_poll.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/error.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/gcm.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/havege.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/md2.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/md4.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/memory_buffer_alloc.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/net.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/padlock.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pbkdf2.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pkcs11.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pkcs12.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pkcs5.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/pkparse.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/platform.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ripemd160.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_cache.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_ciphersuites.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_cli.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_srv.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/ssl_tls.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/threading.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/timing.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/version.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/version_features.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509_create.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509_crl.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509_crt.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509_csr.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509write_crt.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/x509write_csr.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/polarssl-1.3.8/library/xtea.c",
	FRAMEWORK_DIR + "/component/common/network/ssl/ssl_ram_map/ssl_ram_map.c",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/portable/MemMang/heap_5.c",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/portable/GCC/ARM_CM4F/port.c",
	FRAMEWORK_DIR + "/component/os/freertos/cmsis_os.c",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/croutine.c",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/event_groups.c",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_service.c",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/list.c",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/queue.c",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/tasks.c",
	FRAMEWORK_DIR + "/component/os/freertos/freertos_v8.1.2/Source/timers.c",
	FRAMEWORK_DIR + "/component/os/os_dep/device_lock.c",
	FRAMEWORK_DIR + "/component/os/os_dep/osdep_service.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/analogin_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/dma_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/efuse_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/flash_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/gpio_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/gpio_irq_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/i2c_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/i2s_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/nfc_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/pinmap.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/pinmap_common.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/port_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/pwmout_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/rtc_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/serial_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/sleep.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/spi_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/sys_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/timer_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/us_ticker.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/us_ticker_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/wait_api.c",
	FRAMEWORK_DIR + "/component/common/mbed/targets/hal/rtl8711b/wdt_api.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_dsleepcfg.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_dstandbycfg.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_intfcfg.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/misc/rtl8710b_ota.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_pinmapcfg.c",
	FRAMEWORK_DIR + "/component/soc/realtek/8711b/fwlib/ram_lib/rtl8710b_sleepcfg.c",
	FRAMEWORK_DIR + "/component/common/example/bcast/example_bcast.c",
	FRAMEWORK_DIR + "/component/common/example/dct/example_dct.c",
	FRAMEWORK_DIR + "/component/common/example/eap/example_eap.c",
	FRAMEWORK_DIR + "/component/common/example/example_entry.c",
	FRAMEWORK_DIR + "/component/common/example/get_beacon_frame/example_get_beacon_frame.c",
	FRAMEWORK_DIR + "/component/common/example/high_load_memory_use/example_high_load_memory_use.c",
	FRAMEWORK_DIR + "/component/common/example/http_client/example_http_client.c",
	FRAMEWORK_DIR + "/component/common/example/httpc/example_httpc.c",
	FRAMEWORK_DIR + "/component/common/example/httpd/example_httpd.c",
	FRAMEWORK_DIR + "/component/common/example/http_download/example_http_download.c",
	FRAMEWORK_DIR + "/component/common/example/mcast/example_mcast.c",
	FRAMEWORK_DIR + "/component/common/example/mdns/example_mdns.c",
	FRAMEWORK_DIR + "/component/common/example/mqtt/example_mqtt.c",
	FRAMEWORK_DIR + "/component/common/example/nonblock_connect/example_nonblock_connect.c",
	FRAMEWORK_DIR + "/component/common/example/rarp/example_rarp.c",
	FRAMEWORK_DIR + "/component/common/example/sntp_showtime/example_sntp_showtime.c",
	FRAMEWORK_DIR + "/component/common/example/socket_select/example_socket_select.c",
	FRAMEWORK_DIR + "/component/common/example/ssl_download/example_ssl_download.c",
	FRAMEWORK_DIR + "/component/common/example/ssl_server/example_ssl_server.c",
	FRAMEWORK_DIR + "/component/common/example/tcp_keepalive/example_tcp_keepalive.c",
	FRAMEWORK_DIR + "/component/common/example/uart_atcmd/example_uart_atcmd.c",
	FRAMEWORK_DIR + "/component/common/example/wifi_mac_monitor/example_wifi_mac_monitor.c",
	FRAMEWORK_DIR + "/component/common/example/wlan_fast_connect/example_wlan_fast_connect.c",
	FRAMEWORK_DIR + "/component/common/example/wlan_scenario/example_wlan_scenario.c",
	FRAMEWORK_DIR + "/component/common/example/websocket/example_wsclient.c",
	FRAMEWORK_DIR + "/component/common/example/xml/example_xml.c",
	FRAMEWORK_DIR + "/component/common/example/uart_firmware_update/example_uart_update.c",
	FRAMEWORK_DIR + "/component/common/network/httpc/httpc_tls.c",
	FRAMEWORK_DIR + "/component/common/network/httpd/httpd_tls.c", 
	FRAMEWORK_DIR + "/component/common/utilities/cJSON.c",
	FRAMEWORK_DIR + "/component/common/utilities/http_client.c",
	FRAMEWORK_DIR + "/component/common/utilities/uart_socket.c",
	FRAMEWORK_DIR + "/component/common/utilities/webserver.c",
	FRAMEWORK_DIR + "/component/common/utilities/xml.c",
	]

OBJECT_LIST = SOURCE_LIST
OBJECT_LIST = [value.replace('.c','.o') for value in OBJECT_LIST]

env.Replace(

	PICK = join(AMEBA_TOOLDIR, "pick"),
	PAD  = join(AMEBA_TOOLDIR, "padding"),
	CHKSUM = join(AMEBA_TOOLDIR, "checksum"),
	OTA = join(AMEBA_TOOLDIR, "ota"),

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

def compiler(target, source, env):
	global CPPPATH
	prefix = "-I"
	CPPPATH = [prefix + s for s in CPPPATH]
	for i in range(len(OBJECT_LIST)):
# NEINA ATSAUKT SU CTRL + C
		Execute(env.VerboseAction(env.subst("$CC $CFLAGS %s -c %s -o %s" % (' '.join(CPPPATH), SOURCE_LIST[i], OBJECT_LIST[i])), "Compiling %s" % OBJECT_LIST[i]))

def pre_linker(env):
	global LIBS
	prefix = "-l"
	LIBS = [prefix + s for s in LIBS]
	return LIBS

def replace_rtl(env):
	with open("%s/openocd/scripts/_rtl_gdb_flash_write.txt" % FRAMEWORK_DIR, "rt") as fin:
		with open("%s/openocd/scripts/rtl_gdb_flash_write.txt" % FRAMEWORK_DIR, "wt") as fout:
			for line in fin:
				fout.write(line.replace('BUILD_DIR', '%s' % env.subst(env["BUILD_DIR"])).replace('SCRIPTS_DIR', '%s/openocd/scripts' % FRAMEWORK_DIR))

compiling = [
	compiler,
#	env.VerboseAction("$CC -c %s -o %s" % ("$SOURCES", "$TARGET"), "Compiling $TARGET")
	]

linking = [
	env.VerboseAction("$LD $LINKFLAGS -o $TARGET %s $BUILD_DIR/boot_all.o -L%s %s -T%s" % (' '.join(OBJECT_LIST), LIBPATH, ' '.join(pre_linker(env)), LDSCRIPT_PATH), "Linking $TARGET")
	]

prerequirement = [
	env.VerboseAction("chmod 777 %s" % BOOTALL_BIN, "Executing prerequirements"),
	env.VerboseAction("$OBJCOPY -I binary -O elf32-littlearm -B arm %s $BUILD_DIR/boot_all.o" % BOOTALL_BIN, "Generating $TARGET"),
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
	env.VerboseAction('echo -n "set $$" > %s/openocd/scripts/BTAsize.gdb' % FRAMEWORK_DIR, 'Uploading binary'),
	env.VerboseAction('echo "BOOTALLFILESize = 0x$$(echo "obase=16; $$(stat -c %%s %s)"|bc)" >> %s/openocd/scripts/BTAsize.gdb' % (BOOTALL_BIN, FRAMEWORK_DIR), '.'),
	env.VerboseAction('echo -n "set $$" > %s/openocd/scripts/fwsize.gdb' % FRAMEWORK_DIR, '.'),
	env.VerboseAction('echo "RamFileSize = 0x$$(echo "obase=16; $$(stat -c %%s $BUILD_DIR/image2_all_ota1.bin)"|bc)" >> %s/openocd/scripts/fwsize.gdb' % FRAMEWORK_DIR, '.'),
	replace_rtl(env),
	env.VerboseAction('cp %s $BUILD_DIR/boot_all.bin' % BOOTALL_BIN, '.'),
	env.VerboseAction('export FRAMEWORK_DIR="%s"; sh %s/openocd/scripts/openocd.sh' % (FRAMEWORK_DIR, FRAMEWORK_DIR), '.'),
	]

env.Append(
	BUILDERS = dict(
		Prerequirement = Builder(
			action = env.VerboseAction(prerequirement, "Executing prerequirements")),
		Linker = Builder(
			action = env.VerboseAction(linking, "Linker")),
		Compiler = Builder(
			action = env.VerboseAction(compiling, "Compiler")),
		Manipulate = Builder(
			action = env.VerboseAction(manipulating, "Manipulating images")),
		)
)
prerequirement_b = env.Prerequirement(("$BUILD_DIR/boot_all.o"), (BOOTALL_BIN))
compiler_b = env.Compiler(OBJECT_LIST, SOURCE_LIST)
linker_b = env.Linker("$BUILD_DIR/program.axf", [prerequirement_b, compiler_b])
manipulate_images_b = env.Manipulate("$BUILD_DIR/image2_all_ota1.bin", linker_b)
#env.AddPreAction(prerequirement_b, "ls")
#build = Program("$BUILD_DIR/program.axf", [SOURCE_LIST, "$BUILD_DIR/boot_all.o"])

upload = env.Alias("upload", [manipulate_images_b, BOOTALL_BIN], uploading)

#AlwaysBuild(upload)

Default([manipulate_images_b])

#alla = Object(SOURCE_LIST)
#Default(alla)

#def Program(env, target, source):
#   env.Program(target, source.split())

