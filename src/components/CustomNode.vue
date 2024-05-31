<script setup>
import { Position, Handle } from '@vue-flow/core'
import { DefineProps } from '@vue/runtime-core'
import { ref } from 'vue';

// props were passed from the slot using `v-bind="customNodeProps"`
const props = defineProps(['label', 'id'])

const emit = defineEmits([ 'remove', 'edit' ]);

const inputValue = ref('')
</script>

<template>
    <div class="node-body">
        <Handle type="target" :position="Position.Top" />
        <div>{{ label }}</div>
        <Handle type="source" :position="Position.Bottom" />
        <div class="node-helper">
			<div class="node-helper__actions">
				<button
					class="node-helper__action"
					@click="emit('remove', id)"
				>
					Удалить
				</button>

				<button
					class="node-helper__action"
					@click="emit('edit', id)"
				>
					Редактировать
				</button>
			</div>
		</div>
    </div>
    <!--<div class="custom-node-container">-->
    <!--    <input class="nodrag" v-model="inputValue" />-->
    <!--</div>-->
</template>
