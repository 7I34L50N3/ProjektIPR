<template>
    <div>
        <h1>Logged in successfully!</h1>
        <button @click="goToLogin">Back to login</button>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'SuccessView',
    setup() {
        const router = useRouter();
        const goToLogin = () => {
            router.push('/');
        };
        return { goToLogin };
    },
});
</script>

<style scoped>
h1 {
    color: green;
}
</style>