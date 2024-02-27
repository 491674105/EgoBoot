#!/bin/bash

. /etc/profile

shutdown() {
  echo "正在终止原始程序..."
  WORKSPACE=$(pwd)
  SERVICE_PID_FILE="${WORKSPACE}/$1_service/$1_service.pid"
  if [[ -f ${SERVICE_PID_FILE} ]]; then
    PID=$(cat ${SERVICE_PID_FILE})
    kill -TERM ${PID}
    echo "等待服务下线"
    KILL_TIME_OUT=0
    for (( ; ; )); do
      sleep 1
      KILL_TIME_OUT=$((KILL_TIME_OUT + 1))
      echo -n "."
      HIS_PID="$(ps -aux | grep "service_name=\"$1\"" | grep -Ev "(grep|start_up)" | awk '{print $2}')"
      if [[ -z ${HIS_PID} ]]; then
        echo " "
        echo "服务已下线！"
        break
      elif [[ ${KILL_TIME_OUT} -ge 300 ]]; then
        echo " "
        echo "下线异常！"
        exit 0
      fi
    done
  else
    echo "未检索到相关服务。"
  fi
}

main() {
  if [[ $# -gt 0 ]]; then
    shutdown "$@"
  else
    echo "Usage:	bash shutdown.sh [service_name]"
  fi
}

main "$@"
