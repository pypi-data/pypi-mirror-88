<template>
    <div :class="Class" >
        <slot></slot>
    </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({
    name: 'Div',
    inheritAttrs: false,
    components: {
    },
})
export default class Div extends Vue {
    @Prop() private readonly css_class!: string

    get Class(){
        return this.css_class
    }
}
</script>

<style lang="scss" scoped>

</style>
