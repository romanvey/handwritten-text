cp -r src/contrib/ src/deploy/app
cd src/deploy/app && PYTHONPATH=../../ /home/roman/miniconda3/envs/ds/bin/python -m gunicorn.app.wsgiapp -b 0.0.0.0:80 app
cd -
rm -rf src/deploy/app/contrib