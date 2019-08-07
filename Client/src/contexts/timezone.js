import React from 'react';
import {http} from 'helpers';
import moment from 'moment'

let TimezoneContext = React.createContext('Europe/London');

const setTimezone = async () => {
    let data = await http.get("/user/timezone")
    let tomorrowTS = moment().add(1, "days").unix()
    localStorage.setItem("TSB_TZ", JSON.stringify({expr: tomorrowTS, timezone: data.data.data}))
}

const getTimezone = () => {
    let tz = localStorage.getItem("TSB_TZ")
    if(isValid(tz)){
        return JSON.parse(tz).timezone
        return
    } else {
        return setTimezone().then(() => {
            return getTimezone()
        })
    }
}

const isValid = (item) => {
    if(item){
        if(checkExpiry(JSON.parse(item))) {
            return true
        }
    }
    return false
}


const checkExpiry = (item) => {
    if(moment(item.expr).diff(moment(), "hours") > 24){
        return false
    }
    return true
}

console.log(TimezoneContext)



export { TimezoneContext, getTimezone }