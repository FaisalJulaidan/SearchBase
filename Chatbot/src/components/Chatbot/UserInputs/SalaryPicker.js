import React, {useEffect, useState} from 'react';
// Constants
import * as messageTypes from '../../../constants/MessageType';
import * as flowAttributes from '../../../constants/FlowAttributes';
// Styles
import './styles/Inputs.css';
// Components
import {Dropdown, Icon, Menu, Popover, Slider} from 'antd';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faTelegramPlane} from '@fortawesome/free-brands-svg-icons';

const currencySymbols = { 'GBP': '£', 'USD': '$', 'EUR': '€' };

const getDotNotation = (val, currency) => {
    return new Intl.NumberFormat('en-GB', { style: 'currency', currency, minimumFractionDigits: 0 }).format(val);
};

const SalaryPicker = ({ message, submitMessage }) => {

    let [payRate, setPayRate] = useState('Daily');
    let [min, setMin] = useState(0);
    let [max, setMax] = useState(2000);
    let [salary, setSalary] = useState([0.3 * max, 0.7 * max]);
    let [currency, setCurrency] = useState('GBP');

    const submitSalary = () => {
        let afterMessage = message.block[flowAttributes.CONTENT][flowAttributes.CONTENT_AFTER_MESSAGE];
        let type = messageTypes.TEXT;
        let block = message.block;
        let salaries = salary.map(salary => getDotNotation(salary, currency));
        let text = `Between ${salaries[0]} and ${salaries[1]}`;
        let newState = {
            // curAction: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_ACTION],
            curBlockID: message.block[flowAttributes.CONTENT][flowAttributes.USER_INPUT_BLOCKTOGOID],
            waitingForUser: false
        };
        submitMessage(text, type, newState, afterMessage, block, {
            skipped: false,
            input: `${salary[0]}-${salary[1]} ${currency} ${payRate}`
        });
    };

    useEffect(() => {
        let newMin = payRate === 'Daily' ? 0 : 15000;
        let newMax = payRate === 'Daily' ? 2000 : 200000;
        setMin(newMin);
        setMax(newMax);
        setSalary([0.3 * newMax, 0.7 * newMax]);
    }, [payRate]);

    const changePayRate = (item) => {
        setPayRate(item.item.props.value);
    };

    const payRateMenu = () => {
        return (<Menu onClick={changePayRate}>
            <Menu.Item value="Daily" key={1}>Daily</Menu.Item>
            <Menu.Item value="Annual" key={2}>Annual</Menu.Item>
        </Menu>);
    };

    const changeCurrency = (item) => {
        setCurrency(item.item.props.value);
    };


    const onChangeHandler = (val) => {
        const roundTo25 = (num) => {
            let count = Math.round(num / 25);
            return count * 25;
        };
        setSalary([roundTo25(val[0]), roundTo25(val[1])]);
    };

    const currencyMenu = () => {
        return (<Menu onClick={changeCurrency}>
            <Menu.Item value="GBP" key={1}>GBP</Menu.Item>
            <Menu.Item value="USD" key={2}>USD</Menu.Item>
            <Menu.Item value="EUR" key={3}>EUR</Menu.Item>
        </Menu>);
    };

    const payRateSliderMarks = () => {
        if (payRate === 'Daily') {
            return {
                0: `${currencySymbols[currency]}0`,
                2000: `${currencySymbols[currency]}2000`
            };
        } else {
            return {
                15000: `${currencySymbols[currency]}15000`,
                200000: `${currencySymbols[currency]}200000`
            };
        }
    };
    const tipFormatter = (val) => {
        let commaValue = getDotNotation(val, currency);
        return `${commaValue}`;
    };

    const settingsDialog = (
        <div className={'Settings'}>
            <h1 className={'SettingsTitle'}>Settings</h1>
            <div>
                <h2 className={'SettingsOption'}>Currency</h2>
                <Dropdown overlay={currencyMenu}
                          getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}>

                    <a className="ant-dropdown-link" href="#a">
                        {currency} <Icon type="down"/>
                    </  a>
                </Dropdown>
                <h2 className={'SettingsOption'}>Pay rate</h2>
                <Dropdown getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}
                          overlay={payRateMenu}>
                    <a className="ant-dropdown-link" href="#a">
                        {payRate} <Icon type="down"/>
                    </a>
                </Dropdown>
            </div>
        </div>
    );


    return (
        <React.Fragment>
            <div className={'InputContainer'}>
                <Slider
                    getTooltipPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}
                    range={true}
                    tipFormatter={tipFormatter}
                    value={salary}
                    onChange={onChangeHandler}
                    min={min}
                    max={max}
                    className={'Slider'}
                    marks={payRateSliderMarks()}/>
            </div>
            <div className={'Actions'}>
                <Popover
                    content={settingsDialog}
                    placement="top"
                    getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}
                    trigger={'click'}>
                    <i>
                        <Icon
                            type="setting"
                            theme="outlined"
                            style={{ fontSize: '22px' }}/>
                    </i>
                </Popover>
            </div>
            <div className={'Submit'}>
                <i className={'SendIconActive'} onClick={submitSalary}>
                    <FontAwesomeIcon size="2x" icon={faTelegramPlane}/>
                </i>
            </div>
        </React.Fragment>
    );
};

export default SalaryPicker;
