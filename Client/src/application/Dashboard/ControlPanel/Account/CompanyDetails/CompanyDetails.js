import React from "react";
import {Button, Form, Switch, Input, Divider, Icon, Select} from "antd";
import {isEmpty} from "lodash";
import LogoUploader from "components/LogoUploader/LogoUploader"

const FormItem = Form.Item;
const { Option } = Select;

const selectBeforeURL = (
    <Select defaultValue="http://" style={{ width: 90 }}>
        <Option value="http://">http://</Option>
        <Option value="https://">https://</Option>
    </Select>
);

class CompanyDetails extends React.Component {

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.saveCompanyDetails(values);
            }
        });
    };


    render() {
        const{account, form} = this.props;
        const {getFieldDecorator} = form;

        return (
            <>
                <Form layout='vertical' wrapperCol={{span: 10}} onSubmit={this.handleSubmit}>
                    <h2>Company Details</h2>

                    <FormItem label={"Name"}>
                        {getFieldDecorator("companyName", {
                            initialValue: account?.company?.Name,
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: "Company name is required"
                            }],
                        })(
                            <Input/>
                        )}
                    </FormItem>

                    <FormItem label={"Website URL"}
                    help={`website URL will be used in emails sent on behalf of your company by us`}>
                        {getFieldDecorator('websiteURL', {
                            initialValue: account?.company?.URL,
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: "Please enter your company's website URL!"},
                                    {pattern: /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/,
                                        message: 'Sorry, enter a valid URL'}],
                        })(
                            <Input prefix={<Icon type="global" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                   placeholder="TheSearchBase.com" addonBefore={selectBeforeURL}/>
                        )}
                    </FormItem>


                    <Divider/>
                    <h2>Company Data Sharing Settings:</h2>
                    <h4>This part of the website enables you to control what settings your company may share with us.</h4>
                    <p>
                        Any data that you collect, process and store on TheSearchBase platform is kept secure
                        and confidential at all times. The data that you collect is data that enables our
                        software to work at its optimum level.
                    </p>

                    <br />

                    <FormItem
                        label={"Tracking Data"}
                        extra={"We do not in any way track your company information for marketing purposes. However we would recommend " +
                        "allowing us to contact you if we see that there are ways we could enhance your bot or use of our software."}>
                        {getFieldDecorator("trackData", {
                            initialValue: account?.company?.TrackingData,
                            valuePropName: 'checked',
                        })(
                            <Switch/>
                        )}
                    </FormItem>


                    <FormItem
                        label={"Technical Support"}
                        extra={"Let our team view your errors and problems in order for us to solve your issues."}>
                        {getFieldDecorator("techSupport", {
                            initialValue: account?.company?.TechnicalSupport,
                            valuePropName: 'checked',
                        })(
                            <Switch/>
                        )}
                    </FormItem>

                    <FormItem
                        label={"Account Specialist"}
                        extra={"Let our team contact you to help make recommendations as to how you can make your bots more " +
                        "successful and ways to collect more valuable data. If you don't have a sales specialist, we recommend " +
                        "you enable this so we can help you make the most of our software."}>
                        {getFieldDecorator("accountSpecialist", {
                            initialValue: account?.company?.AccountSpecialist,
                            valuePropName: 'checked',
                        })(
                            <Switch/>
                        )}
                    </FormItem>
                    <br/>
                    <Button htmlType={"submit"} size={'large'} type={'primary'}>Save Changes</Button>
                </Form>

                <br/>
                <Divider/>
                <h2>Company Logo</h2>
                <p>
                    your company logo will replace SearchBase logo in the
                    chatbot and emails sent on behalf of your company by us
                </p>
                <LogoUploader
                    logoPath={account?.company?.LogoPath}
                    uploadLogo={this.props.uploadLogo}
                    deleteLogo={this.props.deleteLogo}/>
            </>
        )
    }
}

export default Form.create()(CompanyDetails)