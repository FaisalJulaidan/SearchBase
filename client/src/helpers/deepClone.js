/**
 * Used to deep clone the object to be used as immutable object
 *
 * @param {Object} object - non-immutable object
 * @return {Object} immutable object
 */
export const deepClone = (object) => JSON.parse(JSON.stringify(object));
