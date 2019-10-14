import React, { useState, useEffect } from 'react';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
import * as constants from '../../../constants/Constants';
// Styles
import './styles/Inputs.css';
// Components
import { DatePicker as AntdDatePicker, Icon, Tooltip } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTelegramPlane } from '@fortawesome/free-brands-svg-icons';

import moment from 'moment'

const MultiDatePicker = ({ message, submitMessage }) => {

    let [selectedDates, setSelectedDates] = useState({ individual: [], range: [] });
    let [open, setOpen] = useState(false);


    const renderDate = (curDate, today) => {
        let className = 'antd-date-multi';
        className += curDate.isSame(today, 'month') ? '' : ' fade';
        let element;

        for (let date in selectedDates.individual) {
            if (Math.abs(selectedDates.individual[date].diff(curDate, 'hours')) < 23) {
                className += ' selected individual finish';
            }
        }
        if(curDate.isBefore(moment().startOf('week'))){
          className += ' disabled'
        }
        element = (<div className={className}><span>{curDate.format('D')}</span></div>);
        return addEventHandlers(element, curDate);
    };

    const addEventHandlers = (element, date) => {
        return React.cloneElement(element, {
            onMouseDown: e => dateMouseDown(e, date)
        });
    };

    useEffect(() => {
        function checkValidParent(e) {
            let valid = false;
            e.path.forEach(node => {
                if (node.classList) {
                    if (node.classList.contains('DatepickerCalendar')) {
                        valid = true;
                    }
                }
            });
            if (!valid && open) {
                setOpen(false);
            }
        }

        if (open) {
            console.log('ree');
            window.addEventListener('click', checkValidParent);
        }
        return () => window.removeEventListener('click', checkValidParent);
    }, [setOpen, open]);


    const dateMouseDown = (e, date) => {
        let dates = Object.assign({}, selectedDates);
        if(date.isBefore(moment().startOf('week'), 'week')){
          return
        }
        for(let ind in dates.individual){
          if(dates.individual[ind].isSame(date, 'date')){
            dates.individual.splice(ind, 1)
            setSelectedDates(dates)
            return
          }
        }
        dates.individual = individualCheck(date) ? [...dates.individual, date] : dates.individual;
        setSelectedDates(dates);
        setOpen(true);
    };

    const individualCheck = date => {
        let valid = true;
        selectedDates.individual.forEach(ind => {
            if (date.isSame(ind, 'date')) {
                valid = false;
            }
        });
        return valid;
    };

    const selectedDatesToString = () => {
        let str = '';
        selectedDates.individual.forEach(ind => {
            str += `${ind.format(constants.MOMENT_FORMAT)},`;
        });
        selectedDates.range.forEach(range => {
            str += `${range[0].format(constants.MOMENT_FORMAT)}-${range[1].format(constants.MOMENT_FORMAT)},`;
        });
        return str.substr(0, str.length - 1);
    };

    const inputOnChangeHandler = () => {
        let text;
        if (selectedDates)
            text = selectedDatesToString();

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
                            return document.getElementById('TheSearchBase_Chatbot');
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
