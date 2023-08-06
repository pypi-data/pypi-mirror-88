<template>
    <component
        :is="getComponent(layout)"
        v-bind="layout.props || {}"
    >
        <template v-if="layout.children">
            <Layout v-for="(v,k) in layout.children" :key="k" :layout="v">
                <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
                    <slot :name="slot" v-bind="scope"/>
                </template>
            </Layout>
        </template>
        <template v-else>
            <slot :name="getName(layout)" v-bind:field="getFieldScope(layout)">
               {{ layout }}
            </slot>
        </template>
    </component>
</template>

<script lang="ts">
import {Component, Prop, Vue, Watch} from 'vue-property-decorator';
import {BCol, BRow} from "bootstrap-vue";
import Div from "@/components/Div.vue";
import {FieldLayout} from "@/interfaces/FormTypes";
import {DVComponent} from "@/interfaces/ApiInfo";

@Component({
    name: 'Layout',
    components: {
        Layout
    },
})
export default class Layout extends Vue {
    @Prop() private readonly layout!: any

    getComponent(l: any){
        if(this.isLeaf(l)){
            return Div
        }
        if(l.tag === 'BRow'){
            return BRow
        }
        if(l.tag === 'BCol'){
            return BCol
        }
        if(l.tag === 'Div'){
            return Div
        }
        return Div
    }

    getName(layout: FieldLayout | string) : string{
        if(typeof layout === 'string'){
            return layout
        }
        return layout.name
    }

    getFieldScope(layout: FieldLayout | string): FieldLayout{
        if(typeof layout === 'string'){
            return {
                name: layout,
                props: {},
                tag: DVComponent.B_FORM_INPUT
            }
        }
        return layout
    }

    isLeaf(l: any){
         return typeof l == 'string'
    }
}
</script>

<style lang="scss" scoped>

</style>
