import React from 'react';
import styles from '../../AutoPilots/AutoPilot/AutoPilot.module.less';
import { connect } from 'react-redux';

import moment from 'moment';
import { Dropdown, Button, Menu, Icon, Table } from 'antd';
import 'types/TimeSlots_Types';
import 'types/AutoPilot_Types';

import { conversationActions, assistantActions, databaseActions } from 'store/actions';


class Availability extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            assistant: null,
            database: null,
            start: moment().startOf('week'),
            end:  moment().endOf('week')
        };
    }

    componentWillMount() {
        this.props.dispatch(assistantActions.fetchAssistants());
        this.props.dispatch(databaseActions.getDatabasesList());
    }

    handleMenuClick = (item) => {
        this.setState({ assistant: item.key, database: item.key });
        this.props.dispatch(databaseActions.fetchDatabase(item.key))  
    };

    filterThisWeek = (records) => {
        const searchArray = (convID) => {
            for (let idx in availability) {
                if (availability[idx].conversationID === convID) {
                    return idx;
                }
            }
            return null;
        };
        let availability = [];
        const { start, end } = this.state

        records.filter(record => record.CandidateAvailability).filter(record => {
            let dates = record.CandidateAvailability.split(',');
            let data = {
              name: record.CandidateName,
              skills: record.CandidateSkills,
              location: record.CandidateLocation,
              consultant: "Unknown",
              jobTitle: record.CandidateJobTitle
            }
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
                            let key = searchArray(record.ID); // key exists?
                            if (key) {
                                availability[key].dates.push(realDate);
                            } else {
                                availability.push({ID: record.ID, dates: [realDate], data: data });
                            }
                        }
                    });
                } else { // individual staggered dates
                    let realDate = moment(date, 'L');
                    if (realDate.isBetween(start, end) || realDate.isSame(start, 'date') || realDate.isSame(end, 'date')) {
                        let key = searchArray(record.ID); // key exists?
                        if (key) {
                            availability[key].dates.push(realDate);
                        } else {
                            availability.push({ ID: record.ID, dates: [realDate], data: data });
                        }
                    }
                }
            });
        });
        return availability;
    };

    moveWeek = change => {
      const { start, end } = this.state
      this.setState({start: start.clone().add(change, 'weeks'), end: end.clone().add(change, 'weeks')})
    }
    
    render() {
        const columns = [
            {
                title: 'Name',
                dataIndex: 'name',
                key: 'name'
            },
            {
                title: 'Skills',
                dataIndex: 'skills',
                key: 'skills'
            },
            {
                title: 'Location',
                dataIndex: 'location',
                key: 'location'
            },
            {
                title: 'Job Title',
                dataIndex: 'jobTitle',
                key: 'jobTitle'
            },
            {
                title: 'Consultant',
                dataIndex: 'consultant',
                key: 'consultant'
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
        const menu = (
            <Menu onClick={this.handleMenuClick}>
                {this.props.dbList.map((database, i) => (
                    <Menu.Item key={database.ID}>
                        {database.Name}
                    </Menu.Item>
                ))}
            </Menu>
        );

        const { assistant, database } = this.state;
        const { conversations, db } = this.props;
        let records  = db.databaseContent ? db.databaseContent.records : null
        let availability = null;
        let availableText = <Icon type="check" style={{textAlign: 'center'}}/>

        if (records) {
            availability = this.filterThisWeek(records).map(item => ({
                name: item.data.name,
                skills: item.data.skills,
                location: item.data.location,
                jobTitle: item.data.jobTitle,
                consultant: item.data.consultant,
                monday: item.dates.find(date => date.day() === 1) !== undefined ? availableText : '',
                tuesday: item.dates.find(date => date.day() === 2) !== undefined ? availableText : '',
                wednesday: item.dates.find(date => date.day() === 3) !== undefined ? availableText : '',
                thursday: item.dates.find(date => date.day() === 4) !== undefined ? availableText : '',
                friday: item.dates.find(date => date.day() === 5) !== undefined ? availableText : '',
                saturday: item.dates.find(date => date.day() === 6) !== undefined ? availableText : '',
                sunday: item.dates.find(date => date.day() === 0) !== undefined ? availableText : ''
            }));
        }

        return (
            <div>
                <Dropdown overlay={menu}>
                    {database ?
                        <Button>
                            {this.props.dbList.find(db => db.ID === parseInt(database)).Name} <Icon
                            type="down"/>
                        </Button> :
                        <Button>
                            Select a database <Icon type="down"/>
                        </Button>}
                </Dropdown>
                <Button onClick={() => this.moveWeek(-1)}>
                  <Icon type="left" />
                </Button>
                {this.state.start.format("L")} 
                <Button onClick={() => this.moveWeek(1)} style={{marginLeft: 6}}>
                  <Icon type="right" />
                </Button>

                {availability ?
                    <Table style={{marginTop: '22px'}} columns={columns} dataSource={availability}/>
                    : null}
            </div>);
    }
}


function mapStateToProps(state) {
  console.log(state)
    return {
        dbList: state.database.databasesList,
        conversations: state.conversation.conversations.conversationsList,
        assistants: state.assistant.assistantList,
        db: state.database.fetchedDatabase
    };
}

export default connect(mapStateToProps, null)(Availability);
