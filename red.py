import os
import json
import random
import logging
import time,datetime

def parse_config_file(file_path):
    config_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                key, value = line.split('=')
                config_data[key.strip()] = value.strip()
    return config_data


def get_effect_data(directory, effect_list, effects, duration=500000):
    data_list = []

    if directory is None:
        directory = os.getcwd()

    # 读取effect.txt文件
    effect_file_path = os.path.join(os.getcwd(), 'effect.txt')
    with open(effect_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        effect_list = [line.strip() for line in lines]

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename == 'cache.json':
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)
                    if json_data.get('name') in effect_list and json_data.get('effect_id') in effects:
                        directory = directory.replace('\\', '/')
                        data = [{
                            "category_id": "",
                            "category_name": "",
                            "duration": duration,
                            "id": json_data.get('effect_id'),
                            "material_type": "sticker",
                            "name": json_data.get('name'),
                            "panel": "",
                            "path":  directory+'/'+json_data.get('effect_id')+'/'+json_data['file_url'].get('uri'),
                            "platform": "all",
                            "resource_id": json_data.get('resource_id'),
                            "start": 0,
                            "type": "in"
                        }]
                        data_list.append(data)

    return data_list

def main():
    # 配置日志记录
    log_file = os.path.join(os.getcwd(), 'program.log')
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        current_date = datetime.datetime.now()
        limit_date = datetime.datetime(2023, 7, 1)

        if current_date > limit_date:
            logging.warning("程序已过期，无法运行！请更新")
            print("程序已过期，无法运行！请更新")
        else:
            # 生成list对象
            effect_list = []

            # 读取配置文件获取路径
            config_file_path = os.path.join(os.getcwd(), 'config.txt')
            config_data = parse_config_file(config_file_path)
            effect_path = config_data.get('effect_path')
            project = config_data.get('project_path')
            duration = int(config_data.get('duration'))
            effects=[
                            "3138860",
                            "3114660",
                            "3704299",
                            "1661186",
                            "1719670",
                            "1715294",
                            "1714696",
                            "1722114",
                            "1639676",
                            "1643884",
                            "1488722",
                            "1644341",
                            "6492065",
                            "7080877",
                            "1644340",
                            "1644321",
                            "1644339",
                            "1644322",
                            "1644338",
                            "1644320",
                            "1644319",
                            "1644318",
                            "1644314",
                            "1644315",
                            "1644313",
                            "1644312",
                            "1644309",
                            "1644317",
                            "1644308",
                            "1644310",
                            "1644311",
                            "1644316",
                            "1558840",
                            "1644307",
                            "1644306",
                            "1644305",
                            "1644337",
                            "1644336",
                            "1644280",
                            "1644279",
                            "1644278",
                            "1644304",
                            "1644262",
                            "1644261",
                            "1644263",
                            "1644264",
                            "1644265",
                            "1644277",
                            "1644266",
                            "1644267",
                            "1644268",
                            "1644269",
                            "1644270",
                            "1644271",
                            "1644272",
                            "1644273",
                            "1644274",
                            "1644275",
                            "1644276",
                            "1644335"
                        ]
            # 获取符合条件的数据
            data_list = get_effect_data(effect_path, effect_list, effects, duration)

            draft_content = os.path.join(project, 'draft_content.json')
            with open(draft_content, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                material_animations = json_data['materials'].get('material_animations')
                chosen_data = []
                prev_chosen = None
                for index in range(len(material_animations)):
                    if data_list:
                        available_data = [data for data in data_list if data != prev_chosen]
                        if available_data:
                            chosen = random.choice(available_data)
                        else:
                            chosen = random.choice(data_list)
                        material_animations[index]['animations'] = chosen
                        chosen_data.append(chosen)
                        prev_chosen = chosen
                        data_list.remove(chosen)

            with open(draft_content, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4, sort_keys=True)

            logging.info('动画添加完成')
            print('动画添加完成')
            time.sleep(3)
            

    except Exception as e:
        logging.error("An error occurred: " + str(e))
        print("An error occurred:", str(e))
        time.sleep(10)

if __name__=="__main__":
    main()
    