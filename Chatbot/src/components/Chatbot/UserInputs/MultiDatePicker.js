import React, { useEffect, useState } from 'react';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
import * as constants from '../../../constants/Constants';
// Styles
import './styles/Inputs.css';
// Components
import { DatePicker as AntdDatePicker, Tooltip } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTelegramPlane } from '@fortawesome/free-brands-svg-icons';
import { getContainerElement } from '../../helpers';
import moment from 'moment';

const MultiDatePicker = ({ message, submitMessage }) => {

    moment.updateLocale('en', { week: { dow: 1 } });
    let [selectedDates, setSelectedDates] = useState({ individual: [], range: [] });
    let [open, setOpen] = useState(false);
    let [valid, setValid] = useState(true);
    let [error, setError] = useState(null);

    const renderDate = (curDate, today) => {
        let className = 'antd-date-multi';
        className += curDate.isSame(today, 'month') ? '' : ' fade';

        for (let date in selectedDates.individual) {
            if (selectedDates.individual[date].diff)
                if (Math.abs(selectedDates.individual[date].diff(curDate, 'hours')) < 23)
                    className += ' selected individual finish';
        }
        if (curDate.isBefore(moment().startOf('week'))) {
            className += ' disabled';
        }

        const element = (
            <div className={className}>
                <span>{curDate.format('D')}</span>
            </div>
        );

        return React.cloneElement(element, { onMouseDown: e => dateMouseDown(e, curDate) });
    };


    useEffect(() => {
        function checkValidParent(e) {
            if (!open) {
                return;
            }
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
        let dates = Object.assign({}, selectedDates);
        if (date.isBefore(moment().startOf('week'), 'week')) {
            return;
        }
        for (let ind in dates.individual) {
            if (dates.individual[ind].isSame)
                if (dates.individual[ind].isSame(date, 'date')) {
                    dates.individual.splice(ind, 1);
                    setSelectedDates(dates);
                    return;
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

    const delayedOpen = () => {
        setTimeout(() => {
            setOpen(true);
        }, 10);
    };

    const submitDates = () => {
        let text;
        if (selectedDates.individual.length === 0 && selectedDates.range.length === 0) {
            setValid(false);
            setError('You must select at least one date');
            return;
        }
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
            <Tooltip
                placement="top"
                title={error}
                getPopupContainer={() => getContainerElement()}
                visible={!valid}>
                <div className={'DatePickerContainer'} onClick={() => delayedOpen()}>
                    <AntdDatePicker getCalendarContainer={() => getContainerElement()}
                                    className={'Datepicker'} suffixIcon={<div/>}
                                    dropdownClassName={'DatepickerCalendar'}
                                    showToday={false}
                                    dateRender={renderDate}
                                    open={open}/>
                </div>
            </Tooltip>
            <div className={'Submit'}>
                <i className={'SendIconActive'} onClick={submitDates}>
                    <FontAwesomeIcon size="2x" icon={faTelegramPlane} color={valid ? '' : 'red'}/>
                </i>
            </div>
        </React.Fragment>
    );
};

export default MultiDatePicker;
