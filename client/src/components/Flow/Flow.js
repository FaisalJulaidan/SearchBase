import React, {Component} from 'react';
import "./Flow.less"
import styles from "./Flow.module.less";
import {Avatar, Button, Card, Collapse, Drawer, Form, Icon, Input, List, Select, Tabs} from "antd";
import {arrayMove, SortableContainer, SortableElement} from 'react-sortable-hoc';


const Panel = Collapse.Panel;
const TabPane = Tabs.TabPane;

const data = [
    {title: 'Greetings Group'},
    {title: 'Clients Group'},
    {title: 'Job Finders Group'},
    {title: 'Ending Group'},
];

const FormItem = Form.Item;
const Option = Select.Option;

function callback(key) {
    console.log(key);
}

const SortableItem = SortableElement(({value, key}) =>
    <Collapse bordered={true}>
        <Panel header={value} key={key}>
            <Card title="Uesr Input" style={{width: '100%'}}>
                {value}
            </Card>
        </Panel>
    </Collapse>
);

const SortableList = SortableContainer(({items}) => {
    return (
        <div>
            {items.map(
                (value, index) => (
                    <SortableItem key={`item-${index}`} index={index} value={value}/>
                )
            )}
        </div>
    );
});

/*
*
* Todo:
*   1- split Flow into components
*   2- design card for each tab type
*   3- design add group modal
*   4- make collapse list reorder-able (DONE)
* */

class Flow extends Component {

    state = {visible: false, items: ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6'],};

    onSortEnd = ({oldIndex, newIndex}) => {
        this.setState({
            items: arrayMove(this.state.items, oldIndex, newIndex),
        });
        console.log(this.state.items)
    };


    showDrawer = () => {
        this.setState({
            visible: true,
        });
    };

    onClose = () => {
        this.setState({
            visible: false,
        });
    };


    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;

        return (
            <div style={{height: '100%'}}>

                <div style={{padding: '0 5px'}}>
                    <div style={{width: '100%', height: 56, marginBottom: 10}}>
                        <div className={styles.Panel}>
                            <div className={styles.Header}>
                                <div>
                                    <h3>Assistant Name</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style={{height: 'calc(100% - 66px)', width: '100%', display: 'flex'}}>
                    <div style={{margin: 5, width: '30%'}}>
                        <div className={styles.Panel}>
                            <div className={styles.Header}>
                                <div>
                                    <h3>Flow Groups</h3>
                                </div>
                                <div>
                                    <Button className={styles.PanelButton} type="primary" icon="plus">
                                        Add Group
                                    </Button>
                                </div>
                            </div>

                            <div className={styles.Body}>
                                <List
                                    itemLayout="horizontal"
                                    dataSource={data}
                                    renderItem={item => (
                                        <List.Item>
                                            <List.Item.Meta
                                                avatar={<Avatar icon="ordered-list"
                                                                style={{backgroundColor: '#9254de'}}/>}
                                                title={<a href="/">{item.title}</a>}
                                                description="This groupe is to do xyz and xyz"
                                            />
                                        </List.Item>
                                    )}
                                />
                            </div>

                        </div>
                    </div>

                    <div style={{margin: 5, width: '70%'}}>
                        <div className={styles.Panel}>
                            <div className={styles.Header}>
                                <div>
                                    <h3>Blocks</h3>
                                </div>
                                <div>
                                    <Button className={styles.PanelButton} type="primary" icon="plus"
                                            onClick={this.showDrawer}>
                                        Add Block
                                    </Button>
                                </div>
                            </div>

                            <div className={styles.Body}>
                                <Drawer
                                    title="Configure Block"
                                    placement="right"
                                    mask={false}
                                    onClose={this.onClose}
                                    visible={this.state.visible}
                                    width={'45%'}>
                                    <Tabs onChange={callback} type="card" tabPosition={'right'}>
                                        <TabPane tab={<span><Icon type="form"/>User Input</span>} key="1">
                                            <Card
                                                title="Uesr Input"
                                                extra={<Button type="primary" icon="plus" onClick={this.onClose}>
                                                    Add Block</Button>}
                                                style={{width: '100%'}}>

                                                <Form layout='horizontal'>
                                                    <FormItem
                                                        label="Question"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Where are you from?"/>
                                                    </FormItem>

                                                    <FormItem {...formItemLayout}
                                                              label="Validation">

                                                        <Select placeholder="Will validate the input">
                                                            <Option value="recruitment">Ignore</Option>
                                                            <Option value="Shopping">Email</Option>
                                                            <Option value="Sales">Full Name</Option>
                                                        </Select>
                                                    </FormItem>

                                                    <FormItem
                                                        label="After message"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Your input is considered"/>
                                                    </FormItem>


                                                </Form>
                                            </Card>
                                        </TabPane>
                                        <TabPane tab={<span><Icon type="question-circle"/>Question</span>} key="2">

                                            <Card
                                                title="Question"
                                                extra={<Button type="primary" icon="plus" onClick={this.onClose}>
                                                    Add Block</Button>}
                                                style={{width: '100%'}}>

                                                <Form layout='horizontal'>
                                                    <FormItem
                                                        label="Question"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Where are you from?"/>
                                                    </FormItem>

                                                    <FormItem {...formItemLayout}
                                                              label="Validation">

                                                        <Select placeholder="Will validate the input">
                                                            <Option value="recruitment">Ignore</Option>
                                                            <Option value="Shopping">Email</Option>
                                                            <Option value="Sales">Full Name</Option>
                                                        </Select>
                                                    </FormItem>

                                                    <FormItem
                                                        label="After message"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Your input is considered"/>
                                                    </FormItem>

                                                </Form>
                                            </Card>

                                        </TabPane>
                                        <TabPane tab={<span><Icon type="file-add"/>File Upload</span>} key="3">
                                            <Card
                                                title="File Upload"
                                                extra={<Button type="primary" icon="plus" onClick={this.onClose}>
                                                    Add Block</Button>}
                                                style={{width: '100%'}}>

                                                <Form layout='horizontal'>
                                                    <FormItem
                                                        label="Question"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Where are you from?"/>
                                                    </FormItem>

                                                    <FormItem {...formItemLayout}
                                                              label="Validation">

                                                        <Select placeholder="Will validate the input">
                                                            <Option value="recruitment">Ignore</Option>
                                                            <Option value="Shopping">Email</Option>
                                                            <Option value="Sales">Full Name</Option>
                                                        </Select>
                                                    </FormItem>

                                                    <FormItem
                                                        label="After message"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Your input is considered"/>
                                                    </FormItem>


                                                </Form>
                                            </Card>
                                        </TabPane>
                                        <TabPane tab={<span><Icon type="tag"/>Solutions</span>} key="4">
                                            <Card
                                                title="Solutions"
                                                extra={<Button type="primary" icon="plus" onClick={this.onClose}>
                                                    Add Block</Button>}
                                                style={{width: '100%'}}>

                                                <Form layout='horizontal'>
                                                    <FormItem
                                                        label="Question"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Where are you from?"/>
                                                    </FormItem>

                                                    <FormItem {...formItemLayout}
                                                              label="Validation">

                                                        <Select placeholder="Will validate the input">
                                                            <Option value="recruitment">Ignore</Option>
                                                            <Option value="Shopping">Email</Option>
                                                            <Option value="Sales">Full Name</Option>
                                                        </Select>
                                                    </FormItem>

                                                    <FormItem
                                                        label="After message"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Your input is considered"/>
                                                    </FormItem>

                                                </Form>
                                            </Card>
                                        </TabPane>
                                        <TabPane tab={<span><Icon type="branches"/>Go to block</span>} key="5">
                                            <Card
                                                title="Go to block"
                                                extra={<Button type="primary" icon="plus" onClick={this.onClose}>
                                                    Add Block</Button>}
                                                style={{width: '100%'}}>

                                                <Form layout='horizontal'>
                                                    <FormItem
                                                        label="Question"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Where are you from?"/>
                                                    </FormItem>

                                                    <FormItem {...formItemLayout}
                                                              label="Validation">

                                                        <Select placeholder="Will validate the input">
                                                            <Option value="recruitment">Ignore</Option>
                                                            <Option value="Shopping">Email</Option>
                                                            <Option value="Sales">Full Name</Option>
                                                        </Select>
                                                    </FormItem>

                                                    <FormItem
                                                        label="After message"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Your input is considered"/>
                                                    </FormItem>

                                                </Form>
                                            </Card>
                                        </TabPane>
                                        <TabPane tab={<span><Icon type="fork"/>Go to group</span>} key="6">
                                            <Card
                                                title="Go to group"
                                                extra={<Button type="primary" icon="plus" onClick={this.onClose}>
                                                    Add Block</Button>}
                                                style={{width: '100%'}}>

                                                <Form layout='horizontal'>
                                                    <FormItem
                                                        label="Question"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Where are you from?"/>
                                                    </FormItem>

                                                    <FormItem {...formItemLayout}
                                                              label="Validation">

                                                        <Select placeholder="Will validate the input">
                                                            <Option value="recruitment">Ignore</Option>
                                                            <Option value="Shopping">Email</Option>
                                                            <Option value="Sales">Full Name</Option>
                                                        </Select>
                                                    </FormItem>

                                                    <FormItem
                                                        label="After message"
                                                        {...formItemLayout}>
                                                        <Input placeholder="Ex: Your input is considered"/>
                                                    </FormItem>

                                                </Form>
                                            </Card>
                                        </TabPane>
                                    </Tabs>
                                </Drawer>

                                <div style={{height: "100%", width: '100%', overflowY: 'auto    '}}>
                                    <SortableList items={this.state.items} onSortEnd={this.onSortEnd}/>
                                </div>

                            </div>

                        </div>
                    </div>
                </div>

            </div>
        );
    }

}

export default Form.create()(Flow);

