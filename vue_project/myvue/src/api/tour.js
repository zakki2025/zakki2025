import request from '@/api/request'

// 评论前十的景点
export function getCommentsRank() {
    return request({
        url:  '/commentsRank',
        method: 'get'
    })
}

// 按照数量排名 
export function getNumberRank() {
    return request({
        url:  '/numberRank',
        method: 'get'
    })
}

// 按照数量排名 
export function getScoresRadar() {
    return request({
        url:  '/scoreradar',
        method: 'get'
    })
}

// 按照数量排名 
export function getShopsLocation() {
    return request({
        url:  '/shopslocation',
        method: 'get'
    })
}

export function shops(title,page=1,limit=10){
    return request({
        url:  '/shops',
        method: 'get',
        params: {title, page, limit}
    })
}

// 发送推荐请求
export function sendRecommendationRequest(UserID, user_meal_scene, user_focus_point) {
    return request({
        url: '/commend',  // 确保URL与后端路由一致
        method: 'post',   // 使用POST方法
        data: {           // 发送JSON数据
            UserID: UserID,
            user_meal_scene: user_meal_scene,
            user_focus_point: user_focus_point
        }
    });
}
