<script setup>
import { Position, Handle } from '@vue-flow/core'
import { ref } from 'vue';

// props were passed from the slot using `v-bind="customNodeProps"`
const props = defineProps(['label', 'id'])

const emit = defineEmits([ 'add', 'remove' ]);

const inputValue = ref('')
</script>

<template>
    <div class="node-body">
        <div>{{ label }}</div>
        <div class="node-hover">
            <span class="material-symbols-outlined">
                edit
            </span>
            <div class="node-helper">
                <div class="node-helper__actions">
                    <button
                    class="node-helper__action"
                    @click="emit('add', id)"
                    >
                        Добавить кнопку
                    </button>
<!--                    <button-->
<!--                        class="node-helper__action"-->
<!--                        @click="emit('remove', id)"-->
<!--                    >-->
<!--                        Удалить блок-->
<!--                    </button>-->
                </div>
            </div>
        </div>
    </div>
</template>
