import {StringKeyAnyObject} from "@/interfaces/ApiInfo";

export interface Layout{
    tag: number,
    props: StringKeyAnyObject
}

export interface FieldLayout extends Layout{
    name: string,
}

export interface GenericLayout extends Layout {
    children: Layout[] | string[]
}


export interface FormLayout {
    defaults: any,
    props: any,
    children: (GenericLayout | FieldLayout | string)[]
}