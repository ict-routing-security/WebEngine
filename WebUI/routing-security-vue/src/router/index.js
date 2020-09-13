import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/realglobal'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/realglobal',
                    component: () => import(/* webpackChunkName: "real_global" */ '../components/page/real_global.vue'),
                    meta: { title: '真实平台-网络汇总' }
                },
                {
                    path: '/realeach',
                    component: () => import(/* webpackChunkName: "real_each" */ '../components/page/real_each.vue'),
                    meta: { title: '真实平台-单路由器' }
                },
                {
                    path: '/realattack',
                    component: () => import(/* webpackChunkName: "real_attack" */ '../components/page/real_attack.vue'),
                    meta: { title: '真实平台-异常事件' }
                },
                {
                    path: '/simuglobal',
                    component: () => import(/* webpackChunkName: "real_global" */ '../components/page/simu_global.vue'),
                    meta: { title: '模拟平台-网络汇总' }
                },
                {
                    path: '/simueach',
                    component: () => import(/* webpackChunkName: "real_each" */ '../components/page/simu_each.vue'),
                    meta: { title: '模拟平台-单路由器' }
                },
                {
                    path: '/simuattack',
                    component: () => import(/* webpackChunkName: "real_attack" */ '../components/page/simu_attack.vue'),
                    meta: { title: '模拟平台-异常事件' }
                },
                {
                    // 权限页面
                    path: '/permission',
                    component: () => import(/* webpackChunkName: "permission" */ '../components/page/Permission.vue'),
                    meta: { title: '权限测试', permission: true }
                },
                {
                    path: '/404',
                    component: () => import(/* webpackChunkName: "404" */ '../components/page/404.vue'),
                    meta: { title: '404' }
                },
                {
                    path: '/403',
                    component: () => import(/* webpackChunkName: "403" */ '../components/page/403.vue'),
                    meta: { title: '403' }
                }
            ]
        },
        {
            path: '/login',
            component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue'),
            meta: { title: '登录' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});
