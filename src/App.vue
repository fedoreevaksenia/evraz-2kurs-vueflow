<script setup>
import { ref, onMounted } from 'vue';
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

const {
    addNodes,
    removeNodes,
    findNode,
    addEdges,
    onConnect,
    setViewport,
    toObject,
} = useVueFlow();

const { onDragOver, onDrop, onDragLeave, isDragOver } = useDragAndDrop();

// our dark mode toggle flag
const dark = ref(false);

const initialNodes = ref([]);

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
    addNodes(generateRandomNode());
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
		node.label = blockName;
	}
}

// Функция сохранения блоков в хранилище браузера
function saveNodes(newNodes) {
	localStorage.setItem('nodes', JSON.stringify(newNodes));
}

// Функция получения блоков из хранилища браузера
function loadNodes() {
	const nodes = localStorage.getItem('nodes');
	if (nodes) {
		initialNodes.value = JSON.parse(nodes);
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
        
        <Sidebar />
    </div>
    
    <!--<div class="main-buttons">-->
    <!--    <button-->
    <!--        type="button"-->
    <!--        @click="onAddNode"-->
    <!--    >Новый узел-->
    <!--    </button>-->
    <!--</div>-->
</template>

<style lang="scss">
@import 'style/main';
</style>
