#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Must provide \"command\""
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <command>"
  exit 1
fi

COMMAND=$1

if [ "$COMMAND" != "build" ] && [ "$COMMAND" != "run" ]; then
  echo "Valid commands are \"build\" and \"run\""
  echo "You passed $COMMAND"
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <command>"
  exit 1
fi

# OPENTRONS_HARDWARE is an env variable that is passed to every container

FULL_COMMAND="$COMMAND"-"$OPENTRONS_HARDWARE"
OTHER_ARGS=`echo "${@:2}"`

case $FULL_COMMAND in
  build-heater-shaker)
    (
      cd /opentrons-modules && \
      cmake --preset=stm32-host-gcc10 . && \
      cmake --build ./build-stm32-host --target heater-shaker-simulator
    )
    ;;
  run-heater-shaker)
    bash -c "/opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator $OTHER_ARGS"
    ;;
  build-thermocycler)
    (
      cd /opentrons-modules && \
      cmake --preset=stm32-host-gcc10 . && \
      cmake --build ./build-stm32-host --target thermocycler-refresh-simulator
    )
    ;;
  run-thermocycler)
    bash -c "/opentrons-modules/build-stm32-host/stm32-modules/thermocycler-refresh/simulator/thermocycler-refresh-simulator $OTHER_ARGS"
    ;;
  run-emulator-proxy)
    python3 -m opentrons.hardware_control.emulation.app
    ;;
  run-thermocycler-driver)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_module_emulator thermocycler $OTHER_ARGS"
    ;;
  run-tempdeck-driver)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_module_emulator tempdeck $OTHER_ARGS"
    ;;
  run-magdeck-driver)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_module_emulator magdeck $OTHER_ARGS"
    ;;
  run-robot-server)
    bash -c "uvicorn "robot_server:app" --host 0.0.0.0 --port 31950 --ws wsproto --reload"
    ;;
  build-ot3-firmware-echo)
    (
      cd /ot3-firmware && \
      cmake --preset host-gcc10 && \
      cmake --build ./build-host --target can-simulator
    )
    ;;
  run-ot3-firmware-echo)
    /ot3-firmware/build-host/can/simulator/can-simulator
    ;;
esac