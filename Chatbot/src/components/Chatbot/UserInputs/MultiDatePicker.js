import React, { useEffect, useState } from 'react';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
// Styles
import './styles/Inputs.css';
// Components
import { DatePicker as AntdDatePicker } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTelegramPlane } from '@fortawesome/free-brands-svg-icons';
import { ETIME } from 'constants';

import { getContainerElement } from '../../helpers';


const addClasses = (date, start, end, temp) => {
    let startCheck = date.isSame(start, 'date');
    let endCheck = date.isSame(end, 'date');
    let firstRangeItem = date.isSame(start.clone().add(1, 'days'), 'date');
    let lastRangeItem = date.isSame(end.clone().subtract(1, 'days'), 'date');

    let className = '';
    className += startCheck ? ' begin' : ''; // start of range
    className += endCheck ? ' finish' : '';  // end of range
    className += firstRangeItem ? ' range-start' : ''; // start of range
    className += lastRangeItem ? ' range-end' : '';  // end of range
        className += temp ? ' temp' : '';
    className += (date.isBetween(start, end) || date.isBetween(end, start)) && !endCheck && !startCheck ? ' range' : ''; // in range

    return className;
};

    const renderDate = (curDate, today) => {
        let className = 'antd-date-multi';
        className += curDate.isSame(today, 'month') ? '' : ' fade';
        let element;
        if (temporaryRange.start && temporaryRange.end) {
            className += addClasses(curDate, temporaryRange.start, temporaryRange.end, true);
        }

        if (selectedDates.range.length !== 0) {
            for (let dateRange in selectedDates.range) {
                className += addClasses(curDate, selectedDates.range[dateRange][0], selectedDates.range[dateRange][1], false);
            }
        }

        for (let date in selectedDates.individual) {
            if (Math.abs(selectedDates.individual[date].diff(curDate, 'hours')) < 23) {
                className += ' selected individual finish';
            }
        }
        let closeIcon = className.indexOf("finish") !== -1 && className.indexOf("temp") === -1 ? true : false
        element = (<div className={className}><span>{curDate.format('D')}</span>{closeIcon ? <span className="delete-range" onClick={() => deleteRange(curDate)}></span> : null}</div>);
        return addEventHandlers(element, curDate);
    };

    const deleteRange = (startDate) => {
      let dates = Object.assign({}, selectedDates)
      for(let date in selectedDates.range){
        if(startDate.isSame(selectedDates.range[date][1], 'date')){
          dates.range.splice(date, 1)
        }
      }
      for(let date in selectedDates.individual){
        if(startDate.isSame(selectedDates.individual[date], 'date')){
          dates.individual.splice(date, 1)
        }
      }
      setSelectedDates(dates)
    }

    const addEventHandlers = (element, date) => {
        return React.cloneElement(element, {
            onMouseDown: e => dateMouseDown(e, date),
            onMouseOver: e => dateMouseOver(e, date),
            onMouseUp: e => dateMouseUp(e, date)
        });
    };

    useEffect(() => {
        console.log(Content);

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
            window.addEventListener('click', checkValidParent);
        }

        return () => window.removeEventListener('click', checkValidParent);
    }, [setOpen, open]);


    const dateMouseDown = (e, date) => {
        setMouseDown(date);
        if(e.target.classList.contains("delete-range")){
          return false;
        }
        if (temporaryRange.start) {
            // click same day
            let dates = Object.assign({}, selectedDates);
            let first = temporaryRange.start.isAfter(temporaryRange.end); // start is after date
            let compare = temporaryRange.reverse ? temporaryRange.end : temporaryRange.start;
            if (Math.abs(date.diff(compare, 'hours')) < 24) {
                dates.individual = individualCheck(date) ? [...dates.individual, date] : dates.individual;
            } else {
                let range = first ? [temporaryRange.end, temporaryRange.start] : [temporaryRange.start, temporaryRange.end];
                dates.range = rangeCheck(range) ? [...dates.range, range] : dates.range;
            }
            setSelectedDates(dates);
            setTemporaryRange({ start: null, end: null, reverse: false });
        } else {
            setTemporaryRange({ start: date, end: null, reverse: false });
        }
        setOpen(true);
    };

    const individualCheck = date => {
        let valid = true;
        selectedDates.range.forEach(range => {
            if (date.isBetween(range[0], range[1]) || date.isSame(range[0], 'date') || date.isSame(range[1], 'date')) {
                valid = false;
            }
        });
        selectedDates.individual.forEach(ind => {
            if (date.isSame(ind, 'date')) {
                valid = false;
            }
        });
        return valid;
    };

    const rangeCheck = rangeIn => {
        let valid = true;

        selectedDates.range.forEach(range => {
            // shorten this maybe lol
            if (rangeIn[0].isBetween(range[0], range[1]) || rangeIn[0].isSame(range[0], 'date') || rangeIn[0].isSame(range[1], 'date')
                || rangeIn[1].isBetween(range[0], range[1]) || rangeIn[1].isSame(range[0], 'date') || rangeIn[1].isSame(range[1], 'date')
                || range[0].isBetween(rangeIn[0], rangeIn[1]) || range[0].isSame(rangeIn[0], 'date') || range[0].isSame(rangeIn[1], 'date')
                || range[1].isBetween(rangeIn[0], rangeIn[1]) || range[1].isSame(rangeIn[0], 'date') || range[1].isSame(rangeIn[1], 'date')) {
                valid = false;
            }
        });

        selectedDates.individual.forEach(ind => {
            if (ind.isBetween(rangeIn[0], rangeIn[1]) ||
                ind.isSame(rangeIn[0], 'date') ||
                ind.isSame(rangeIn[1], 'date')) {
                valid = false;
            }
        });

        return valid;
    };

    const selectedDatesToString = () => {
        let str = '';

        selectedDates.individual.forEach(ind => {
            str += `${ind.format('L')}, `;
        });

        selectedDates.range.forEach(range => {
            str += `${range[0].format('L')}-${range[1].format('L')}, `;
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

    const renderDate = (curDate, today) => {
        const addEventHandlers = (element, date) => {
            const dateMouseUp = () => {
                if (mouseDown) {
                    setMouseDown(null);
                    // setOpen(false)
                }
            };
            const dateMouseOver = (e, date) => {
                if (temporaryRange.start) {
                    if (!temporaryRange.start.isAfter(date) && !temporaryRange.reverse) {
                        setTemporaryRange(obj => ({ ...obj, end: date, reverse: false }));
                    } else if (!temporaryRange.reverse) {
                        setTemporaryRange(obj => ({ end: obj.start, start: date, reverse: true }));
                    } else {
                        setTemporaryRange(obj => ({ ...obj, start: date, reverse: true }));
                    }
                }
            };
            const dateMouseDown = (e, date) => {
                setMouseDown(date);
                if (temporaryRange.start) {
                    // click same day
                    let dates = Object.assign({}, selectedDates);
                    let first = temporaryRange.start.isAfter(temporaryRange.end); // start is after date
                    let compare = temporaryRange.reverse ? temporaryRange.end : temporaryRange.start;

                    if (Math.abs(date.diff(compare, 'hours')) < 24) {
                        dates.individual = individualCheck(date) ? [...dates.individual, date] : dates.individual;
                    } else {
                        let range = first ? [temporaryRange.end, temporaryRange.start] : [temporaryRange.start, temporaryRange.end];
                        dates.range = rangeCheck(range) ? [...dates.range, range] : dates.range;
                    }

                    setSelectedDates(dates);
                    setTemporaryRange({ start: null, end: null, reverse: false });
                } else {
                    setTemporaryRange({ start: date, end: null, reverse: false });
                }
                setOpen(true);
            };

            return React.cloneElement(element, {
                onMouseDown: e => dateMouseDown(e, date),
                onMouseOver: e => dateMouseOver(e, date),
                onMouseUp: e => dateMouseUp(e, date)
            });
        };

        let className = 'antd-date-multi';
        className += curDate.isSame(today, 'month') ? '' : ' fade';
        let element;
        if (temporaryRange.start && temporaryRange.end) {
            className += addClasses(curDate, temporaryRange.start, temporaryRange.end);
        }

        if (selectedDates.range.length !== 0) {
            for (let dateRange in selectedDates.range) {
                className += addClasses(curDate, selectedDates.range[dateRange][0], selectedDates.range[dateRange][1]);
            }
        }

        for (let date in selectedDates.individual) {
            if (Math.abs(selectedDates.individual[date].diff(curDate, 'hours')) < 23) {
                className += ' selected';
            }
        }

        element = (<div className={className}><span>{curDate.format('D')}</span></div>);
        return addEventHandlers(element, curDate);
    };

    return (
        <React.Fragment>

            <div className={'DatePickerContainer'} onClick={() => setOpen(true)}>
                <Tooltip title={'lofl'} visible={open} getTooltipContainer={() => {
                        if (document.getElementById('TheSearchBase_Chatbot_Input'))
                            return document.getElementById('TheSearchBase_Chatbot_Input');
                        else
                            return document.getElementById('TheSearchBase_Chatbot');
                    }}>
                <AntdDatePicker getCalendarContainer={() => getContainerElement()}
                                className={'Datepicker'}
                                suffixIcon={<div/>}
                                dropdownClassName={'DatepickerCalendar'}
                                showToday={false}
                                dateRender={renderDate}
                                open={open}/>
                </Tooltip>
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
