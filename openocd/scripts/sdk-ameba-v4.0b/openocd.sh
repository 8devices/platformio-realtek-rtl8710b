openocd -f interface/cmsis-dap.cfg \
        -f $PLATFORM_DIR/openocd/scripts/$FRAMEWORK/amebaz.cfg \
        -c "init" &

export ocdpid=$!

arm-none-eabi-gdb --init-eval-command="dir  $PLATFORM_DIR/openocd/scripts/$FRAMEWORK" -x $PLATFORM_DIR/openocd/scripts/$FRAMEWORK/rtl_gdb_flash_write.txt

kill -9 $ocdpid
