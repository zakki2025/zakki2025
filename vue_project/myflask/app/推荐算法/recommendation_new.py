import pandas as pd
import numpy as np
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split, GridSearchCV, cross_validate
from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, SVD, SVDpp, NMF
from surprise import accuracy
from sentence_transformers import SentenceTransformer, util
import warnings
warnings.filterwarnings('ignore')

def get_final_recommendations(UserID, user_meal_scene, user_focus_point):
    # 加载并准备数据
    file_path = 'myflask\\app\推荐算法\MealRating.csv'
    df = pd.read_csv(file_path)
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    data = df[['UserID', 'MealID', 'Rating']].dropna()

    # 创建 Surprise 读取器和数据集
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(data, reader)

    # 评估不同算法
    def evaluate_algorithms(data):
        algorithms = {
            'KNNBasic': KNNBasic(),
            'KNNWithMeans': KNNWithMeans(),
            'KNNWithZScore': KNNWithZScore(),
            'SVD': SVD(),
            'SVDpp': SVDpp(),
            'NMF': NMF()
        }
        results = {}
        for name, algo in algorithms.items():
            cv_results = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=False)
            results[name] = {
                'RMSE': cv_results['test_rmse'].mean(),
                'MAE': cv_results['test_mae'].mean()
            }
        return results

    # 优化 SVD 参数
    def optimize_svd_params(data):
        param_grid = {
            'n_epochs': [20, 30, 40],
            'lr_all': [0.005, 0.01],
            'reg_all': [0.02, 0.1, 0.4]
        }
        gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=5)
        gs.fit(data)
        return gs.best_score['rmse'], gs.best_params['rmse']

    # 使用最佳参数训练最终模型
    def train_final_model(data, best_params):
        trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
        algo = SVD(
            n_epochs=best_params['n_epochs'],
            lr_all=best_params['lr_all'],
            reg_all=best_params['reg_all']
        )
        algo.fit(trainset)
        predictions = algo.test(testset)
        return algo, accuracy.rmse(predictions), accuracy.mae(predictions)

    # 为特定用户获取前N个推荐
    def get_top_n_recommendations(algo, user_id, n=5):
        user_ratings = df[df['UserID'] == user_id]['MealID'].unique()
        all_items = df['MealID'].unique()
        items_to_predict = np.setdiff1d(all_items, user_ratings)
        predictions = []
        for item_id in items_to_predict:
            pred = algo.predict(user_id, item_id)
            predictions.append((item_id, pred.est))
        predictions.sort(key=lambda x: x[1], reverse=True)
        top_n = predictions[:n]
        recommended_meals = []
        for meal_id, pred_rating in top_n:
            meal_info = df[df['MealID'] == meal_id].iloc[0]
            recommended_meals.append({
                'MealID': meal_id,
                'MealName': meal_info['mealName'],
                'MealType': meal_info['mealType'],
                'MealPrice': meal_info['mealPrice'],
                'PredictedRating': round(pred_rating, 2)
            })
        return recommended_meals

    # 运行优化过程
    results = evaluate_algorithms(dataset)
    best_rmse, best_params = optimize_svd_params(dataset)
    final_algo, final_rmse, final_mae = train_final_model(dataset, best_params)
    recommendations = get_top_n_recommendations(final_algo, UserID, n=5)

    # 读取店铺信息并转换数值列为合适的类型
    file_path_shop_info = 'myflask\\app\推荐算法\店铺标签_更新2.xlsx'
    df_shop_info = pd.read_excel(file_path_shop_info)
    numeric_columns = ['口味分', '服务分', '环境分', '总分']
    df_shop_info[numeric_columns] = df_shop_info[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # 读取菜品描述数据
    file_path_meal_descriptions = 'myflask\\app\推荐算法\阿里云菜品描述.xlsx'
    df_meal_descriptions = pd.read_excel(file_path_meal_descriptions)
    meal_description_map = df_meal_descriptions.set_index('菜品名称')['菜品描述'].to_dict()

    # 获取推荐菜品的描述并构建用户输入信息
    user_food_descriptions = [meal_description_map.get(rec['MealName'], "无法找到该菜品的描述") for rec in recommendations]

    # 加载预训练的SBERT模型
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 定义计算相似度的函数
    def calc_food_similarity(shop_description, user_description):
        if pd.isna(shop_description):
            return 0.0
        shop_embedding = model.encode(shop_description, convert_to_tensor=True)
        user_embedding = model.encode(user_description, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(shop_embedding, user_embedding)
        return float(cosine_scores[0]) * 10

    def calc_scene_similarity(scene_tags, user_scene):
        if pd.notna(scene_tags) and user_scene in scene_tags:
            return 1
        else:
            return 0

    def calc_focus_similarity(focus_score, focus_point):
        if pd.notna(focus_score) and focus_score > 4:
            return 1
        else:
            return 0

    def calc_overall_score(total_score):
        if pd.isna(total_score):
            return 0
        elif total_score > 4.5:
            return 1
        elif total_score > 4.3:
            return 0.5
        else:
            return 0

    # 计算每个描述与所有店铺的【菜品相似度得分】，并保留前20个店铺
    top_shops_per_description = {}
    for description in user_food_descriptions:
        df_shop_info['菜品相似度得分'] = df_shop_info['店铺描述'].apply(lambda x: calc_food_similarity(x, description))
        top_20_shops = df_shop_info.nlargest(20, '菜品相似度得分').copy()
        top_shops_per_description[description] = top_20_shops

    # 对每个描述中的20个店铺进行后续计算，并选出推荐分最高的店铺
    recommended_shops = []
    for description, top_20_shops in top_shops_per_description.items():
        top_20_shops['场景相似度得分'] = top_20_shops.apply(lambda row: calc_scene_similarity(str(row['场景标签']), user_meal_scene), axis=1)
        top_20_shops['关注点相似度得分'] = top_20_shops.apply(lambda row: calc_focus_similarity(row[user_focus_point + '分'], user_focus_point), axis=1)
        top_20_shops['总体评分'] = top_20_shops.apply(lambda row: calc_overall_score(row['总分']), axis=1)
        top_20_shops['推荐分'] = (
            top_20_shops['菜品相似度得分'] * 0.4 +
            top_20_shops['场景相似度得分'] * 0.4 +
            top_20_shops['关注点相似度得分'] * 0.5 +
            top_20_shops['总体评分'] * 0.1
        )
        best_shop = top_20_shops.nlargest(1, '推荐分')
        recommended_shops.append(best_shop[['店铺名称', '菜品相似度得分', '场景相似度得分', '关注点相似度得分', '总体评分', '推荐分']])

    # 合并推荐结果并去重，选取最终推荐的5个店铺
    final_recommendations = pd.concat(recommended_shops).drop_duplicates(subset=['店铺名称']).nlargest(5, '推荐分')
    result1 = final_recommendations[['店铺名称', '菜品相似度得分', '场景相似度得分', '关注点相似度得分', '总体评分', '推荐分']]
    result2 = pd.DataFrame(result1)
    result_list = result2.to_dict(orient='records')
    print(result_list)

    return result_list

# 示例调用
#UserID = 1
#user_meal_scene = "家庭聚餐"
#user_focus_point = "口味"
#print(get_final_recommendations(UserID, user_meal_scene, user_focus_point))