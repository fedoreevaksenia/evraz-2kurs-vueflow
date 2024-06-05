<script setup>
import {
    ref,
    onMounted,
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
import Icon from './components/Icon.vue';
import CustomNode from '@/components/CustomNode.vue';
import DropzoneBackground from '@/components/DropzoneBackground.vue';
import useDragAndDrop from './composables/useDnD';
import Sidebar from '@/components/Sidebar.vue';
import CustomParentNode from '@/components/CustomParentNode.vue';

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

const { onDragOver, onDrop, onDragLeave, isDragOver } = useDragAndDrop();

// our dark mode toggle flag
const dark = ref(false);

let nodesId = ref(0);

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

function generateRandomNode() {
    return {
        id: Math.random().toString(),
        // position:       { x: Math.random() * 500, y: Math.random() * 500 },
        position:       { x: 16, y: 75 },
        label:          'Random Node',
        connectable:    true,
        type:           'default', // You can omit this as it's the fallback type
        targetPosition: Position.Top, // or Bottom, Left, Right,
        sourcePosition: Position.Bottom, // or Top, Left, Right,
    };
}

function onAddNode() {
    // add a single node to the graph
    // addNodes(generateRandomNode());
    
    let parentNodeId = nodesId.value;
    let parentNode = {
        id:       parentNodeId,
        label:    'parent node',
        type:     'parent',
        position: { x: 100, y: 100 },
        style:    {
            backgroundColor: 'rgba(16, 185, 129, 0.5)',
            width:           '400px',
            height:          '200px',
        },
    };
    nodesId.value = nodesId.value + 1;
    addNodes(parentNode);
    
    let titleNode = {
        id:         nodesId.value,
        label:      'Сообщение',
        type:       'input',
        position:   { x: 0, y: 0 },
        parentNode: parentNodeId.toString(),
        extent:     'parent',
        // expandParent: true,
    };
    nodesId.value = nodesId.value + 1;
    addNodes(titleNode);
    
    let buttonNode = {
        id:         nodesId.value,
        label:      'Текст кнопки',
        type:       'default',
        position:   { x: 20, y: 20 },
        parentNode: parentNodeId.toString(),
        extent:     'parent',
        // expandParent: true,
    };
    nodesId.value = nodesId.value + 1;
    addNodes(buttonNode);
    
    buttonNode = {
        id:         nodesId.value,
        label:      'Текст кнопки',
        type:       'default',
        position:   { x: 20, y: 20 },
        parentNode: parentNodeId.toString(),
        extent:     'parent',
        // expandParent: true,
    };
    nodesId.value = nodesId.value + 1;
    addNodes(buttonNode);
}

function onAddNodes() {
    // add multiple nodes to the graph
    addNodes(Array.from({ length: 10 }, generateRandomNode));
}

// remove a single node from the graph
function onRemoveNode(id) {
    const canRemove = confirm('Вы уверены, что хотите удалить этот блок?');
    if (canRemove) {
        removeNodes(id);
    }
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
    localStorage.setItem('nodes', JSON.stringify(toObject()));
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

function handleNodeDragStop() {
    saveNodes(initialNodes.value);
}

// remove multiple nodes from the graph
function onRemoveNodes() {
    removeNodes([ '1', '2' ]);
}

function onSomeEvent(nodeId) {
    // const node = initialNodes.value.find((node) => node.id == nodeId)
    const node = findNode('1');
    if (node) {
        node.label = 'Node custom';
    }
    // node.data = {
    //     ...node.data,
    //     hello: 'world',
    // }
    //
    // // you can also mutate properties like `selectable` or `draggable`
    // node.selectable = false
    // node.draggable = false
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
    setViewport({ x: 0, y: 0, zoom: 1 });
}

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
                    @remove="onRemoveNode"
                    @edit="onEditNode"
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
    
    <div class="main-buttons">
        <button
            type="button"
            @click="onAddNode"
        >+ Новый блок сообщения
        </button>
    </div>
</template>

<style lang="scss">
@import 'style/main';
</style>
