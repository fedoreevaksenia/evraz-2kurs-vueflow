<script setup>
import useDragAndDrop from '../composables/useDnD';

const { onDragStart } = useDragAndDrop();
</script>

<template>
<!--    <aside>-->
<!--        <div class="description">Выберите нужный блок и перетащите его на рабочее пространство</div>-->
<!--        -->
<!--        <div class="nodes">-->
<!--            <div-->
<!--                class="vue-flow__node-input"-->
<!--                :draggable="true"-->
<!--                @dragstart="onDragStart($event, 'input')"-->
<!--            >Блок для обозначения текстового сообщения-->
<!--            </div>-->
<!--            -->
<!--            <div-->
<!--                class="vue-flow__node-default"-->
<!--                :draggable="true"-->
<!--                @dragstart="onDragStart($event, 'default')"-->
<!--            >Блок для обозначения кнопки-->
<!--            </div>-->
<!--        </div>-->
<!--    </aside>-->
</template>
