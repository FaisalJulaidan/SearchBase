const capitalize = (s) => {
    let capitalizeWord = (s) => {
        if (typeof s !== 'string') return '';
        return s.charAt(0).toUpperCase() + s.slice(1)
    };

    if (typeof s !== 'string') return '';
    let words = s.split(" ");
    let capitalised = "";
    words.map((word, i) => {
        if (i === 0)
            capitalised = capitalizeWord(word);
        else
            capitalised = capitalised + " " + capitalizeWord(word);
    });
    return capitalised
};

const trimDash = (s) => {
    if (typeof s !== 'string') return '';
    return s.replace("-", " ");
};

export const trimText = {
    capitalize,
    trimDash,
};