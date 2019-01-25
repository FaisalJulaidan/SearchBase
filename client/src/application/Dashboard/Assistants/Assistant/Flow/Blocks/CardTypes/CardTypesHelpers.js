export const onDelete = (id, type, handler) => handler({
    id: id,
    type: type
});

export const onCancel = (handleNewBlock, handleEditBlock) => handleNewBlock ? handleNewBlock(false) : handleEditBlock(false);


export const initActionType = (block, allGroups) => {
    if (block.content.action === "Go To Specific Block")
        return {showGoToBlock: true, showGoToGroup: false};
    else if (block.content.action === "Go To Group") {
        // because here we dont' have column in each block contains all the group
        // this is a workaround to have the group name from the block id
        const {blockToGoID} = block.content;
        allGroups.map((group) => {
            if (group.blocks[0].id === blockToGoID)
                return {showGoToBlock: false, showGoToGroup: true, groupName: group.name}
        })
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

export const onChange = (checkedValues) => {
    return {fileTypes: checkedValues}
};

export const getInitialVariables = (options, type) => {
    const {flowOptions, allGroups, allBlocks} = options;
    let block = options.block ? options.block : {content: {}};
    let blockOptions = {};
    // extract the correct blockType from blockTypes[]
    for (const blockType of flowOptions.blockTypes)
        if (blockType.name === (block.type || type)) {
            blockOptions = blockType;
            break;
        }
    return {flowOptions, allGroups, allBlocks, blockOptions, block}
};