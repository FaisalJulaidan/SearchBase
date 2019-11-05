import moment from 'moment'

// IF YOU WANT TO ADD MORE DATE/TIME FORMATS PUT THE MORE COMPLEX ONE FIRST 
// SO IF YOU HAVE (HH mm Z) and (HH mm), (HH mm Z) SHOULD GO FIRST SINCE IF A DATE
// FITS (HH mm Z) IT ALSO FITS (HH mm) BUT FOR ACCURACY YOU WANT (HH mm Z)

const dateFormats = [
  "ddd MMM D YYYY",
  "DD MM YYYY",
  "DD/MM/YYYY",
  "MM DD YYYY",
  "YYYY MM DD"
]

const timeFormats = [
  "HH mm Z",
  "HH mm"
]

const textFormats = {
  immediate: ["now", "immediate"]
}


export const checkDate = (date, strict=false, timeformats=false) => {
  const validate = (date, format, strict) => {
    let momentObject = moment(date, format, strict)
    if(momentObject.isValid()){
      return momentObject
    }
    return null
  }
  for(let dateFormat of dateFormats){
    let final
    if(timeformats){
      for(let time of timeFormats){
        let format = dateFormat + ` ${time}`
        final = validate(date, format, strict)
        if(final){
          return final
        }
      }
    } 
    final = validate(date, dateFormat, strict)
    if(final){
      return final
    }
  }
  // // Immediate
  // for(let type in textFormats.immediate){
  //   if(date.toLowerCase() === type){
  //     return moment()
  //   }
  // }
  
  return null
}