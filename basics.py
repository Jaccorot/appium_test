# coding=utf-8
import random
TEST_TYPE = "TEST"

TEMPLATE_TYPE = ["单图", "多图", "文字", "表单", "封面"]
PHOTO_TYPE = ["本地", "图片库", "我的"]
MUSIC_TYPE = ["手机", "音乐库", "我的"]
FLIP_TYPE = ["上下翻页", "上下惯性翻页", "左右惯性翻页", "左右翻页", "左右连续翻页", "立体翻页", "卡片翻页", "放大翻页", "交换翻页"]
SERVER_SWITCHED_FLAG = False
SCENE_BASIC_SETTING = {
    # "name": "name test",
    # "details": "details test",
    "cover": {
        "type": random.choice(PHOTO_TYPE),
        "preview": 1
    },
    # "music": {
    #     "type": random.choice(MUSIC_TYPE)
    # },
    # "flip": random.choice(FLIP_TYPE)
}


if TEST_TYPE == "ONLINE":
    BASIC_USER = {
        "username": "apptest_1@eqxiu.com",
        "psw": "aaa123",
    }
elif TEST_TYPE == "TEST":
    BASIC_USER = {
        "username": "apptest_1@eqxiu.com",
        "psw": "aaa123",
    }
elif TEST_TYPE == "PRE":
    pass
else: #develop
    pass