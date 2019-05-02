import React from 'react';
import {Button, Icon, Input, Select, Modal, Slider, Switch, Row, Col} from "antd";

const {Option} = Select;


const AdaptFormItems = ({FormItem, layout, getFieldDecorator}) => {
    return (
        <div>
            <FormItem label="Domain"
                      {...layout}>
                {getFieldDecorator('domain', {
                    rules: [{
                        required: true,
                        message: "Please add your domain name",
                    }],
                })(
                    <Input placeholder={'Your Domain'}/>
                )}
            </FormItem>

            <FormItem label="Username"
                      {...layout}>
                {getFieldDecorator('username', {
                    rules: [{
                        required: true,
                        max: 20,
                        message: "Username is required, and should be less than or 20 character",
                    }],
                })(
                    // To readOnly to avoid autocomplete
                    <Input readOnly
                           onFocus={elem => elem.target.removeAttribute('readonly')}
                           placeholder={'Login of user to use for authentication'}/>
                )}
            </FormItem>

            <FormItem label="Password"
                      {...layout}>
                {getFieldDecorator('password', {
                    rules: [{
                        required: true,
                        max: 32,
                        message: "Password is required, and should be less than or 32 character",
                    }],
                })(
                    // To readOnly to avoid autocomplete
                    <Input readOnly
                           onFocus={elem => elem.target.removeAttribute('readonly')}
                           prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                           placeholder={"User's password"} type="password"/>
                )}
            </FormItem>

            <FormItem label="Profile"
                      {...layout}>
                {getFieldDecorator('profile', {
                    rules: [{
                        required: true,
                        message: "Profile is required field",
                    }],
                })(
                    <Input placeholder={"Profile to use (e.g. CoreProfile)"}/>
                )}
            </FormItem>

            <FormItem label="Locale" {...layout}>
                {getFieldDecorator('locale', {
                    rules: [{
                        required: true,
                        message: "Locale is required field",
                    }],
                })(
                    <Input placeholder={"Locale is like: en_GB"}/>
                )}
            </FormItem>

            <FormItem label="Timezone"
                      {...layout}>
                {getFieldDecorator('timezone', {
                    rules: [{
                        required: true,
                        message: "Timezone is required field",
                    }],
                })(
                    <Input placeholder={"Time zone identifier (e.g. GMT)"}/>
                )}
            </FormItem>

            <FormItem label="Date Format"
                      {...layout}>
                {getFieldDecorator('dateFormat', {
                    rules: [{
                        required: true,
                        message: "Date Format is required field",
                    }],
                })(
                    <Select placeholder={'Select one of the Date Formats'}>
                        <Option value="0">0 – default</Option>
                        <Option value="1">1 – Long</Option>
                        <Option value="2">2 – Medium</Option>
                        <Option value="3">3 – Short</Option>
                    </Select>
                )}
            </FormItem>


            <FormItem label="Time Format"
                      {...layout}>
                {getFieldDecorator('timeFormat', {
                    rules: [{
                        required: true,
                        message: "Time Format is required field",
                    }],
                })(
                    <Select placeholder={'Select one of the Time Formats'}>
                        <Option value="0">0 – Full</Option>
                        <Option value="1">1 – Long</Option>
                        <Option value="2">2 – Medium</Option>
                        <Option value="3">3 – Short</Option>
                    </Select>
                )}
            </FormItem>
        </div>
    )
};

export default AdaptFormItems
