<template>
    <b-input-group :prepend="prepend" :append="append" :size="$attrs.size">
        <slot>
        </slot>
    </b-input-group>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({
    name: 'DjVueInputGroup',
    inheritAttrs: false
})
export default class DjVueInputGroup extends Vue {
    @Prop(String) private readonly prepend!: string
    @Prop(String) private readonly append!: string
    @Prop() private readonly value!: string;
    @Prop() private readonly disabled!: boolean;
    @Prop() private readonly placeholder!: string;
    @Prop() private readonly state!: boolean | null;
}
</script>
