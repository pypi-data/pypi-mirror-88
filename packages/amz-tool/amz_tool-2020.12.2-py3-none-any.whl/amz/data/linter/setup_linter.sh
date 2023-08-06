if [ ! -z $ZSH_NAME ] ; then
  LINTER_PATH_ALL="$( cd "$( dirname "$0" )" && pwd )"
elif [ ! -z $BASH ] ; then
  LINTER_PATH_ALL="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
else
  echo "Linter: Unsupported shell! Only bash and zsh supported at the moment!"
fi
LINTER_PATH=$(echo ${LINTER_PATH_ALL} | tr ' ' '\n' | tail -1)
export LINTER_PATH

export PATH="$PATH:$LINTER_PATH/bin"
