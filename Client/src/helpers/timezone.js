import momentTZ from 'moment-timezone'

export const convertTimezone = (dt, originalFormat, newFormat=null) => {
    let timezone = getTimezone();
    return momentTZ.utc(dt, originalFormat).tz(timezone).format(newFormat || originalFormat);
};


export const getTimezone = () => {
    // return user from local storage
    let timezone = localStorage.getItem('timezone');
    if(!timezone){return momentTZ.tz.guess();}
    return timezone;
};

export const updateTimezone = (timezone) => {
    if(!timezone) return;
    localStorage.setItem("timezone", timezone);
};