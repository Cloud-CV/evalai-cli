echo Setting up EvalAI server. This may take some time

git clone --branch fix-docker-compose-dev https://github.com/nikochiko/EvalAI.git .travis-ci_tmp_evalai && cd .travis-ci_tmp_evalai
docker-compose up --build &

cd ..
i=0
while :
do
  if [ $i -gt 8 ]
  then
    echo ERROR: Timeout while trying to set up EvalAI server.
    exit 1
  fi
  if nc -z -w 1 127.0.0.1 8000 &> /dev/null
  then
    echo EvalAI server is up
    break
  fi
  sleep 1m 30s
  echo It may take up to 12 minutes to get the server started
  let i++
  echo Tries: $i
done

py.test --ignore=.travis-ci_tmp_evalai --cov . --cov-config .coveragerc
