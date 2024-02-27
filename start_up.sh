#!/bin/bash

. /etc/profile

start_up() {
  sleep 1
  REAL_SERVICE_NAME="$1"
  SERVICE_NAME="${REAL_SERVICE_NAME}_service"
  GUNICORN_CMD="venv/bin/python venv/bin/gunicorn"
  START_CMD="${GUNICORN_CMD} -c ${WORKSPACE}/${SERVICE_NAME}/resources/gunicorn.py starter:starter_hosting(service_name=\"${REAL_SERVICE_NAME}\")"

  if [[ $? == 0 ]]; then
    echo "ready to start the ${SERVICE_NAME}..."
    echo "begin to execute ${START_CMD}"
    [ -e ${WORKSPACE}/${SERVICE_NAME}/logs ] || mkdir -pv ${WORKSPACE}/${SERVICE_NAME}/logs
    nohup ${START_CMD} > "${WORKSPACE}"/"${SERVICE_NAME}"/logs/catalina.out 2>&1 &
    echo "success!"
  else
    echo "start up failed!"
  fi
}

echo "check then venv..."
HOME_PATH="${HOME}"
PIP_CONFIG_PATH="${HOME_PATH}/.pip"
if [[ ! -d ${PIP_CONFIG_PATH} ]]; then
  mkdir -p "${PIP_CONFIG_PATH}"

  PIP_CONFIG_FILE_PATH="${PIP_CONFIG_PATH}/pip.conf"
  if [[ ! -f ${PIP_CONFIG_FILE_PATH} ]]; then
    touch "${PIP_CONFIG_FILE_PATH}"
    cat > "${PIP_CONFIG_FILE_PATH}" << EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
extra-index-url = https://pypi.org/simple/
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
EOF
  fi
fi

#PYTHON_DEPENDENCY="python3-devel.x86_64"
#CHECK_PYTHON_DEPENDENCY="$(yum list | grep ${PYTHON_DEPENDENCY})"
#if [[ -z "${CHECK_PYTHON_DEPENDENCY}" ]]; then
#redhat/centos/rocky
#  su - root -c "yum install -y python3-devel"
#debian/ubuntu/deepin
#  su - root -c "apt install -y python3-dev"
#fi

#MYSQL_DEPENDENCY="mariadb-devel.x86_64"
#CHECK_MYSQL_DEPENDENCY="$(yum list | grep ${MYSQL_DEPENDENCY})"
#if [[ -z ${CHECK_MYSQL_DEPENDENCY} ]]; then
# redhat/centos/rocky
#  su - root -c "yum install -y mysql-devel"
# debian/ubuntu/deepin
#  su - root -c "apt install -y libmariadb-dev"
#fi

WORKSPACE="$(pwd)"
if [ ! -d "${WORKSPACE}/venv" ]; then
  /usr/bin/env python3.8 -m venv venv
fi
REQUIREMENTS_PATH="${WORKSPACE}/requirements.txt"
echo "activate the venv..."
source ./venv/bin/activate &&
  venv/bin/python -m pip install --upgrade pip &&
  venv/bin/pip install eventlet==0.33.3 &&
  venv/bin/pip install gunicorn==21.2.0 &&
  venv/bin/pip install -r "${REQUIREMENTS_PATH}"
echo "activated!"

if [[ $# -le 0 ]]; then
  echo "Usage:	bash start_up.sh [service_name]"
  SERVICE_LIST="$(venv/bin/python starter.py service --query_all)"
  echo "${SERVICE_LIST}"
  venv/bin/python
  exit 1
fi

echo "正在终止原始程序..."
SERVICE_PID_FILE="${WORKSPACE}/$1_service/$1_service.pid"
if [[ -f ${SERVICE_PID_FILE} ]]; then
  PID=$(cat ${SERVICE_PID_FILE})
  kill -HUP ${PID}
  echo "Service restart is completed!"
else
  echo "未检索到相关服务。"
  start_up "$@"
fi
