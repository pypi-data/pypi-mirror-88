<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import Div from "@/components/Div.vue";

@Component({
    name: 'DjVueHidden',
    inheritAttrs: false
})
export default class DjVueHidden extends Div {
    get Class(){
        return 'd-none'
    }
}
</script>
