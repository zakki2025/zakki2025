import warnings
import pandas as pd
warnings.filterwarnings('ignore')

def get_final_recommendations(UserID, user_meal_scene, user_focus_point):
    if not UserID or not user_meal_scene or not user_focus_point:
        return None  # 或者返回一个错误消息，例如：return "参数不能为空"
    
    data1 = {
    '店铺名称': ['店铺A', '店铺B', '店铺C', '店铺D', '店铺E'],
    '菜品相似度得分': [0.85, 0.90, 0.75, 0.80, 0.95],
    '场景相似度得分': [0.70, 0.80, 0.75, 0.85, 0.90],
    '关注点相似度得分': [0.80, 0.85, 0.70, 0.75, 0.90],
    '总体评分': [4.5, 4.7, 4.3, 4.6, 4.8],
    '推荐分': [85, 90, 75, 80, 95]
    }
    data2 = pd.DataFrame(data1)
    result = data2.to_dict(orient='records')

    return result


# 示例调用
#UserID = 1
#user_meal_scene = "家庭聚餐"
#user_focus_point = "口味"
#print(get_final_recommendations(UserID, user_meal_scene, user_focus_point))
