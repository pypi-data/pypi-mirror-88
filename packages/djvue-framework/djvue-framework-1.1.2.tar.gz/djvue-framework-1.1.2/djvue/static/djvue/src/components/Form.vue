<template>
    <div>
        <b-alert
            :show="showFormErrorAlert"
            class="col-12"
            variant="danger"
        >
            <p class="m-0" v-for="(e,idx) in formErrors" :key="idx">{{ e }}</p>
        </b-alert>

        <b-alert
            :show="showNonFieldAlert"
            class="col-12"
            variant="warning"
        >
            <p class="m-0" v-for="(e,idx) in nonFieldErrors" :key="idx">{{ e }}</p>
        </b-alert>

        <div class="d-flex justify-content-between pb-3"
             v-if="showRemove"
        >
            <b-badge pill variant="secondary" class="align-self-baseline">{{ inlineKey + 1 }}</b-badge>
            <BButton
                @click="$emit('remove', inlineKey)"
                size="sm"
                variant="danger"
            >
                <BIcon icon="trash"></BIcon>
            </BButton>
        </div>

        <b-form v-bind="form.props">
            <Layout :layout="form" ref="layout">
                <template v-slot:[f.name]="scope" v-for="f in Fields">
                    <component
                        :is="getComponent(f, scope.field)"
                        :key="f.name"
                        v-bind="getComponentAttributes(f, form.defaults, scope.field.props)"
                        :state="getErrorState(f)"
                    >
                        <component
                            v-if="getWrapper(f, scope.field)"
                            :is="getWrapper(f, scope.field)"
                            v-bind="getWidgetAttributes(f, form.defaults, scope.field.props)"
                        >
                            <component
                                :is="getWidget(f, scope.field)"
                                v-model="value[f.name]"
                                v-bind="getWidgetAttributes(f, form.defaults, scope.field.props)"
                                @input="onInput(f.name, $event)"
                            >
                            </component>
                        </component>
                        <component
                            v-else
                            :is="getWidget(f, scope.field)"
                            v-model="value[f.name]"
                            v-bind="getWidgetAttributes(f, form.defaults, scope.field.props)"
                            @input="onInput(f.name, $event)"
                        >
                        </component>

                    </component>
                </template>
            </Layout>
        </b-form>
    </div>
</template>

<script lang="ts">
import {Component, Prop, Watch} from 'vue-property-decorator';
import {
    DVComponent,
    EOperation,
    StringKeyArrayString,
} from "@/interfaces/ApiInfo";
import DjVueSelect from "@/components/forms/DjVueSelect.vue";
import DjVueAcSelect from "@/components/forms/DjVueAcSelect.vue";
import DjVueRadioGroup from "@/components/forms/DjVueRadioGroup.vue";
import DjVueCheckboxGroup from "@/components/forms/DjVueCheckboxGroup.vue";
import FormComponent from "@/components/FormComponent";
import {BFormCheckbox, BFormGroup, BFormInput, BFormTextarea} from "bootstrap-vue";
import DjVueInputGroup from "@/components/forms/DjVueInputGroup.vue";
import Layout from "@/components/Layout.vue";
import {FieldLayout, FormLayout} from "@/interfaces/FormTypes";
import DjVueHidden from "@/components/forms/DjVueHidden.vue";
import InlineForm from "@/components/InlineForm.vue";


@Component({
    name: 'Form',
    components: {
        Layout,
        DjVueAcSelect,
        DjVueSelect,
        BFormTextarea
    },
})
export default class Form extends FormComponent {
    @Prop(Number) private readonly operation!: EOperation
    @Prop() private readonly value!: any
    @Prop() private readonly form!: FormLayout
    @Prop() private readonly fields!: any
    @Prop() private readonly inlineKey!: number
    @Prop() private readonly showRemove!: boolean

    @Prop({
        type: Object, default: () => {
            return {}
        }
    }) private readonly fieldErrors!: StringKeyArrayString
    @Prop({
        type: Array, default: () => {
            return []
        }
    }) private readonly formErrors!: string[]
    @Prop({
        type: Array, default: () => {
            return []
        }
    }) private readonly nonFieldErrors!: string[]
    @Prop({type: Boolean, default: true}) private readonly prevent_id!: boolean

    private dvComponent = DVComponent

    get showSend() {
        return this.operation !== EOperation.DETAIL
    }

    get Fields() {
        return this.fields
    }

    get showFormErrorAlert() {
        return this.formErrors.length > 0
    }

    get showNonFieldAlert() {
        return this.nonFieldErrors.length > 0
    }

    getFieldError(f: any) {
        return this.fieldErrors[f.name] || []
    }

    getFirstFieldError(f: any) {
        return this.getFieldError(f)[0] || ''
    }

    getErrorState(f: any) {
        if (this.fieldErrors && this.fieldErrors[f.name]) {
            return this.fieldErrors[f.name].length == 0
        }
        return null
    }

    getType(f: any) {
        switch (f.type) {
            case 'integer':
            case 'decimal':
            case 'float':
                return 'number'
            case 'string':
                return 'text'
            case 'boolean':
                return 'number'
            case 'field':
                return 'select'
            case 'datetime':
                return 'datetime-local'
            default:
                return f.type
        }
    }

    isInline(f: any) {
        return f.type === 'nested object'
    }

    getInlineAttribute(f: any) {
        return {
            field: f,
            value: this.value[f.name],
            operation: this.operation,
            fieldErrors: this.getFieldError(f)
        }
    }

    isHidden(f: any) {
        return f.tag === DVComponent.DJVUE_HIDDEN
    }

    getComponentAttributes(f: any, fd: any, w: any) {
        const p = {...f, ...fd, ...w}

        return {
            ...p,
            invalidFeedback: this.getFirstFieldError(f)
        }
    }


    getWidgetAttributes(f: any, fd: any, w: any) {
        const p = {...f, ...fd, ...w}

        if (this.isInline(p)) {
            return this.getInlineAttribute(p)
        }
        return {
            ...p,
            type: this.getType(p),
            baseUrl: this.baseUrl,
            defaultParams: this.defaultParams,
            disabled: this.operation == EOperation.DETAIL ? true : p.read_only,
            multiple: p.many || false,
        }
    }


    getComponent(f: any, fl: FieldLayout) {
        const p = {...f, ...fl}
        if (this.isHidden(p)) {
            return DjVueHidden
        } else if (this.isInline(p)) {
            return InlineForm;
        } else {
            return BFormGroup;
        }
    }

    // il wrapper è solo un omponente che viene utilizzato quando si vuole un prepend e/o un append.
    getWrapper(f: any, fl: FieldLayout) {
        const p = {...f, ...fl}
        if(p.props.append || p.props.prepend) {
            return DjVueInputGroup
        }
        return false
    }

    getWidget(f: any, fl: FieldLayout) {
        const p = {...f, ...fl}
        switch (p.tag) {
            case DVComponent.B_FORM_TEXTAREA:
                return BFormTextarea
            case DVComponent.B_FORM_CHECKBOX:
                return BFormCheckbox
            case DVComponent.DJVUE_RADIO_GROUP:
                return DjVueRadioGroup
            case DVComponent.DJVUE_CHECKBOX_GROUP:
                return DjVueCheckboxGroup
            case DVComponent.DJVUE_AC_SELECT:
                return DjVueAcSelect
            case DVComponent.DJVUE_SELECT:
                return DjVueSelect
            default:
                switch (p.type) {
                    case 'field':
                    case 'choice':
                        if (p.many) {
                            return DjVueAcSelect
                        }
                        return DjVueSelect
                    case 'boolean':
                        return BFormCheckbox
                }
                return BFormInput
        }
    }

    onInput(name: string, val: any) {
        //todo questa cosa puo' essere tolta?
        // this.value[name] = val;
        this.$emit('input', this.value);
    }

    @Watch('fields')
    initData() {
        for (const f in this.Fields) {
            if (this.value && !Object.prototype.hasOwnProperty.call(this.value, f)) {
                this.initFieldData(this.Fields[f])
            }
        }
    }

    initFieldData(f: any) {
        if (f.type == 'nested object') {
            this.$set(this.value, f.name, [])
            return
        } else if (!Object.prototype.hasOwnProperty.call(this.value, f.name)) {
            if (typeof f.default !== "undefined") {
                this.$set(this.value, f.name, f.default)
            } else if (f.type == 'field' && f.many) {
                this.$set(this.value, f.name, [])
            } else if (f.required) {
                switch (f.type) {
                    //nel caso dei booleano settare il default per non avere un messaggio di errore, oppure usare un
                    //nullable boolean lato backcend
                    case 'boolean':
                        if (!f.allow_null) {
                            this.$set(this.value, f.name, false)
                        }
                        break
                    default:
                        //in tutti gli altri casi metto ad undefined. Se non lo faccio alcuni componenti come la multiselect si incartano
                        this.$set(this.value, f.name, undefined)

                }
            }
        }
    }
}
</script>

<style lang="scss" scoped>

</style>
