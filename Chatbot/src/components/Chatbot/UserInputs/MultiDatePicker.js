import React, {useState, useEffect} from 'react';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
// Styles
import './styles/Inputs.css';
// Components
import {DatePicker as AntdDatePicker, Icon, Tooltip} from 'antd';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faTelegramPlane} from '@fortawesome/free-brands-svg-icons';


const MultiDatePicker = ({message, submitMessage}) => {

    let [settings, setSettings] = useState(false);
    let [selectedDate, setSelectedDate] = useState(null);
    let [selectedDates, setSelectedDates] = useState({individual: [], range: []})
    let [temporaryRange, setTemporaryRange] = useState({start: null, end: null})
    let [mouseDown, setMouseDown] = useState(null)
    let [open, setOpen] = useState(false)

    const addClasses = (date, start, end) => {
        let startCheck = date.isSame(start, 'date')
        let endCheck = date.isSame(end, 'date')
        let firstRangeItem = date.isSame(start.clone().add(1, 'days'), 'date')
        let lastRangeItem = date.isSame(end.clone().subtract(1, 'days'), 'date')
        let className = ""
        className += startCheck ? " start" : "" // start of range
        className += endCheck ? " end" : ""  // end of range
        className += firstRangeItem ? " range-start" : "" // start of range
        className += lastRangeItem ? " range-end" : ""  // end of range
        className += 
        className += date.isBetween(start, end) && !endCheck && !startCheck ? " range": "" // in range
        return className
    }

    const renderDate = (curDate, today) => {
      let className = "antd-date-multi"
      className += curDate.isSame(today, 'month') ? "" : " fade"
      let element
      if(temporaryRange.start && temporaryRange.end){
          className += addClasses(curDate, temporaryRange.start, temporaryRange.end)
      }

      if(selectedDates.range.length !== 0){
        for(let dateRange in selectedDates.range){
          className += addClasses(curDate, selectedDates.range[dateRange][0], selectedDates.range[dateRange][1])
        }
      }

      for(let date in selectedDates.individual){
        if(Math.abs(selectedDates.individual[date].diff(curDate, 'hours')) < 23){
          className += " selected"
        }
      } 
      element = (<div className={className}><span>{curDate.format("D")}</span></div>)
      return addEventHandlers(element, curDate)
    }

    const addEventHandlers = (element, date) => {
      return React.cloneElement(element, {onMouseDown: e => dateMouseDown(e, date), onMouseOver: e => dateMouseOver(e, date), onMouseUp: e => dateMouseUp(e, date)})
    }

    useEffect(() => {
      function checkValidParent(e){
        let valid = false
        e.path.forEach(node => {
          if(node.classList){
            if(node.classList.contains("DatepickerCalendar")){
              valid = true;
            }
          }
        })
        if(!valid && open){
          setOpen(false)
        }
      }
      if(open){
        console.log('ree')
        window.addEventListener("click", checkValidParent)
      }
      return () => window.removeEventListener("click", checkValidParent)
    }, [setOpen, open])
    


    const dateMouseDown = (e, date) => {
      setMouseDown(date)
      if(temporaryRange.start){
        // click same day
        let dates = Object.assign({}, selectedDates)
        if(Math.abs(date.diff(temporaryRange.start, 'hours')) < 24){
          dates.individual.push(date)
          setSelectedDates(dates)
        } else {
          dates.range.push([temporaryRange.start, date])
          setSelectedDates(dates)
        }
        setTemporaryRange({start: null, end: null})
      } else {
        setTemporaryRange({start: date, end: null})
      }
      setOpen(true)
    }

    useEffect(() => {
      console.log(selectedDates)
    }, [selectedDates])

    const dateMouseUp = (e, date) => {
      if(mouseDown){
        setMouseDown(null)
        // setOpen(false)
      }
    }

    const dateMouseOver = (e, date) => {
      if(temporaryRange.start){
        setTemporaryRange(obj => ({...obj, end: date}))
      }
    }

    // const selectDate = (date) => {
    //   let dates = Object.assign({}, selectedDates)
    //   dates.individual.push(date)
    //   setSelectedDates(dates)
    // }

    const inputOnChangeHandler = () => {
        let text;
        if (selectedDate)
            text = selectedDate;  

        let afterMessage = message.block[flowAttributes.CONTENT][flowAttributes.CONTENT_AFTER_MESSAGE];
        let type = messageTypes.TEXT;
        let block = message.block;

        let newState = {
            curBlockID: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_BLOCKTOGOID],
            curAction: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_ACTION],
            waitingForUser: false
        };

        submitMessage(text, type, newState, afterMessage, block, {
            skipped: false,
            input: text
        });

    };

    return (
        <React.Fragment>
            <div className={'InputContainer'} onClick={() => setOpen(true)}>
                <AntdDatePicker getCalendarContainer={
                    () => {
                        if (document.getElementById('TheSearchBase_Chatbot_Input'))
                            return document.getElementById('TheSearchBase_Chatbot_Input');
                        else
                            return document.getElementById('TheSearchBase_Chatbot')
                    }}
                            className={'Datepicker'} suffixIcon={<div/>}
                            dropdownClassName={'DatepickerCalendar'}
                            showToday={false}
                            dateRender={renderDate}
                            open={open}
                            // onChange={(e) => {
                            //     if (e)
                            //         if (e._isAMomentObject)
                            //             setSelectedDate(e.format('L'));
                            //         else
                            //             setSelectedDate(e.target.value);
                            // }}
                />
            </div>
            <div className={'Submit'}>
                <i className={'SendIconActive'} onClick={inputOnChangeHandler}>
                    <FontAwesomeIcon size="2x" icon={faTelegramPlane}/>
                </i>
            </div>
        </React.Fragment>
    );
};

export default MultiDatePicker;
