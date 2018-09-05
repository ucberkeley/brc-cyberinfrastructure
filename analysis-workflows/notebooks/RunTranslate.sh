module load python/3.6
source activate translate2
export PYTHONIOENCODING="utf-8"

while true; do
python GoogleTranslateAPI.py
sleep 60
done
