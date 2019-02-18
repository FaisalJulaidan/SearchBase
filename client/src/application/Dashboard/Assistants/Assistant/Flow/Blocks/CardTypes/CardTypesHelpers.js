export const onDelete = (id, type, handler) => handler({
    id: id,
    type: type
});

export const onCancel = (handleNewBlock, handleEditBlock) => handleNewBlock ? handleNewBlock(false) : handleEditBlock(false);


export const initActionType = (block, allGroups, handleSetState) => {
    if (block.Content.action === "Go To Specific Block")
        return {showGoToBlock: true, showGoToGroup: false}
    else if (block.Content.action === "Go To Group") {
        // because here we dont' have column in each block contains all the group
        // this is a workaround to have the group name from the block id
        const {blockToGoID} = block.Content;
        for (const group of allGroups)
            if (group.blocks[0].ID === blockToGoID)
                return {showGoToBlock: false, showGoToGroup: true};
    } else
        return {showGoToBlock: false, showGoToGroup: false};
};

export const onSelectAction = (action) => {
    if (action === "Go To Specific Block")
        return {showGoToBlock: true, showGoToGroup: false};
    else if (action === "Go To Group")
        return {showGoToBlock: false, showGoToGroup: true};
    else
        return {showGoToBlock: false, showGoToGroup: false};
};

export const onFileTypeChange = (checkedValues) => {
    return {fileTypes: checkedValues}
};

export const getBlockId = (blockToGoID, blockToGoIDGroup, blocks, formBlock) => {
    if (blockToGoID)
        return blockToGoID;
    else if (blockToGoIDGroup)
        return blockToGoIDGroup;
    else if (formBlock === "NewBlock")
        return null
    else
    // find my id and my next block id then return it
    // else retrun null
        for (const [index, block] of Object.entries(blocks))
            if (formBlock.ID === block.ID)
                if (blocks[Number(index) + 1].ID)
                    return blocks[Number(index) + 1].ID;
                else
                    return null
};

export const getInitialVariables = (flowOptions, modalState, type) => {
    let block = modalState.block ? modalState.block : {Content: {}};
    let blockOptions = {};
    // extract the correct blockType from blockTypes[]
    for (const blockType of flowOptions.blockTypes)
        if (blockType.name === (block.Type || type)) {
            blockOptions = blockType;
            break;
        }
    return {blockOptions, block}
};