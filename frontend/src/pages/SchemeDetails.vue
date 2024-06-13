<script setup>
import {
    ref,
    onMounted,
    computed,
} from 'vue';
import {
    VueFlow,
    useVueFlow,
    Position,
} from '@vue-flow/core';
import { Background } from '@vue-flow/background';
import { MiniMap } from '@vue-flow/minimap';
import {
    ControlButton,
    Controls,
} from '@vue-flow/controls';
import Icon from '../components/Icon.vue';
import CustomNode from '@/components/CustomNode.vue';
import DropzoneBackground from '@/components/DropzoneBackground.vue';
import useDragAndDrop from '../composables/useDnD';
import Sidebar from '@/components/Sidebar.vue';
import CustomParentNode from '@/components/CustomParentNode.vue';
import {
    useRouter,
    useRoute,
} from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const {
    addNodes,
    removeNodes,
    findNode,
    addEdges,
    onConnect,
    setViewport,
    toObject,
    fromObject,
    updateNode,
    onNodeDragStop,
} = useVueFlow();

const { onDrop, isDragOver } = useDragAndDrop();

// our dark mode toggle flag
const dark = ref(false);

const nodesId = ref(0);
const schemeName = ref('');
const botUserName = ref('');
const botLink = ref('');
const activeBot = ref(false);
const initialNodes = ref([
    // { id: '1', type: 'input', label: 'node', position: { x: 250, y: 0 } },
    // {
    //     id: '2',
    //     label: 'parent node',
    //     position: { x: 100, y: 100 },
    //     style: { backgroundColor: 'rgba(16, 185, 129, 0.5)', width: '200px', height: '200px' },
    // },
    // {
    //     id: '2a',
    //     label: 'child node',
    //     position: { x: 10, y: 50 },
    //     parentNode: '2',
    // },
    // {
    //     id: '4',
    //     label: 'parent node',
    //     position: { x: 320, y: 175 },
    //     style: { backgroundColor: 'rgba(16, 185, 129, 0.5)', width: '400px', height: '300px' },
    // },
    // {
    //     id: '4a',
    //     label: 'child node',
    //     position: { x: 15, y: 65 },
    //     extent: 'parent',
    //     parentNode: '4',
    // },
    // {
    //     id: '4b',
    //     label: 'nested parent node',
    //     position: { x: 15, y: 120 },
    //     style: { backgroundColor: 'rgba(139, 92, 246, 0.5)', height: '150px', width: '270px' },
    //     parentNode: '4',
    // },
    // {
    //     id: '4b1',
    //     label: 'nested child node',
    //     position: { x: 20, y: 40 },
    //     parentNode: '4b',
    // },
    // {
    //     id: '4b2',
    //     label: 'nested child node',
    //     position: { x: 100, y: 100 },
    //     parentNode: '4b',
    // },
    // { id: '4c', label: 'child node', position: { x: 200, y: 65 }, parentNode: '4' },
    // {
    //     id: '999',
    //     type: 'input',
    //     label: 'Drag me to extend area!',
    //     position: { x: 20, y: 100 },
    //     class: 'light',
    //     expandParent: true,
    //     parentNode: '2',
    // },
]);

const initialEdges = ref([
    // {
    //     id: 'e1-2',
    //     source: '1',
    //     target: '2',
    //     animated: true,
    // },
]);

const schemeId = computed(() => route.params.id);

function onAddNode() {
    let parentNodeId = nodesId.value;
    let parentNode = {
        id:       parentNodeId,
        label:    'Блок ответа',
        type:     'parent',
        position: { x: 150, y: 150 },
        style:    {
            backgroundColor: 'rgba(16, 185, 129, 0.5)',
            width:           '350px',
            height:          '250px',
        },
    };
    nodesId.value = nodesId.value + 1;
    addNodes(parentNode);
    
    let titleNodeId = nodesId.value;
    let titleNode = {
        id:         titleNodeId,
        label:      'Сообщение',
        type:       'input',
        position:   { x: 100, y: 40 },
        parentNode: parentNodeId.toString(),
        extent:     'parent',
        // expandParent: true,
    };
    nodesId.value = nodesId.value + 1;
    addNodes(titleNode);
    
    let buttonNode1 = nodesId.value;
    let buttonNode = {
        id:         buttonNode1,
        label:      'Текст кнопки',
        type:       'default',
        position:   { x: 20, y: 155 },
        parentNode: parentNodeId.toString(),
        extent:     'parent',
        // expandParent: true,
    };
    nodesId.value = nodesId.value + 1;
    addNodes(buttonNode);
    
    let buttonNode2 = nodesId.value;
    buttonNode = {
        id:         buttonNode2,
        label:      'Текст кнопки',
        type:       'default',
        position:   { x: 180, y: 155 },
        parentNode: parentNodeId.toString(),
        extent:     'parent',
        // expandParent: true,
    };
    nodesId.value = nodesId.value + 1;
    addNodes(buttonNode);
    
    addEdges({
        id:       `e${ titleNodeId }-${ buttonNode1 }`,
        source:   titleNodeId.toString(),
        target:   buttonNode1.toString(),
        animated: true,
    });
    addEdges({
        id:       `e${ titleNodeId }-${ buttonNode2 }`,
        source:   titleNodeId.toString(),
        target:   buttonNode2.toString(),
        animated: true,
    });
}

// Функция редактирования блока
function onEditNode(id) {
    const node = findNode(id);
    const blockName = prompt('Введите новое название для блока');
    if (blockName) {
        updateNode(node.id, {
            label: blockName,
        });
        // node.label = blockName;
        saveNodes();
    }
}

// Функция сохранения блоков в хранилище браузера
function saveNodes(newNodes) {
    // localStorage.setItem('nodes', JSON.stringify(toObject()));
    updateSchemeData();
}

// Функция получения блоков из хранилища браузера
function loadNodes() {
    const nodes = localStorage.getItem('nodes');
    const nodesArr = JSON.parse(localStorage.getItem('nodes')) || { nodes: [] };
    nodesId.value = nodesArr.nodes.length + 1;
    
    if (nodes) {
        fromObject(JSON.parse(nodes));
        // initialNodes.value = JSON.parse(nodes);
    }
}

/**
 * onConnect is called when a new connection is created.
 *
 * You can add additional properties to your new edge (like a type or label) or block the creation altogether by not calling `addEdges`
 */
onConnect((connection) => {
    connection.animated = true;
    addEdges(connection);
});

onNodeDragStop((a, b, c) => {
    saveNodes();
});

/**
 * toObject transforms your current graph data to an easily persist-able object
 */
function logToObject() {
    console.log(toObject());
}

/**
 * Resets the current viewport transformation (zoom & pan)
 */
function resetTransform() {
    setViewport({ x: 0, y: 0, zoom: 1 });
}

function onAdd(id) {
    let node = findNode(id);
    let result = node.style.width.replace('px', '');
    let dlina = parseInt(result) + 160;
    let pobeda = dlina.toString() + 'px';
    updateNode(id, {
        width: pobeda,
    });
    saveNodes(updateNode);
    let pravo = dlina - 170;
    let buttonNode = {
        id:         nodesId.value,
        label:      'Текст кнопки',
        type:       'default',
        position:   { x: pravo, y: 95 },
        parentNode: id.toString(),
        extent:     'parent',
    };
    nodesId.value = nodesId.value + 1;
    addNodes(buttonNode);
    // console.log(nodesId.value)
}

function onRemoveNode(id) {
    let node = findNode(id);
    const canRemove = confirm('Вы уверены, что хотите удалить этот блок?');
    if (canRemove) {
        removeNodes(id);
        nodesId.value = nodesId.value - 1;
    }
    if (node.type === 'default') {
        let code = findNode(node.parentNode);
        let result = code.width.replace('px', '');
        let dlina = parseInt(result) - 150;
        let pobeda = dlina.toString() + 'px';
        updateNode(node.parentNode, {
            width: pobeda,
        });
        saveNodes(updateNode);
    }
}

function toggleDarkMode() {
    dark.value = !dark.value;
}

async function getSchemeData() {
    try {
        const response = await axios.get(`/api/schemes/${ schemeId.value }`);
        
        if (response.data.message.front_schema) {
            fromObject(response.data.message.front_schema);
        }
        
        schemeName.value = response.data.message.name;
        botUserName.value = response.data.message.botUserName;
        botLink.value = response.data.message.botLink;
    }
    catch (err) {
        console.error('ERROR GET SCHEME');
        console.error(err);
    }
}

async function updateSchemeData(activeBot = false) {
    let status = false;
    
    try {
        const request = {
            scheme:    toObject(),
            name:      schemeName.value,
            activeBot: activeBot,
        };
        const response = await axios.post(`/api/schemes/${ schemeId.value }/update`, request);
        status = true;
    }
    catch (err) {
        console.error('ERROR UPDATE SCHEME');
        console.error(err);
    }
    
    return status;
}

async function changeSchemeName() {
    try {
        let result = prompt('Введите новое название проекта');
        
        if (result && result.length === 0) {
            await changeSchemeName();
        }
        else if (!result) {
        
        }
        else {
            schemeName.value = result;
            await updateSchemeData();
        }
    }
    catch (err) {
        console.error('ERROR CREATE PROJECT');
        console.error(err);
    }
}

async function activeBotAction() {
    let res = await updateSchemeData(true);
    if (res) {
        activeBot.value = true;
    }
}

onMounted(() => {
    getSchemeData();
    // loadNodes();
});
</script>

<template>
    <div
        class="dndflow"
        @drop="onDrop"
    >
        <VueFlow
            v-model="initialNodes"
            :class="{ dark }"
            class="basicflow"
            :nodes="initialNodes"
            :edges="initialEdges"
            :default-viewport="{ zoom: 1 }"
            :min-zoom="0.2"
            :max-zoom="4"
            @update:model-value="saveNodes"
        >
            <!--<template #node-custom="customNodeProps">-->
            <!--    <CustomNode v-bind="customNodeProps"/>-->
            <!--</template>-->
            
            <template #node-info="customNodeProps">
                <CustomNode
                    v-bind="customNodeProps"
                    @remove="onRemoveNode"
                    @edit="onEditNode"
                />
            </template>
            
            <template #node-default="customNodeProps">
                <CustomNode
                    v-bind="customNodeProps"
                    @remove="onRemoveNode"
                    @edit="onEditNode"
                />
            </template>
            
            <template #node-output="customNodeProps">
                <CustomNode
                    v-bind="customNodeProps"
                    @remove="onRemoveNode"
                    @edit="onEditNode"
                />
            </template>
            
            <template #node-input="customNodeProps">
                <CustomNode
                    v-bind="customNodeProps"
                    @remove="onRemoveNode"
                    @edit="onEditNode"
                />
            </template>
            
            <template #node-parent="customNodeProps">
                <CustomParentNode
                    v-bind="customNodeProps"
                    @add="onAdd"
                />
            </template>
            
            <Background
                pattern-color="#aaa"
                :gap="16"
            />
            
            <MiniMap/>
            
            <DropzoneBackground
                :style="{
                backgroundColor: isDragOver ? '#e7f3ff' : 'transparent',
                transition: 'background-color 0.2s ease',
            }"
            />
            
            <Controls position="top-right">
                <ControlButton
                    title="Reset Transform"
                    @click="resetTransform"
                >
                    <Icon name="reset"/>
                </ControlButton>
                
                <ControlButton
                    title="Toggle Dark Mode"
                    @click="toggleDarkMode"
                >
                    <Icon
                        v-if="dark"
                        name="sun"
                    />
                    <Icon
                        v-else
                        name="moon"
                    />
                </ControlButton>
                
                <ControlButton
                    title="Log `toObject`"
                    @click="logToObject"
                >
                    <Icon name="log"/>
                </ControlButton>
            </Controls>
        </VueFlow>
        
        <!--<Sidebar />-->
    </div>
    <div
        class="main-buttons"
        style="display:flex; flex-direction: column; align-items: flex-start;"
    >
        <div
            class="back-button"
            @click="router.push({ name: 'start' })"
        >← На главную
        </div>
        <div class="scheme__name">
            <div>
                {{ schemeName }}
                
                <span
                    class="material-symbols-outlined"
                    @click="changeSchemeName"
                >
                    edit
                </span>
            </div>
            
            <div>
                <a
                    :href="botLink"
                    target="_blank"
                >{{ botUserName }}</a>
            </div>
        </div>
        <button
            type="button"
            @click="onAddNode"
        >+ Новый блок сообщения
        </button>
        <button
            v-if="!activeBot"
            type="button"
            @click="activeBotAction"
        >Активировать бота
        </button>
    </div>
</template>

<style lang="scss">
.scheme {
    &__name {
        width:            100%;
        font-weight:      bold;
        margin-bottom:    10px;
        font-size:        1.3rem;
        background-color: #fff;
        padding:          10px;
        box-shadow:       0 0 7px rgba(0, 0, 0, 0.2);
        display:          flex;
        flex-direction:   column;
        align-items:      center;
        justify-content:  center;
        
        span:hover {
            cursor: pointer;
            color:  #268f61;
        }
        
        > div {
            display:         flex;
            align-items:     center;
            justify-content: center;
            
            &:last-child {
                font-size: 1rem;
            }
        }
    }
}

.main-buttons {
    button {
        margin-bottom: 10px;
    }
}

.back-button {
    font-size:     1.3rem;
    margin-bottom: 10px;
    cursor:        pointer;
}
</style>
