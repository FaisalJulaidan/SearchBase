import React from 'react';
import { Button, Form, Input, Switch, Divider, Icon, AutoComplete } from 'antd';
import ChangePassword from './ChangePassword';
import moment from 'moment-timezone';


const FormItem = Form.Item;

const tz = moment.tz.names();

class ProfileDetails extends React.Component {

    state = {
        name: '',
        email: '',
        companyName: '',
        tzList: [],
        narrowSearch: false
    };
    //

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.saveProfileDetails(values);
            }
        });
    };

    searchTimezone = (input) => {
        let filter = tz.filter(timezone => timezone.toLowerCase().indexOf(input.toLowerCase()) !== -1);
        this.setState({ tzList: filter.slice(0, 10), narrowSearch: filter.length > 10 });
    };


    render() {
        const { account, form } = this.props;
        const { getFieldDecorator } = form;

        return (

            <>
                <Form layout='vertical' wrapperCol={{ span: 10 }} onSubmit={this.handleSubmit}>
                    <h2>Profile Details</h2>
                    <FormItem label={'First Name'}>
                        {getFieldDecorator('firstname', {
                            initialValue: account?.user?.Firstname,
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: 'Please enter your first'
                            }]
                        })(
                            <Input/>
                        )}
                    </FormItem>

                    <FormItem label={'Surname'}>
                        {getFieldDecorator('surname', {
                            initialValue: account?.user?.Surname,
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: 'Please enter your surname'
                            }]
                        })(
                            <Input/>
                        )}
                    </FormItem>

                    <FormItem
                        label={'Email'}
                        extra={'For your security, we have temporarily disabled this box'}>
                        {getFieldDecorator('email', {
                            initialValue: account?.user?.Email,
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: 'Please enter a valid email'
                            }]
                        })(
                            <Input disabled={true} readOnly={true}/>
                        )}
                    </FormItem>

                    <FormItem
                        label={'Phone Number'}>
                        {getFieldDecorator('phoneNumber', {
                            initialValue: account?.user?.PhoneNumber,
                            rules: [{ required: false, message: 'Please enter a valid email' },
                                {
                                    pattern: /^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$/,
                                    message: 'Invalid phone number'
                                }
                            ]
                        })(
                            <Input prefix={<Icon type="phone" style={{ color: 'rgba(0,0,0,.25)' }}/>}
                                   placeholder="+44 7502719493"/>
                        )}
                    </FormItem>

                    <FormItem
                        label={'Timezone'}
                        help={'We\'ve guessed a default for you, however if you\'d like to change it simply enter the Continent/City you\'re from and select from the list!' +
                        ' If you cant find the country you\'re looking for on the list, try a more specific search.'}>
                        {getFieldDecorator('timeZone', {
                            initialValue: account?.user?.TimeZone,
                            rules: [{
                                validator: (rule, val, callback) => {
                                    if (!tz.includes(val)) {
                                        callback('Timezone must be identical to one on the list!');
                                    } else {
                                        callback();
                                    }
                                }
                            }]
                        })(
                            <AutoComplete
                                dataSource={this.state.tzList}
                                onSearch={this.searchTimezone}
                                placeholder="Please search for a timezone"
                            />
                        )}
                    </FormItem>

                    <FormItem
                        label={'Chatbot Email Notifications'}
                        extra={'If switched on, we will send you notifications via email with users that have interacted with the chatbot.  ' +
                        'You can change the frequency of the notifications from the assistant settings page. '}>
                        {getFieldDecorator('chatbotNotifications', {
                            initialValue: account?.user?.ChatbotNotifications,
                            valuePropName: 'checked'
                        })(
                            <Switch onChange={this.handleChangeStatNotifications}
                                    style={{ marginRight: '5px' }}/>
                        )}
                    </FormItem>

                    <FormItem
                        label={'Newsletters'}
                        extra={'We would like to keep you updated with the latest software updates and features available to\n' +
                        'you, If you decide to not subscribe you may miss on important features and announcements.'}>
                        {getFieldDecorator('newsletters', {
                            initialValue: account?.newsletters,
                            valuePropName: 'checked'
                        })(
                            <Switch onChange={this.handleChangeNewsletters}
                                    style={{ marginRight: '5px' }}/>
                        )}
                    </FormItem>

                    <br/>
                    <Button htmlType={'submit'} size={'large'} type={'primary'}>Save Changes</Button>
                </Form>

                <Divider/>
                <h2>Password Update</h2>
                <ChangePassword savePassword={this.props.savePassword}/>
            </>

        );
    }
}

export default Form.create()(ProfileDetails);