<script setup>
import useDragAndDrop from '../composables/useDnD';

const { onDragStart } = useDragAndDrop();
</script>

<template>
    <aside>
        <div class="description">Выберите нужный блок и перетащите его на рабочее пространство</div>
        
        <div class="nodes">
            <div
                class="vue-flow__node-input"
                :draggable="true"
                @dragstart="onDragStart($event, 'input')"
            >Блок для обозначения начала схемы
            </div>
            
            <div
                class="vue-flow__node-default"
                :draggable="true"
                @dragstart="onDragStart($event, 'default')"
            >Блок для обозначения какого-то действия
            </div>
            
            <div
                class="vue-flow__node-info"
                :draggable="true"
                @dragstart="onDragStart($event, 'info')"
            >Блок для описания действий
            </div>
            
            <div
                class="vue-flow__node-output"
                :draggable="true"
                @dragstart="onDragStart($event, 'output')"
            >Блок для обозначения конца ветвления
            </div>
        </div>
    </aside>
</template>
