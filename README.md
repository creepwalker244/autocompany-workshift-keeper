# autocompany-workshift-keeper
пример сервиса контроля рабочего времени

## локальное развертывание:

### 1. создаем виртуальную среду выполнения пайтон.
python3 -m venv .venv

cd .venv/Scripts

activate

### 2. устанавливаем в актвиированную виртуальную среду зависимости
pip install -r requirements.txt


### 3. локальный запуск
uvicorn app:app --reload

или в unix среде:
bash run.sh
