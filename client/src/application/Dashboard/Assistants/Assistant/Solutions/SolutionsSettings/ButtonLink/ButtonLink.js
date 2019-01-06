import React from "react";
import {Button, Form, Input, Select} from "antd";
import styles from "../SolutionsSettings.module.less";
import {isEmpty} from "lodash";

const FormItem = Form.Item;
const Option = Select.Option;

class ButtonLink extends React.Component {

    state = {
        webLink: "",
        IDHeader: "",
    };

    static getDerivedStateFromProps(newProps){
        if(this !== undefined) {
            if (!isEmpty(this.props.currentSolution)) {
                if (this.props.currentSolution.Solution.ID === newProps.currentSolution.Solution.ID) {
                    return ({webLink: "", IDHeader: ""});
                }
            }
        }

        if(newProps.currentSolution.Solution === undefined){ return ({webLink: "", IDHeader: ""}); }

        return ({webLink: newProps.currentSolution.Solution.WebLink, IDHeader: newProps.currentSolution.Solution.IDReference});
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if(!err){
                this.props.updateButtonLink(values);
            }
        });
    };

    render(){
        const {getFieldDecorator} = this.props.form;


        return (
            <Form style={{textAlign:"center"}} onSubmit={this.handleSubmit}>
                <p>In order to be able to direct users to your solutions at your home website we will need some input from you.
                    We would need the page part that holds all the solutions and then the solution reference. For example that
                    can be http://mycoolwebsite.com/jobs/JobID* . To create the bridge between us we would need that information
                    in the bellow text inputs. <br />
                    <strong>To do that just contact us and we will find them for you.</strong><br />
                    Alternatively you can try finding them on your own. To do that please provide us with the link (ex. "http://mycoolwebsite.com/jobs/")
                    and then the reference to the JobID which you can find in your upload file(add @ in front of it) or Raw Data bellow.<br />
                    For example: "@JobID" : C2143. <br />You can also take your solution ID and use Ctrl + F on this page to find the
                    corresponding title in the Raw Data.</p>

                <FormItem style={{margin: "15px 0 5px 0"}}>
                    {getFieldDecorator("webLink", {
                        initialValue: this.state.webLink,
                        rules: [{
                            required: true,
                            message: 'Please paste the link without the solution ID here',
                        }],
                    })(
                        <Input className={styles.Input} placeholder={"https://jobwebsite.com/jobs/"}/>
                    )}
                </FormItem>

                <FormItem style={{marginBottom: "5px"}}>
                    {getFieldDecorator("IDHeader", {
                        initialValue: this.state.IDHeader,
                        rules: [{
                            required: true,
                            message: 'Please select the header that holds the job ID',
                        }],
                    })(
                        <Select className={styles.Select} placeholder={"@JobID"}>
                            {
                                this.props.currentSolution.DisplayTitles.map((record, index) => {
                                    return <Option key={index} value={record}>{record}</Option>
                                })
                            }
                        </Select>
                    )}
                </FormItem>
                <Button htmlType={"submit"} className={"ant-btn-primary"} style={{marginTop:"10px"}}>Update</Button>
            </Form>
        )
    }
}

export default Form.create()(ButtonLink)