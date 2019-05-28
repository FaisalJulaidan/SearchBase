import React from 'react';
import {connect} from 'react-redux';
import styles from './Calendar.module.less'
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Badge, Calendar as AntdCalendar, Col, Divider, Icon, Modal, Row, Typography, Input} from 'antd';
import moment from 'moment';
import './Calendar.less'

const {Title, Paragraph} = Typography;
const { TextArea } = Input;

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
        appointments: [
            {
                name: "Jamie Burns",
                dateTime: 'Mon, 27 May 2019 23:13:45 GMT',
                notes: "This is a good candidate and fits very well in big projects"
            }, {
                name: "Emilio Blake",
                dateTime: 'Mon, 27 May 2019 23:13:45 GMT',
                notes: null
            }, {
                name: "Marvin Williamson",
                dateTime: 'Mon, 27 May 2019 23:13:45 GMT',
                notes: null
            },
        ]
    };

    onCloseModal = () => {
        this.setState({visible: false});
    };

    onSelect = value => {
        const x = this.getListData(value);

        if (x.length)
            this.setState({value, visible: true});
        else
            this.setState({value});
    };

    onPanelChange = value => this.setState({value});

    getListData = (value) => {
        let listData;
        switch (value.date()) {
            case 8:
                listData = [
                    {type: 'warning', content: '2 Appointments'},
                ];
                break;
            case 10:
                listData = [
                    {type: 'warning', content: '1 Appointment'},
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

                    <Modal title="Appointments Details"
                           width={640}
                           className={'custom_calendar'}
                           onCancel={this.onCloseModal}
                           onOk={this.onCloseModal}
                           okText="Save"
                           cancelText="Cancel"
                           visible={this.state.visible}>
                        {
                            this.state.appointments.map((a, index) =>

                                <div key={index}>
                                    {console.log(a.name)}
                                    <Title level={4}>{a.name}</Title>
                                    <Row>
                                        <Col span={24}>
                                            <p>
                                                <b>Date & Time: </b>
                                                <span style={{color:'#9254de'}}>{a.dateTime}</span>
                                            </p>
                                        </Col>
                                        <Col span={24}>
                                            <p><b>Notes:</b></p>
                                            <TextArea
                                                placeholder="Write your notes here..."
                                                autosize={{ minRows: 2, maxRows: 6 }}
                                                value={a.notes}
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
