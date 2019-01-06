import React from "react";
import {Button, Form, Select} from "antd";
import styles from "../SolutionsSettings.module.less";
import QueueAnim from "rc-queue-anim";
import {isEmpty} from "lodash";

const FormItem = Form.Item;
const Option = Select.Option;

class ITDForm extends React.Component {

    state = {
        chosenDisplays: [],
    };

    addNewDisplaySelect = () => {
        let chosenDisplays = [...this.state.chosenDisplays];
        chosenDisplays.push(undefined);
        this.setState({chosenDisplays: chosenDisplays});
    };

    static getDerivedStateFromProps(newProps){
        if(newProps.currentSolution.Solution === undefined){ return ({chosenDisplays: []}); }
        if(newProps.currentSolution.Solution.DisplayTitles === null){ return ({chosenDisplays: []}); }

        const chosenDisplays = [...newProps.currentSolution.Solution.DisplayTitles.titleValues];
        return ({chosenDisplays: chosenDisplays});
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if(!err){
                this.props.updateInformationToDisplay(values);
            }
        });
    };

    render(){
        const {getFieldDecorator} = this.props.form;

        return (
            <Form style={{textAlign:"center"}} onSubmit={this.handleSubmit}>
                <p>From here you can choose which part of your information you want to be displayed inside the solution box.
                    If you are unsure what data is inside those titles simply have a look at the Raw Data section.</p>
                <Button className={styles.Button} type="primary" onClick={this.addNewDisplaySelect}>Add More Information</Button>
                <QueueAnim>
                {
                    this.state.chosenDisplays.map((record, index) => {
                        return (
                            <FormItem style={{marginBottom: "5px"}} key={index}>
                                {getFieldDecorator("displaySelect" + String(index), {
                                    initialValue: record,
                                    rules: [{
                                        required: true,
                                        message: 'Please select a header',
                                    }],
                                })(
                                    <Select className={styles.Select}>
                                        {
                                            this.props.currentSolution.DisplayTitles.map((record, index) => {
                                                return <Option key={index} value={record}>{record}</Option>
                                            })
                                        }
                                    </Select>
                                )}
                            </FormItem>
                        )
                    })
                }
                </QueueAnim>
                <Button htmlType={"submit"} className={"ant-btn-primary"} style={{marginTop:"10px"}}>Update</Button>
            </Form>
        )
    }
};

export default Form.create()(ITDForm)