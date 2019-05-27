import React from 'react';
import {connect} from 'react-redux';
import styles from './Calendar.module.less'
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Badge, Calendar as AntdCalendar, Col, Divider, Icon, Modal, Row, Typography} from 'antd';
import moment from 'moment';
import './Calendar.less'

const {Title, Paragraph} = Typography;

const pStyle = {
    fontSize: 16,
    color: 'rgba(0,0,0,0.85)',
    lineHeight: '24px',
    display: 'block',
    marginBottom: 16,
};

const DescriptionItem = ({title, content}) => (
    <div
        style={{
            fontSize: 14,
            lineHeight: '22px',
            marginBottom: 7,
            color: 'rgba(0,0,0,0.65)',
        }}
    >
        <p style={{
                marginRight: 8,
                display: 'inline-block',
                color: 'rgba(0,0,0,0.85)',
        }}>
            {title}:
        </p>
        {content}
    </div>
);

class Calendar extends React.Component {

    state = {
        value: moment(),
        visible: false,
        drawerData: []
    };

    onCloseDrawer = () => this.setState({visible: false}, () => this.setState({drawerData: []}));

    onSelect = value => {
        const x = this.getListData(value);

        if (x.length)
            this.setState({value, visible: true, drawerData: x});
        else
            this.setState({value});
    };

    onPanelChange = value => this.setState({value});

    getListData = (value) => {
        let listData;
        switch (value.date()) {
            case 8:
                listData = [
                    {type: 'warning', content: 'Candidate appointment'},
                    {type: 'success', content: 'Client xyz'},
                ];
                break;
            case 10:
                listData = [
                    {type: 'warning', content: 'Candidate appointment baz'},
                    {type: 'success', content: 'Client xyz foo'},
                    {type: 'warning', content: 'Candidate appointment foo'},
                    {type: 'warning', content: 'Candidate appointment bar'},
                    {type: 'success', content: 'Client xyz bar'},
                ];
                break;
            case 15:
                listData = [
                    {type: 'success', content: 'Client xyz'},
                    {type: 'warning', content: 'Candidate appointment'},
                ];
                break;
            default:
        }
        return listData || [];
    };

    dateCellRender = (value) => {
        const listData = this.getListData(value);
        return (
            <ul className="events">
                {listData.map(item => (
                    <li key={item.content}>
                        <Badge status={item.type} text={item.content}/>
                    </li>
                ))}
            </ul>
        );
    };

    getMonthData = (value) => {
        if (value.month() === 8) {
            return 8;
        }
    };

    monthCellRender = (value) => {
        const num = this.getMonthData(value);
        return num ? (
            <div className="notes-month">
                <section>{num}</section>
                <span>Candidates</span>
            </div>
        ) : null;
    };


    render() {
        const {value} = this.state;

        return (
            <NoHeaderPanel>
                <div className={styles.Title}>
                    <div className={styles.Details}>
                        <Title> <Icon type="calendar"/> Calendar</Title>
                        <Paragraph type="secondary">
                            Here you can find all assigned calendars
                        </Paragraph>
                    </div>
                </div>

                <div>
                    <AntdCalendar value={value} onSelect={this.onSelect} onPanelChange={this.onPanelChange}
                                  dateCellRender={this.dateCellRender} monthCellRender={this.monthCellRender}/>

                    <Modal title="Basic Drawer"
                           width={640}
                           className={'custom_calendar'}
                           onCancel={this.onCloseDrawer}
                           onOk={this.onCloseDrawer}
                           visible={this.state.visible}>
                        {
                            this.state.drawerData.map((i, k) =>
                                <div key={k}>
                                    <p style={pStyle}>Personal</p>
                                    <Row>
                                        <Col span={12}>
                                            <DescriptionItem title="Full Name" content="Lily"/>{' '}
                                        </Col>
                                        <Col span={12}>
                                            <DescriptionItem title="Account" content="AntDesign@example.com"/>
                                        </Col>
                                    </Row>
                                    <Row>
                                        <Col span={12}>
                                            <DescriptionItem title="City" content="HangZhou"/>
                                        </Col>
                                        <Col span={12}>
                                            <DescriptionItem title="Country" content="China🇨🇳"/>
                                        </Col>
                                    </Row>
                                    <Row>
                                        <Col span={12}>
                                            <DescriptionItem title="Birthday" content="February 2,1900"/>
                                        </Col>
                                        <Col span={12}>
                                            <DescriptionItem title="Website" content="-"/>
                                        </Col>
                                    </Row>
                                    <Row>
                                        <Col span={24}>
                                            <DescriptionItem
                                                title="Message"
                                                content="Make things as simple as possible but no simpler."
                                            />
                                        </Col>
                                    </Row>
                                    <Divider/>
                                </div>
                            )
                        }
                    </Modal>
                </div>
            </NoHeaderPanel>
        );
    }
}

function mapStateToProps(state) {
    return {};
}

export default connect(mapStateToProps)(Calendar);
