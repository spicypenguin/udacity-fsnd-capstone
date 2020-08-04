sudo -u postgres dropdb castingagency-test
sudo -u postgres createdb castingagency-test
cd src && python test_app.py