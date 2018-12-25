import Hashids from "hashids";

const hashids = new Hashids("b9iLXiAa", 5);

const encode = (param) => {
    return hashids.encode(param);
};

const decode = (param) => {
    return hashids.decode(param);
};


export const hasher = {
    encode,
    decode
};