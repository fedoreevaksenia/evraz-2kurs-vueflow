import {
    createWebHistory,
    createRouter,
} from 'vue-router';

const routes = [
    {
        path:      '/',
        component: () => import('../App.vue'),
        children:  [
            {
                path:      '',
                name:      'start',
                component: () => import('../pages/StartPage.vue'),
            },
            {
                path:      'scheme/:id',
                name:      'scheme',
                component: () => import('../pages/SchemeDetails.vue'),
            },
        ],
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
