import Vue from 'vue';
import Router from 'vue-router';
import AppLayout from '@/layouts/AppLayout';

// 引入页面组件
import VisualData from '@/views/VisualData';
import RecommendSystem from '@/views/RecommendSystem';
import ShopsAround from '@/views/ShopsAround';

Vue.use(Router);

const routes = [
    {
        path: '/',
        component: AppLayout,
        redirect: '/VisualData',
        children: [
            {
                path: 'VisualData',
                component: VisualData,
                name: 'VisualData'
            },
            {
                path: 'RecommendSystem',
                component: RecommendSystem,
                name: 'RecommendSystem'
            },
            {
                path: 'ShopsAround',
                component: ShopsAround,
                name: 'ShopsAround'
            }
            // 其他子路由
        ]
    },
    // 其他路由
];

const router = new Router({
    mode: 'history',
    routes
});

export default router;

