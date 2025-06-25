from flask import Blueprint, jsonify, request
from app.models import Shop
from app.schemas import shops_schema, chart_schema
from app.utils import make_response
from . import db
from sqlalchemy import func
from app.推荐算法.recommendation import get_final_recommendations

main = Blueprint('main', __name__)

# 评论TOP10店铺
@main.route('/commentsRank', methods=['GET'])
def get_top_shops():
    try:
        top_shops = Shop.query.order_by(Shop.评论数量.desc()).limit(10).all()
        result = shops_schema.dump(top_shops)
        return make_response(data=result)
    except Exception as e:
        return make_response(code=1, message=str(e))
    

@main.route('/numberRank', methods=['GET'])
def get_top_Rank():
    try:
        ret = db.session.query(Shop.标签.label('name'),
                               db.func.count(Shop.ROWID).label('value')).group_by(Shop.标签).order_by(db.desc('value')).limit(20).all()
        result = chart_schema.dump(ret)
        return make_response(data=result)
    except Exception as e:
        return make_response(code=1, message=str(e))

@main.route('/scoreradar', methods=['GET'])
def shop_radar_chart():
    try:
        # 使用SQLAlchemy查询数据库，计算每个指标的最大值、最小值、中位数、众数、平均值
        max_scores = db.session.query(
            func.max(Shop.评分).label('总评分_max'),
            func.max(Shop.口味).label('口味_max'),
            func.max(Shop.服务).label('服务_max'),
            func.max(Shop.环境).label('环境_max')
        ).first()

        min_scores = db.session.query(
            func.min(Shop.评分).label('总评分_min'),
            func.min(Shop.口味).label('口味_min'),
            func.min(Shop.服务).label('服务_min'),
            func.min(Shop.环境).label('环境_min')
        ).first()

        avg_scores = db.session.query(
            func.avg(Shop.评分).label('总评分_avg'),
            func.avg(Shop.口味).label('口味_avg'),
            func.avg(Shop.服务).label('服务_avg'),
            func.avg(Shop.环境).label('环境_avg')
        ).first()

        # 准备返回的数据
        data = {
            '最大值': {
                '总评分': max_scores.总评分_max,
                '口味': max_scores.口味_max,
                '服务': max_scores.服务_max,
                '环境': max_scores.环境_max
            },
            '最小值': {
                '总评分': min_scores.总评分_min,
                '口味': min_scores.口味_min,
                '服务': min_scores.服务_min,
                '环境': min_scores.环境_min
            },
            '平均值': {
                '总评分': avg_scores.总评分_avg,
                '口味': avg_scores.口味_avg,
                '服务': avg_scores.服务_avg,
                '环境': avg_scores.环境_avg
            }
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/shopslocation', methods=['GET'])
def get_treemap_data():
    try:
        # 获取商圈和标签的统计数据
        商圈数据 = db.session.query(
            Shop.位置,
            Shop.标签,
            func.count(Shop.ROWID).label('数量')
        ).group_by(Shop.位置, Shop.标签).all()

        # 构建返回的数据结构
        result = {}
        for 位置, 标签, 数量 in 商圈数据:
            if 位置 not in result:
                result[位置] = {}
            if 标签 not in result[位置]:
                result[位置][标签] = {'数量': 0}
            result[位置][标签]['数量'] += 数量

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/shops', methods=['GET'])
def get_shops():
    try:
        title = request.args.get('title', '')  # 获取查询参数中的 title
        page = int(request.args.get('page', 1))  # 获取当前页码，默认为 1
        limit = int(request.args.get('limit', 10))  # 获取每页显示的记录数，默认为 10
        # 根据 title 进行模糊搜索
        query = Shop.query.filter(Shop.商家名称.like(f'%{title}%'))
        # 计算总数和获取当前页数据
        total = query.count()  # 总记录数
        shops = query.offset((page - 1) * limit).limit(limit).all()  # 当前页的数据
        result = shops_schema.dump(shops)  # 使用你的序列化方案处理数据
        return make_response(data={'total': total, 'records': result})
    except Exception as e:
        return make_response(code=1, message=str(e))
    


# 推荐系统
@main.route('/commend', methods=['POST'])  # 修改为 POST 方法
def commend():
    data = request.get_json()  # 获取 JSON 数据
    UserID = data.get('UserID')  # 直接获取 UserID
    user_meal_scene = data.get('user_meal_scene')  # 直接获取 user_meal_scene
    user_focus_point = data.get('user_focus_point')  # 直接获取 user_focus_point

    result = get_final_recommendations(UserID, user_meal_scene, user_focus_point)
    if result is None:
        return jsonify({'error': '参数不能为空'}), 400
    return jsonify(result), 200

