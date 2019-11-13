import React, { useState } from 'react';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
// Styles
import './styles/Inputs.css';
// Components
import { DatePicker as AntdDatePicker, Tooltip } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTelegramPlane } from '@fortawesome/free-brands-svg-icons';
import { getContainerElement } from '../../helpers';
import moment from 'moment';


const DatePicker = ({ message, submitMessage }) => {
    moment.updateLocale('en', { week: { dow: 1 } });
    let [selectedDate, setSelectedDate] = useState(null);
    let [valid, setValid] = useState(true);
    let [error, setError] = useState(null);

    const inputOnChangeHandler = () => {
        let text;
        console.log(selectedDate);
        if (selectedDate) {
            text = selectedDate;
        } else {
            setValid(false);
            setError('You must select a date');
            return;
        }

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
                <div className={'DatePickerContainer'}>
                    <AntdDatePicker getCalendarContainer={() => getContainerElement()}
                                    className={'Datepicker'} suffixIcon={<div/>}
                                    dropdownClassName={'DatepickerCalendar'}
                                    onChange={(e) => {
                                        if (e)
                                            if (e._isAMomentObject)
                                                setSelectedDate(e.format('L'));
                                            else
                                                setSelectedDate(e.target.value);
                                    }}
                    />
                </div>
            </Tooltip>
            <div className={'Submit'}>
                <i className={'SendIconActive'} onClick={inputOnChangeHandler}>
                    <FontAwesomeIcon size="2x" icon={faTelegramPlane} color={valid ? '' : 'red'}/>
                </i>
            </div>
        </React.Fragment>
    );
};

export default DatePicker;
