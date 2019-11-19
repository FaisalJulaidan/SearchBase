
// text (String), arr (array)
// does the text contains any of the array elements which are strings
export  const contains = (text, arr) => {
    var value = 0;
    arr.forEach(function(word){
        value = value + text.includes(word);
    });
    return (value === 1)
};