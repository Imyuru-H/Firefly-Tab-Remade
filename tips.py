"""
This file use to storage searching input placeholder.
"""

tips = ["主人今天要搜些什么呢喵~?",
        "今天天气真好啊喵~（伸懒腰）",
        "主人~我饿了喵~"]

errors = {
    # 4xx错误 (客户端错误)
    400 : "主人你输入了什么啊喵, 人家听不懂呢~ ( http 400 error )",
    401 : "人家不认识你喵, 快走开啊喵~ ( http 401 error )",
    403 : "想要? 真是杂鱼呢~, 不给你喵~ ( http 403 error )",
    404 : "这个东西...人家找不到呢喵~ ( http 404 error )",
    405 : "这样不可以啊喵! ( http 405 error )",
    
    # 5xx错误 (服务器错误)
    500 : "主人...人家觉得自己闯祸了喵... ( http 500 error )",
    501 : "这个人家做不到哦喵~ ( http 501 error )",
    502 : "主人...人家感觉自己要死掉了喵... ( http 502 error )",
    503 : "主人...人家好累啊喵... ( http 503 error )",
    504 : "主人, 这个人家想不出来喵~ ( http 504 error )",
    505 : "主人, 这个人家看不懂喵~ ( http 505 error )"
}