import React, {useState} from 'react';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
// Styles
import './styles/Inputs.css';
// Components
import {DatePicker} from 'antd';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faTelegramPlane} from '@fortawesome/free-brands-svg-icons';
// import Tooltip from '../../generic/Tooltip'

const {RangePicker} = DatePicker;

const SalaryPicker = ({message, submitMessage}) => {

    let [settings, setSettings] = useState(false);
    let [selectedDate, setSelectedDate] = useState(null);

    const inputOnChangeHandler = () => {
        let text;
        if (selectedDate)
            text = selectedDate;

        let afterMessage = message.block[flowAttributes.CONTENT][flowAttributes.CONTENT_AFTER_MESSAGE];
        let type = messageTypes.TEXT;
        let block = message.block;

        let newState = {
            curBlockID: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_BLOCKTOGOID],
            waitingForUser: false
        };

        submitMessage(text, type, newState, afterMessage, block, {
            skipped: false,
            input: text
        });

    };

    return (
        <React.Fragment>

            <DatePicker getCalendarContainer={() => document.getElementById('TheSearchBase_Chatbot_Input')}
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
            <div className={'Submit'}>
                <i className={'SendIconActive'} onClick={inputOnChangeHandler}>
                    <FontAwesomeIcon size="2x" icon={faTelegramPlane}/>
                </i>
            </div>
        </React.Fragment>
    );
};

export default SalaryPicker;
