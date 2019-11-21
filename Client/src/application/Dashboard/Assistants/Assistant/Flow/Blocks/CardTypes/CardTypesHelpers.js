export const onCancel = (handleNewBlock, handleEditBlock) => handleNewBlock ? handleNewBlock(false) : handleEditBlock(false);

export const initActionType = (block, allGroups) => {
    if (block.Content.action === "Go To Specific Block")
        return {showGoToBlock: true, showGoToGroup: false};
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

export const initActionTypeSkip = (block, allGroups) => {
    if (block.SkipAction === "Go To Specific Block")
        return {showGoToBlockSkip: true, showGoToGroupSkip: false};
    else if (block.SkipAction === "Go To Group") {
        // because here we dont' have column in each block contains all the group
        // this is a workaround to have the group name from the block id
        for (const group of allGroups)
            if (group.blocks[0].ID === block.SkipBlockToGoID)
                return {showGoToBlockSkip: false, showGoToGroupSkip: true};
    } else
        return {showGoToBlockSkip: false, showGoToGroupSkip: false};
};

export const onSelectAction = (action, isSkip = false) => {
    if (isSkip)
        if (action === "Go To Specific Block")
            return {showGoToBlockSkip: true, showGoToGroupSkip: false};
        else if (action === "Go To Group")
            return {showGoToBlockSkip: false, showGoToGroupSkip: true};
        else
            return {showGoToBlockSkip: false, showGoToGroupSkip: false};
    else {
        if (action === "Go To Specific Block")
            return {showGoToBlock: true, showGoToGroup: false};
        else if (action === "Go To Group")
            return {showGoToBlock: false, showGoToGroup: true};
        else
            return {showGoToBlock: false, showGoToGroup: false};
    }
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
        return null;
    else
    // find my id and my next block id then return it
    // else retrun null
        for (const [index, block] of Object.entries(blocks)) {
            if (formBlock?.ID === block?.ID)
                if (blocks[Number(index) + 1]?.ID)
                    return blocks[Number(index) + 1]?.ID;
                else
                    return null
        }
};

export const checkBlockTogGoID = (blocks, blockGroups, groupID) => {
    // if there is a passed blocks
    //   - if Content.action === "Go To Next Block" update it from here to the next block ID (DONE)
    //   - Check the current block if its blockToGoID is valid or not
    //     - how to check if it is valid or not?
    //       by finding this ID in all blocks in the assistant level
    //       if not return it as null
    //       - in the case of deleting a block and there are blocks assigned to to it
    // if there is no passed blocks
    //   - Check each block.Content.action === "Go To Next Block" in each group then update it to the next block ID
    //     - (1) Print each block from blockGroups variable
    //     - (2) Validate each block from blockGroups variable if it has valid block.Content.blockToGoID or not
    //   - [...]

    if (blocks) {
        // works fine for update
        blocks.map((block, index) => {
            if (block.Content.action === "Go To Next Block")
                block.Content.blockToGoID = blocks[Number(index) + 1]?.ID || null;
            else {
                // check the next step where to check block.ID is valid or not
                // we might have IDs from other groups, so we might need the whole state of blockGroups from reducer
                let isValidID = !!blockGroups.map(group => group.blocks.find(fromState_block => fromState_block.ID === block.ID))[0];
                if (!isValidID)
                    block.Content.blockToGoID = null;
            }
            return block;
        });

        return blocks
    } else {
        // I want this to update everything in flow
        blockGroups.map(group => {
            group.blocks.map(fromState_block => {
                // check each block.Content.blockToGoID if valid or not
                let isValidID = !!blockGroups.map(group => group.blocks.find(comparedBlock => comparedBlock.ID === fromState_block.ID))[0];
                if (!isValidID)
                    fromState_block.Content.blockToGoID = null;
            })
        });

        return blockGroups
    }
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
