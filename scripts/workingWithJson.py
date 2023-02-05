import json
import scripts.logger as log
log.Logging()

@log.logger.catch()
def read_json(path: str):
    with open(path, 'r', encoding='utf-8') as file: return json.load(file)

@log.logger.catch()
def write_json(path: str, var: list or dict):
    with open(path, 'w', encoding='utf8') as file: json.dump(var, file, indent='\t', ensure_ascii=False)