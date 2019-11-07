import React from 'react';
import { connect } from 'react-redux';

import moment from 'moment';
import { AutoComplete, Button, Dropdown, Icon, Input, Menu, Table } from 'antd';
import {checkDate} from "helpers";
import 'types/TimeSlots_Types';
import 'types/AutoPilot_Types';
import './Availabilty.less';
import { assistantActions, databaseActions } from 'store/actions';

let momentFormat = 'DD/MM/YYYY';


class Availability extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            assistant: null,
            database: null,
            start: moment().startOf('week'),
            end: moment().endOf('week'),
            searches: {}
        };
    }

    componentWillMount() {
        this.props.dispatch(assistantActions.fetchAssistants());
        this.props.dispatch(databaseActions.getDatabasesList());
    }

    handleMenuClick = (item) => {
        this.setState({ assistant: item.key, database: item.key });
        this.props.dispatch(databaseActions.fetchDatabase(item.key));
    };

    filterSearches = (records) => {
        const { searches } = this.state;
        return records.filter(record => {
            let matches = Object.keys(searches).length;
            let catches = 0;
            Object.keys(searches).map(search => {
                if (record[search].indexOf(searches[search]) !== -1) {
                    catches++;
                }
            });
            return catches === matches;
        });
    };

    filterThisWeek = (records) => {
        const searchArray = (convID) => {
            for (let idx in availability) {
                if (availability[idx].ID === convID) {
                    return idx;
                }
            }
            return null;
        };
        let availability = [];
        const { start, end } = this.state;
        records.filter(record => record.CandidateAvailability).filter(record => {
            let dates = record.CandidateAvailability.split(',');

            let data = {
                name: record.CandidateName,
                skills: record.CandidateSkills,
                location: record.CandidateLocation,
                consultant: record.CandidateConsultantName,
                jobTitle: record.CandidateJobTitle
            };

            dates.forEach(date => {
                let realDate = checkDate(date, true, true);
                if(!realDate) return
                if (realDate.isBetween(start, end) || realDate.isSame(start, 'date') || realDate.isSame(end, 'date')) {
                    let key = searchArray(record.ID); // key exists?
                    if (key) {
                        availability[key].dates.push(realDate);
                    } else {
                        availability.push({ ID: record.ID, dates: [realDate], data: data });
                    }
                }
            });
        });
        return availability;
    };

    moveWeek = change => {
        const { start, end } = this.state;
        this.setState({ start: start.clone().add(change, 'weeks'), end: end.clone().add(change, 'weeks') });
    };

    getSearchAggregates = records => {
        const returnNewAggregate = (record, aggr) => {
            Object.keys(record).map(key => {
                let add;
                if (key === 'skills') {
                    record[key].split(',').forEach(skill => {
                        if (!aggr[key].includes(skill)) {
                            aggr[key].push(skill);
                        }
                    });
                } else {
                    if (!aggr[key].includes(record[key]) && record[key] !== null) {
                        aggr[key].push(record[key]);
                    }
                }
            });
            return aggr;
        };
        if (records.length === 0) {
            return {};
        }
        let emptyAggregates = Object.keys(records[0]).reduce((prev, curr) => {
            prev[curr] = [];
            return prev;
        }, {});
        return records.reduce((prev, curr) => returnNewAggregate(curr, prev), emptyAggregates);
    };

    setSearch = (type, val) => {
        let searches = Object.assign({}, this.state.searches);
        if (val === '') {
            delete searches[type];
        } else {
            searches[type] = val;
        }
        this.setState({ searches: searches });
    };

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
                title: 'Sunday',
                dataIndex: 'sunday',
                key: 'sunday'
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
        let records = db.databaseContent ? db.databaseContent.records : null;
        let availability = null;
        let aggregates = {};
        let availableText = <Icon type="check" style={{ textAlign: 'center' }}/>;

        if (records) {
            availability = this.filterThisWeek(records).map(item => ({
                name: item.data.name,
                skills: item.data.skills,
                location: item.data.location,
                jobTitle: item.data.jobTitle,
                consultant: item.data.consultant,
                sunday: item.dates.find(date => date.day() === 0) !== undefined ? availableText : '',
                monday: item.dates.find(date => date.day() === 1) !== undefined ? availableText : '',
                tuesday: item.dates.find(date => date.day() === 2) !== undefined ? availableText : '',
                wednesday: item.dates.find(date => date.day() === 3) !== undefined ? availableText : '',
                thursday: item.dates.find(date => date.day() === 4) !== undefined ? availableText : '',
                friday: item.dates.find(date => date.day() === 5) !== undefined ? availableText : '',
                saturday: item.dates.find(date => date.day() === 6) !== undefined ? availableText : ''
            }));
            // availability = this.searc
            aggregates = this.getSearchAggregates(availability);
            availability = this.filterSearches(availability);
        }

        console.log(aggregates);

        return (
            <div>
                <div style={{ display: 'flex' }}>
                    <div className="certain-category-search-wrapper"
                         style={{ width: 200, margin: '10px 10px 10px 0px' }}>
                        <AutoComplete
                            className="certain-category-search"
                            dropdownClassName="certain-category-search-dropdown"
                            dropdownMatchSelectWidth={false}
                            dataSource={aggregates.skills || []}
                            dropdownStyle={{ width: 300 }}
                            size="large"
                            style={{ width: '100%' }}
                            placeholder="Skills"
                            onChange={val => this.setSearch('skills', val)}
                            optionLabelProp="value"
                        >
                            <Input suffix={<Icon type="search" className="certain-category-icon"/>}/>
                        </AutoComplete>
                    </div>

                    <div className="certain-category-search-wrapper" style={{ width: 200, margin: 10 }}>
                        <AutoComplete
                            className="certain-category-search"
                            dropdownClassName="certain-category-search-dropdown"
                            dropdownMatchSelectWidth={false}
                            dropdownStyle={{ width: 300 }}
                            dataSource={aggregates.location || []}
                            size="large"
                            style={{ width: '100%' }}
                            placeholder="Location" onChange={val => this.setSearch('location', val)}
                            optionLabelProp="value"
                        >
                            <Input suffix={<Icon type="search" className="certain-category-icon"/>}/>
                        </AutoComplete>
                    </div>

                    <div className="certain-category-search-wrapper" style={{ width: 200, margin: 10 }}>
                        <AutoComplete
                            className="certain-category-search"
                            dropdownClassName="certain-category-search-dropdown"
                            dropdownMatchSelectWidth={false}
                            dropdownStyle={{ width: 300 }}
                            dataSource={aggregates.jobTitle || []}
                            size="large"
                            style={{ width: '100%' }}
                            placeholder="Job Title"
                            optionLabelProp="value"
                            onChange={val => this.setSearch('jobTitle', val)}
                        >
                            <Input suffix={<Icon type="search" className="certain-category-icon"/>}/>
                        </AutoComplete>
                    </div>
                </div>
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
                    <Icon type="left"/>
                </Button>
                {this.state.start.format(momentFormat)}
                <Button onClick={() => this.moveWeek(1)} style={{ marginLeft: 6 }}>
                    <Icon type="right"/>
                </Button>

                {availability ?
                    <Table style={{ marginTop: '22px' }} columns={columns} dataSource={availability}/>
                    : null}
            </div>);
    }
}


function mapStateToProps(state) {
    console.log(state);
    return {
        dbList: state.database.databasesList,
        conversations: state.conversation.conversations.conversationsList,
        assistants: state.assistant.assistantList,
        db: state.database.fetchedDatabase
    };
}

export default connect(mapStateToProps, null)(Availability);
