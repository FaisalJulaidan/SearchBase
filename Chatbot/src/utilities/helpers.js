
export const detectUserType = (userTypesArr) => {
    if(userTypesArr.length === 0)
        return [];

    var typesFreqs = {};
    var maxEl = userTypesArr[0], maxCount = 1;
    for(var i = 0; i < userTypesArr.length; i++)
    {
        var el = userTypesArr[i];
        if(typesFreqs[el] == null)
            typesFreqs[el] = 1;
        else
            typesFreqs[el]++;
        if(typesFreqs[el] > maxCount)
        {
            maxEl = el;
            maxCount = typesFreqs[el];
        }
    }
    return Object.keys(typesFreqs).filter(key => typesFreqs[key] === maxCount && key !== "Unknown");
};
