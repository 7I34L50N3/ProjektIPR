import { createRouter, createWebHistory } from 'vue-router';
import SuccessView from './components/SuccessView.vue';

const routes = [
    { path: '/', component: SuccessView },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;