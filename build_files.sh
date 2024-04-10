echo "BUILD START"
python install -r requirements.txt
python3.9 manage.py collectstatic --noinput
echo "BUILD END"
