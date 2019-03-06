#! /usr/bin/env bash


if [ -z "$REPO_ROOT" ]; then
    echo 'error: env var must be set.'
    echo 'If you execute this script from CLI, do `direnv allow` first.'
    exit 1
fi


source $REPO_ROOT/script/check_requirements.sh
check_requirements java


SIMULATOR_DIR=$REPO_ROOT/submodule/FightingICE


os_type=
case $(uname) in
    'Linux')
        os_type=linux
        ;;
    'Darwin')
        os_type=macos
        ;;
    *)
        echo "error: This OS is not supported"
        exit 1
        ;;
esac


classpath=$(echo $SIMULATOR_DIR/jar/FightingICE.jar $SIMULATOR_DIR/lib/* $SIMULATOR_DIR/lib/lwjgl/* $SIMULATOR_DIR/lib/natives/$os_type/* | tr ' ' : | sed 's/:$//')
# workaround:
#   Simulator requires current directory is simulator root.
#   If don't, raise an error like:
#     java.io.FileNotFoundException: ./data/characters/ZEN/gSetting.txt (No such file or directory)
cd $SIMULATOR_DIR
exec java -XstartOnFirstThread -cp $classpath Main --py4j $@
