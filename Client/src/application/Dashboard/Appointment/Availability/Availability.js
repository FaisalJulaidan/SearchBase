import React from 'react';
import styles from '../../AutoPilots/AutoPilot/AutoPilot.module.less';
import { connect } from 'react-redux';

import moment from 'moment';
import { Dropdown, Button, Menu, Icon, Table } from 'antd';
import 'types/TimeSlots_Types';
import 'types/AutoPilot_Types';

import { conversationActions, assistantActions } from 'store/actions';


class Availability extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            assistant: null
        };
    }

    componentWillMount() {
        this.props.dispatch(assistantActions.fetchAssistants());
    }

    handleMenuClick = (item) => {
        this.setState({ assistant: item.key });
        this.props.dispatch(conversationActions.fetchConversations(item.key));
    };

    filterThisWeek = (conversations) => {
        const searchArray = (convID) => {
            for (let idx in availability) {
                if (availability[idx].conversationID === convID) {
                    return idx;
                }
            }
            return null;
        };
        let availability = [];
        let start = moment().startOf('week');
        let end = moment().endOf('week');
        conversations.filter(conversation => conversation.Data.keywordsByDataType['Candidate Availability']).filter(conversation => {
            let dates = conversation.Data.keywordsByDataType['Candidate Availability'][0].split(',');
            dates.forEach(date => {
                let range = date.split('-');
                if (range.length > 1) { // range handlers
                    let startDate = moment(range[0], 'L');
                    let rangeArr = [startDate];
                    let moveDate = startDate.clone();
                    let endDate = moment(range[1], 'L');
                    while (rangeArr.length !== Math.abs(startDate.diff(endDate, 'days'))) {
                        rangeArr.push(moveDate.add(1, 'days').clone());
                    }
                    rangeArr.push(endDate);
                    rangeArr.forEach(realDate => {
                        if (realDate.isBetween(start, end) || realDate.isSame(start, 'date') || realDate.isSame(end, 'date')) {
                            let key = searchArray(conversation.ID); // key exists?
                            if (key) {
                                availability[key].dates.push(realDate);
                            } else {
                                availability.push({ conversationID: conversation.ID, conversation, dates: [realDate] });
                            }
                        }
                    });
                } else { // individual staggered dates
                    let realDate = moment(date, 'L');
                    if (realDate.isBetween(start, end) || realDate.isSame(start, 'date') || realDate.isSame(end, 'date')) {
                        let key = searchArray(conversation.ID); // key exists?
                        if (key) {
                            availability[key].dates.push(realDate);
                        } else {
                            availability.push({ conversationID: conversation.ID, conversation, dates: [realDate] });
                        }
                    }
                }
            });
        });
        return availability;
    };


    render() {

        const columns = [
            {
                title: 'Name',
                dataIndex: 'name',
                key: 'name'
            },
            {
                title: 'Monday',
                dataIndex: 'monday',
                key: 'monday'
            },
            {
                title: 'Tuesday',
                dataIndex: 'tuesday',
                key: 'tuesday'
            },
            {
                title: 'Wednesday',
                dataIndex: 'wednesday',
                key: 'wednesday'
            },
            {
                title: 'Thursday',
                dataIndex: 'thursday',
                key: 'thursday'
            },
            {
                title: 'Friday',
                dataIndex: 'friday',
                key: 'friday'
            },
            {
                title: 'Saturday',
                dataIndex: 'saturday',
                key: 'saturday'
            },
            {
                title: 'Sunday',
                dataIndex: 'sunday',
                key: 'sunday'
            }
        ];
        console.log(this.props.conversations);
        const menu = (
            <Menu onClick={this.handleMenuClick}>
                {this.props.assistants.map((assistant, i) => (
                    <Menu.Item key={assistant.ID}>
                        {assistant.Name}
                    </Menu.Item>
                ))}
            </Menu>
        );

        const { assistant } = this.state;
        const { conversations } = this.props;
        let availability = null;
        if (conversations) {
            availability = this.filterThisWeek(conversations).map(item => ({
                name: 'Bob',
                monday: item.dates.find(date => date.day() === 1) !== undefined ? 'Available' : '',
                tuesday: item.dates.find(date => date.day() === 2) !== undefined ? 'Available' : '',
                wednesday: item.dates.find(date => date.day() === 3) !== undefined ? 'Available' : '',
                thursday: item.dates.find(date => date.day() === 4) !== undefined ? 'Available' : '',
                friday: item.dates.find(date => date.day() === 5) !== undefined ? 'Available' : '',
                saturday: item.dates.find(date => date.day() === 6) !== undefined ? 'Available' : '',
                sunday: item.dates.find(date => date.day() === 0) !== undefined ? 'Available' : ''
            }));
        }

        return (
            <div>
                <Dropdown overlay={menu}>
                    {assistant ?
                        <Button>
                            {this.props.assistants.find(astnt => astnt.ID === parseInt(assistant)).Name} <Icon
                            type="down"/>
                        </Button> :
                        <Button>
                            Select an assistant <Icon type="down"/>
                        </Button>}
                </Dropdown>

                {availability ?
                    <Table style={{marginTop: '22px'}} columns={columns} dataSource={availability}/>
                    : null}
            </div>);
    }
}


function mapStateToProps(state) {
    return {
        conversations: state.conversation.conversations.conversationsList,
        assistants: state.assistant.assistantList
    };
}

export default connect(mapStateToProps, null)(Availability);
