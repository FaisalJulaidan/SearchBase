import React, { useState } from 'react';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
// Styles
import './styles/Inputs.css';
import './SalaryPicker.css';
// Components
import { Slider } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTelegramPlane } from '@fortawesome/free-brands-svg-icons';
import { getContainerElement } from '../../helpers';

const currencySymbols = { 'GBP': '£', 'USD': '$', 'EUR': '€' };

const getDotNotation = (salary, currency) => {
    return new Intl.NumberFormat('en-GB', { style: 'currency', currency, minimumFractionDigits: 0 }).format(salary);
};

const SalaryPicker = ({ message, submitMessage, block_min, block_max, period, currency }) => {

    let [salary, setSalary] = useState([0.3 * block_max, 0.7 * block_max]);

    const submitSalary = () => {
        let afterMessage = message.block[flowAttributes.CONTENT][flowAttributes.CONTENT_AFTER_MESSAGE];
        let type = messageTypes.TEXT;
        let block = message.block;
        let salaries = salary.map(salary => getDotNotation(salary, currency));
        let text = `Between ${salaries[0]} and ${salaries[1]} ${period}`;
        let newState = {
            curAction: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_ACTION],
            curBlockID: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_BLOCKTOGOID],
            waitingForUser: false
        };
        submitMessage(text, type, newState, afterMessage, block, {
            skipped: false,
            input: `${salary[0]}-${salary[1]} ${currency} ${period}`
        });
    };

    const onChangeHandler = (val) => {
        const roundTo25 = (num) => {
            let count = Math.round(num / 10);
            return count * 10;
        };
        setSalary([roundTo25(val[0]), roundTo25(val[1])]);
    };

    const tipFormatter = (val) => `${getDotNotation(val, currency)}`;

    return (
        <React.Fragment>
            <div className={'InputContainer'}>
                <Slider range={true}
                        getTooltipPopupContainer={() => getContainerElement()}
                        tipFormatter={tipFormatter}
                        value={salary}
                        onChange={onChangeHandler}
                        min={block_min}
                        max={block_max}
                        className={'Slider'}
                        marks={{
                            [block_min]: `${currencySymbols[currency]}${block_min}`,
                            [block_max]: `${currencySymbols[currency]}${block_max}`
                        }}/>
            </div>

            <div className={'SubmitWrapper'} onClick={submitSalary}>
                <div className={'Actions'}>
                    <p>{period}</p>
                </div>

                <div className={'Submit'}>
                    <i className={'SendIconActive'}>
                        <FontAwesomeIcon size="2x" icon={faTelegramPlane}/>
                    </i>
                </div>
            </div>
        </React.Fragment>
    );
};

export default SalaryPicker;
