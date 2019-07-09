import React from 'react'
import styles from './Input.module.css'
import {constants} from '../../../utilities/constants';
import {Validators} from '../../../utilities/validators';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faTelegramPlane} from '@fortawesome/free-brands-svg-icons'
import {DatePicker, Icon, Input as AntdInput, Progress, Select, Tooltip} from 'antd';
import {connect} from 'react-redux';
import * as actionTypes from '../../../store/actions';

import 'antd/lib/icon/style';
import 'antd/lib/tooltip/style';
import 'antd/lib/progress/style';
import 'antd/lib/input/style';
import 'antd/lib/select/style';

import 'antd/dist/antd.less'
import './Input.css'


const {Option} = Select;

class Input extends React.Component {

    state = {
        inputText: '',
        progressBarPercent: 0,
        isFileUploading: false,
        file: undefined,
        isValidInput: true,
        isValidFileExt: true,
        errorMsg: undefined,

        range: 'Greater Than',
        currency: 'USD',
        payPeriod: 'Monthly'
    };

    validators = Object.create(Validators);

    inputSubmitHandler = () => {
        const inputText = this.state.inputText.trim();
        const {inputSubmitted} = this.props;

        /**
         * I added this if statement to check the inputText even if there is no inputText
         * to check the others like range & payPeriod
         * I could've remove this line (inputText !== "")
         * But I was afraid of break others cases
         * This is why we need a testing for this :(
         * */
        if (this.props.currentBlock.DataType.validation === constants.SALARY) {
            if (!this.state.currency || !this.state.range || !this.state.payPeriod || !inputText)
                this.setState({isValidInput: false, errorMsg: 'Select currency and range and salary type'});
            else {
                const input = `${this.state.range} ${inputText} ${this.state.currency} ${this.state.payPeriod}`;
                inputSubmitted(input, [input]);
            }
        } else if (inputText !== "" && !(this.props.isBotTyping)) {
            switch (this.props.currentBlock.DataType.validation) {
                case constants.EMAIL:
                    if (!(this.validators.isValidEmail(inputText))) {
                        this.setState({isValidInput: false, errorMsg: 'Invalid email'});
                        return;
                    }
                    inputSubmitted(inputText, [inputText]);
                    break;
                case constants.TELEPHONE:
                    if (!(this.validators.isValidTelephone(inputText))) {
                        this.setState({isValidInput: false, errorMsg: 'Invalid phone number'});
                        return;
                    }
                    inputSubmitted(inputText, [inputText]);
                    break;
                case constants.STRING:
                    if (!(this.validators.isValidString(inputText))) {
                        this.setState({isValidInput: false, errorMsg: "Don't only use numbers"});
                        return;
                    }
                    inputSubmitted(inputText, inputText.split(' ').filter(n => n));
                    break;
                case constants.NUMBER:
                    if (!(this.validators.isValidNumber(inputText))) {
                        this.setState({isValidInput: false, errorMsg: 'Numbers only accepted'});
                        return;
                    }
                    inputSubmitted(inputText, [inputText]);
                    break;
                case constants.URL:
                    if (!(this.validators.isValidURL(inputText))) {
                        this.setState({isValidInput: false, errorMsg: 'Invalid URL'});
                        return;
                    }
                    inputSubmitted(inputText, [inputText]);
                    break;
                default:
                    inputSubmitted(inputText, inputTextstring.trim().split(' '));
            }
            this.setState({inputText: ''});
            // if we set botIsTyping to true it means user cannot submit multiple input unless bot responded
            this.props.onIsBotTypingUpdate(true) // << This fix spamming
        }
    };

    inputOnChangeHandler = (e) => {
        if (e)
            if (e._isAMomentObject)
                this.setState({
                    inputText: e.format('L'),
                    isValidInput: true,
                    isValidFileExt: true
                });
            else
                this.setState({
                    inputText: e.target.value,
                    isValidInput: true,
                    isValidFileExt: true
                });
    };

    fileOnChangeHandler = (e) => {
        // Validate file type (extension)
        const file = e.target.files[0];
        const typesArr = this.props.currentBlock.Content.fileTypes;
        if (!(this.validators.isValidFile(file.name, typesArr))) {
            this.setState({isValidFileExt: false, errorMsg: 'Allowed types: ' + typesArr.join(', ')});
            console.log("invalid file type");
            return;
        }
        this.setState({file, isValidFileExt: true, errorMsg: undefined});
    };

    fileUploadHandler = (e) => {
        const file = this.state.file;
        if (file && this.state.isValidFileExt) {
            // Show progress bar for good user experience
            let percent = this.state.progressBarPercent;
            const interval = setInterval(() => {
                this.setState({
                        progressBarPercent: ++percent,
                        isFileUploading: true
                    },
                    () => checkProgressBar(110));
            }, 30);

            const checkProgressBar = (target) => {
                if (percent === target) {
                    // After progress bar is 100% complete,
                    // send file to chatbot.js (parent) to handle it
                    clearInterval(interval);
                    this.props.fileSubmitted(file);
                    this.setState({
                        isFileUploading: false,
                        file: null,
                        progressBarPercent: 0,
                        inputText: ''
                    });
                }
            }
        }
    };

    onKeyPressHandler = (e) => {
        // When user click enter while focusing on the input field
        if (e.key === 'Enter') {
            this.inputSubmitHandler();
        }
    };


    render() {
        let input = null;
        switch (this.props.currentBlock.Type) {
            case constants.QUESTION:
                input = (
                    <React.Fragment>
                        <input className={styles.Text} type="text" disabled
                               value="" onChange={this.inputOnChangeHandler}
                               placeholder={"Select an answer..."}
                        />
                        <div className={styles.Actions}>
                            <i><Icon type="paper-clip" theme="outlined" style={{fontSize: '22px'}}/></i>
                            <i><FontAwesomeIcon size="2x" icon={faTelegramPlane}/></i>
                        </div>
                    </React.Fragment>
                );

                break;
            case constants.USER_INPUT:
                const salaryInput = (
                    <AntdInput className={styles.Salary}
                               type="number"
                               placeholder={'Eg. 5000'}
                               disabled={this.props.isBotTyping}
                               onKeyPress={(e) => this.onKeyPressHandler(e)}
                               onChange={this.inputOnChangeHandler}
                               addonBefore={
                                   <Select defaultValue="Greater Than"
                                           dropdownClassName={'salaryDropdown'}
                                           onSelect={(val) => this.setState({range: val})}
                                           getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}>
                                       <Option value="Greater Than">Greater</Option>
                                       <Option value="Less Than">Less</Option>
                                   </Select>
                               }
                               addonAfter={
                                   <>
                                       <Select defaultValue="USD"
                                               style={{marginRight: 0}}
                                               onSelect={(val) => this.setState({currency: val})}
                                               getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}
                                               dropdownClassName={'salaryDropdown'}>
                                           {
                                               this.props.currencies.map((currency, i) =>
                                                   <Option value={currency} key={i}>{currency}</Option>
                                               )
                                           }
                                       </Select>
                                       <Select defaultValue={this.state.payPeriod}
                                               dropdownClassName={'salaryDropdown'}
                                               onSelect={(val) => this.setState({payPeriod: val})}
                                               getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}>
                                           <Option value={'Monthly'}>Monthly</Option>
                                           <Option value={'Annually'}>Annually</Option>
                                       </Select>
                                   </>
                               }
                    />
                );
                const datepickerInput = (
                    <DatePicker getCalendarContainer={() => document.getElementById('TheSearchBase_Chatbot')}
                                className={styles.Datepicker} suffixIcon={<div/>}
                                dropdownClassName={styles.DatepickerCalendar}
                                onChange={this.inputOnChangeHandler}
                    />
                );
                const generalInput = (
                    <input className={styles.Text}
                           type="text"
                           disabled={this.props.isBotTyping}
                           value={this.state.inputText}
                           onChange={this.inputOnChangeHandler}
                           onKeyPress={(e) => this.onKeyPressHandler(e)}
                           placeholder={"Type your message here..."}
                           ref={input => input && input.focus() && !this.props.isBotTyping}
                    />
                );
                input = (
                    <React.Fragment>
                        <Tooltip placement="top" title={this.state.errorMsg}
                                 getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}
                                 visible={!this.state.isValidInput}>
                            <>
                                {
                                    this.props.currentBlock.DataType.validation === "Salary" &&
                                    salaryInput
                                }

                                {
                                    this.props.currentBlock.DataType.validation === "DateTime" &&
                                    datepickerInput
                                }

                                {
                                    this.props.currentBlock.DataType.validation !== "Salary" &&
                                    this.props.currentBlock.DataType.validation !== "DateTime" &&
                                    generalInput
                                }
                            </>
                        </Tooltip>
                        {/* Icons */}
                        <div className={styles.Actions}>
                            <i className={styles.SendIconActive}
                               onClick={this.inputSubmitHandler}>
                                <FontAwesomeIcon size="2x" icon={faTelegramPlane}
                                                 color={this.state.isValidInput ? "" : "red"}
                                />
                            </i>
                        </div>
                    </React.Fragment>
                );
                break;
            case constants.FILE_UPLOAD:
                input = this.state.isFileUploading ? (
                    <React.Fragment>
                        <div className={styles.Progress}>
                            <Tooltip placement="top" title={this.state.file.name} visible
                                     getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}>
                                <Progress percent={this.state.progressBarPercent} showInfo={false}/>
                            </Tooltip>
                        </div>
                    </React.Fragment>
                ) : (
                    <React.Fragment>
                        <input
                            className={styles.Text} type="text" disabled
                            value={this.state.file ? this.state.file.name : "Attach your file..."}
                            onChange={this.inputOnChangeHandler}
                            placeholder={"Attach your file..."}
                        />
                        {/* Icons */}
                        <div className={styles.Actions}>
                            <Tooltip placement="topRight"
                                     getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}
                                     title={this.state.errorMsg}
                                     visible={!this.state.isValidFileExt}>
                                {/* ClipIcon */}
                                <i className={styles.ClipIconActive} onClick={() => this.fileInput.click()}>
                                    <input ref={(el) => this.fileInput = el} value="" type="file"
                                           disabled={!this.state.isValidInput}
                                           onChange={this.fileOnChangeHandler}/>
                                    <Icon type="paper-clip" theme="outlined"
                                          style={this.state.isValidFileExt ? {fontSize: '22px'} : {
                                              color: 'red',
                                              fontSize: '22px'
                                          }}/>
                                </i>
                            </Tooltip>
                            {/*SendIcon */}
                            <i className={styles.SendIconActive} onClick={this.fileUploadHandler}>
                                <FontAwesomeIcon size="2x" icon={faTelegramPlane}/>
                            </i>
                        </div>
                    </React.Fragment>
                );
                break;
        }
        return (
            <div className={styles.Input}>
                {/* {this.props.isBotTyping ? null : input} */}
                {input}
            </div>
        );
    }

}

const mapStateToProps = state => {
    return {
        isBotTyping: state.isBotTyping
    }
};

const mapDispatchToProps = dispatch => {
    return {
        onIsBotTypingUpdate: (value) => {
            dispatch({type: actionTypes.UPDATE_IS_BOT_TYPING, payload: {value}});
            return Promise.resolve();
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Input);
