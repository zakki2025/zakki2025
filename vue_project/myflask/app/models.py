from . import db

class Shop(db.Model):
    __tablename__ = 'shops'

    # ID
    ROWID = db.Column(db.String(255), primary_key=True, nullable=False)
    # 商家名称
    商家名称 = db.Column(db.String(255), nullable=False)
    # 商家ID
    商家ID = db.Column(db.String(255), nullable=False)
    # 商家链接
    商家链接 = db.Column(db.String(255), nullable=False)
    # 商家标签
    标签 = db.Column(db.String(255), nullable=False)
    # 商家位置
    位置 = db.Column(db.String(255), nullable=False)
    # 评论数量
    评论数量 = db.Column(db.Integer, nullable=True)
    # 人均消费
    人均消费 = db.Column(db.Integer, nullable=True)
    # 评分
    评分 = db.Column(db.Float, nullable=True)
    # 口味
    口味 = db.Column(db.Float, nullable=True)
    # 环境
    环境 = db.Column(db.Float, nullable=True)
    # 服务
    服务 = db.Column(db.Float, nullable=True)