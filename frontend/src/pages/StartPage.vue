<script setup>
import axios from 'axios';
import {
    onMounted,
    ref,
} from 'vue';
import { useRouter } from 'vue-router';
import { notify } from '@kyvg/vue3-notification';

const router = useRouter();

const projectsIsLoading = ref(true);
const projectsList = ref([]);

onMounted(() => {
    loadProjects();
});

async function loadProjects() {
    try {
        const response = await axios.get('/api/schemes/list');
        projectsList.value = response.data.message;
    }
    catch (err) {
        console.error('ERROR LOAD PROJECTS');
        console.error(err);
    }
    finally {
        projectsIsLoading.value = false;
    }
}

async function newProject() {
    try {
        let result = prompt('Введите название проекта');
        
        if (result && result.length === 0) {
            await newProject();
        }
        else if (!result) {
        
        }
        else {
            const request = {
                name: result,
            };
            const response = await axios.post('/api/schemes/add', request);
            notify({
                title: 'Проект успешно создан',
                type:  'success',
            });
            await router.push({ name: 'scheme', params: { id: response.data.data.id } });
        }
    }
    catch (err) {
        console.error('ERROR CREATE PROJECT');
        console.error(err);
        
        let errMsg = err.response.data.message;
        
        if (errMsg === 'bots are busy') {
            notify({
                title: 'К сожалению все боты заняты, пожалуйста попробуйте позже',
                type:  'error',
            });
        }
    }
}

async function openProject(id) {
    await router.push({ name: 'scheme', params: { id: id } });
}
</script>

<template>
    <div class="main-container">
        <button
            @click="newProject"
            class="outline"
        >+ Новый проект
        </button>
        
        <div
            v-if="projectsIsLoading"
            class="is-loading"
        ></div>
        
        <button
            v-else
            v-for="(button, buttonIndex) in projectsList"
            @click="openProject(button.id)"
        >{{ button.name }}
        </button>
    </div>
</template>

<style lang="scss">
.main-container {
    width:           100%;
    height:          100%;
    display:         flex;
    flex-direction:  column;
    justify-content: center;
    align-items:     center;
    
    button {
        cursor:           pointer;
        padding:          10px 14px;
        width:            300px;
        font-size:        1rem;
        background-color: #42b983;
        border:           1px solid #268f61;
        border-radius:    10px;
        margin-bottom:    10px;
        color:            white;
        transition:       all 0.3s ease-in-out;
        
        &:hover {
            background-color: #268f61;
        }
        
        &:last-child {
            margin-bottom: 0;
        }
        
        &.outline {
            background-color: #fff;
            color:            #268f61;
            
            &:hover {
                background-color: #268f61;
                color:            white;
            }
        }
    }
}

div.is-loading {
    width:           300px;
    height:          40px;
    border-radius:   10px;
    background:      #eee;
    background:      linear-gradient(110deg, #ececec 8%, #f5f5f5 18%, #ececec 33%);
    background-size: 200% 100%;
    animation:       1.5s shine linear infinite;
}

@keyframes shine {
    to {
        background-position-x: -200%;
    }
}
</style>
