import Hashids from "hashids";

const hasher = new Hashids("b9iLXiAa", 5);

const encode = (param) => {
    return hasher.encode(param);
};

const decode = (param) => {
    return hasher.decode(param);
};

export default hasher;