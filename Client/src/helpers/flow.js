

// This function will replace all the enum.value to enums.name for the server to accept it
import {deepClone} from "helpers/deepClone";

const parse = (flow) => {

    const newFlow = deepClone(flow);
    newFlow.groups.forEach(group => {
        group.blocks.forEach(block => {
            block.DataType = block.DataType.enumName;
        });
    });
    return newFlow;
};


export const flow = {
    parse,
};
