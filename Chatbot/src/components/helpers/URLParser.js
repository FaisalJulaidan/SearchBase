import React from 'react';


const parseURL = (string) => {
    const hash = () => Math.random().toString(36).slice(2);
    let urlobj = [];
    let end = 0;
    if(!string)
      return null
    while (string.split('*&&').length > 1) {
        let len = '*&&TEXT:'.length;
        let endLen = '&&END*'.length;

        let textIndex = string.indexOf('*&&TEXT:');
        let linkIndex = string.indexOf('*&&LINK:');
        let endIndex = string.indexOf('&&END*');
        let text = '', link = '';

        let char = string[textIndex + len];
        while (char !== '*') {
            text += char;
            char = string[textIndex + len + text.length];
        }

        char = string[linkIndex + len];
        while (char !== '*') {
            link += char;
            char = string[linkIndex + len + link.length];
        }

        let replace = string.slice(textIndex, endIndex + endLen);
        let id = hash();
        string = string.replace(replace, id);
        urlobj.push({ str: string.slice(end, string.indexOf(id) + id.length), id, link, text });
        end = string.indexOf(id) + id.length;
    }

    if (string.length > end) {
        urlobj.push({ str: string.slice(end, string.length) });
    }
    return urlobj;
};


const URLParser = ({ children }) => {
    const url = parseURL(children);
    return (
      <>
        {url ? 
        <>
            {url.map((obj, i) => {
                return (
                    <React.Fragment key={i}>
                        {obj.str.replace(obj.id, '')}{obj.link ? <a href={obj.link}>{obj.text}</a> : null}
                    </React.Fragment>
                );
            })}
        </>
        : <>No text found</>}
      </>
    );
};

export default URLParser;
