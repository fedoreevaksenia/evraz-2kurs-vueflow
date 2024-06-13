<script setup>
import {ref, onMounted} from 'vue';
import {
    VueFlow,
    useVueFlow,
    Position,
} from '@vue-flow/core';
import {Background} from '@vue-flow/background';
import {MiniMap} from '@vue-flow/minimap';
import {
    ControlButton,
    Controls,
} from '@vue-flow/controls';
import Icon from './components/Icon.vue';
import CustomNode from '@/components/CustomNode.vue';
import DropzoneBackground from '@/components/DropzoneBackground.vue';
import useDragAndDrop from './composables/useDnD';
import Sidebar from '@/components/Sidebar.vue';
import CustomParentNode from "@/components/CustomParentNode.vue";

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
} = useVueFlow();

const {onDragOver, onDrop, onDragLeave, isDragOver} = useDragAndDrop();

// our dark mode toggle flag
const dark = ref(false);

const initialNodes = ref([]);

const edges = ref([
    {id: 'e1-2', source: '1', target: '2'},
    {id: 'e1-4', source: '1', target: '4'},
    {id: 'e1-4c', source: '1', target: '4c'},
    {id: 'e2a-4a', source: '2a', target: '4a'},
    {id: 'e4a-4b1', source: '4a', target: '4b1'},
    {id: 'e4a-4b2', source: '4a', target: '4b2'},
    {id: 'e4b1-4b2', source: '4b1', target: '4b2'},
])

const initialEdges = ref([
    // {
    //     id: 'e1-2',
    //     source: '1',
    //     target: '2',
    //     animated: true,
    // },
]);

// function generateRandomNode() {
//     return {
//         id: Math.random().toString(),
//         // position:       { x: Math.random() * 500, y: Math.random() * 500 },
//         position:       { x: 16, y: 75 },
//         label:          'Random Node',
//         connectable:    true,
//         type:           'default', // You can omit this as it's the fallback type
//         targetPosition: Position.Top, // or Bottom, Left, Right,
//         sourcePosition: Position.Bottom, // or Top, Left, Right,
//     };
// }

// function onAddNode() {
//     // add a single node to the graph
//     addNodes(generateRandomNode());
// }

// function onAddNodes() {
//     // add multiple nodes to the graph
//     addNodes(Array.from({ length: 10 }, generateRandomNode));
// }

// remove a single node from the graph

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
    localStorage.setItem('nodes', JSON.stringify(toObject()));
}

// Функция получения блоков из хранилища браузера
function loadNodes() {
    const nodes = localStorage.getItem('nodes');
    if (nodes) {
        fromObject(JSON.parse(nodes));
        // initialNodes.value = JSON.parse(nodes);
    }
}

function handleNodeDragStop() {
    saveNodes(initialNodes.value);
}

function onRemoveNodes() {
    removeNodes(['1', '2']);
}

function onSomeEvent(nodeId) {
    const node = findNode('1');
    if (node) {
        node.label = 'Node custom';
    }
}

/**
 * onConnect is called when a new connection is created.
 *
 * You can add additional properties to your new edge (like a type or label) or block the creation altogether by not calling `addEdges`
 */
onConnect((connection) => {
    addEdges(connection);
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
    setViewport({x: 0, y: 0, zoom: 1});
}

let nodesId = ref(0);
function onAddNode() {
    let parentNodeId = nodesId.value;
    let parentNode = {
        id: parentNodeId,
        label: 'Блок ответа',
        type: 'parent',
        position: {x: 30, y: 30},
        style: {
            backgroundColor: 'rgba(16, 185, 129, 0.5)',
            width: '350px',
            height: '150px',
        },
    };
    nodesId.value = nodesId.value + 1;
    addNodes(parentNode);
    let titleNode = {
        id: nodesId.value,
        label: 'Сообщение',
        type: 'input',
        position: {x: 100, y: 40},
        parentNode: parentNodeId.toString(),
        extent: 'parent',
    };
    nodesId.value = nodesId.value + 1;
    addNodes(titleNode);
    let buttonNode = {
        id: nodesId.value,
        label: 'Текст кнопки',
        type: 'default',
        position: {x: 20, y: 95},
        parentNode: parentNodeId.toString(),
        extent: 'parent',
    };
    nodesId.value = nodesId.value + 1;
    addNodes(buttonNode);
    buttonNode = {
        id: nodesId.value,
        label: 'Текст кнопки',
        type: 'default',
        position: {x: 180, y: 95},
        parentNode: parentNodeId.toString(),
        extent: 'parent',
    };
    nodesId.value = nodesId.value + 1;
    addNodes(buttonNode);
}
function onAdd(id) {
    let node = findNode(id)
    let result = node.style.width.replace("px", "");
    let dlina = parseInt(result) + 160
    let pobeda = dlina.toString()+'px'
    updateNode(id,{
        width: pobeda,
    });
    saveNodes(updateNode);
    let pravo = dlina-170
    let buttonNode = {
        id: nodesId.value,
        label: 'Текст кнопки',
        type: 'default',
        position: {x: pravo, y: 95},
        parentNode: id.toString(),
        extent: 'parent',
    };
    nodesId.value = nodesId.value + 1;
    addNodes(buttonNode);
    // console.log(nodesId.value)
}
function onRemoveNode(id) {
    let node = findNode(id)
    const canRemove = confirm('Вы уверены, что хотите удалить этот блок?');
    if (canRemove) {
        removeNodes(id);
    }
    if (node.type === 'default') {
        let code = findNode(node.parentNode)
        let result = code.width.replace("px", "");
        let dlina = parseInt(result) - 150
        let pobeda = dlina.toString()+'px'
        updateNode(node.parentNode,{
            width: pobeda,
        });
        saveNodes(updateNode);
    }
    nodesId.value = nodesId.value - 1;
}
// function onRemoveParentNode(id) {
//     const canRemove = confirm('Вы уверены, что хотите удалить этот блок?');
//     if (canRemove) {
//         removeNodes(id);
//         removeNodes((parseInt(id)+1).toString());
//         removeNodes((parseInt(id)+2).toString());
//         removeNodes((parseInt(id)+3).toString());
//     }
//     nodesId.value = nodesId.value - 4;
// }
function toggleDarkMode() {
    dark.value = !dark.value;
}

onMounted(() => {
    loadNodes();
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
            @dragover="onDragOver"
            @dragleave="onDragLeave"
            @nodeDragStop="handleNodeDragStop"
            @update:model-value="saveNodes"
        >
            <!--<template #node-custom="customNodeProps">-->
            <!--    <CustomNode v-bind="customNodeProps"/>-->
            <!--</template>-->

            <template #node-default="customNodeProps">
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
                    @remove="onRemoveParentNode"
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

        <Sidebar/>
    </div>
    <div class="main-buttons">
        <button
            type="button"
            @click="onAddNode"
        >Добавить блок
        </button>
    </div>
</template>

<style lang="scss">
@import 'style/main';
</style>
