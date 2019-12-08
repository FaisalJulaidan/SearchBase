import React from 'react';
import { connect } from 'react-redux';

import moment from 'moment';
import { AutoComplete, Button, Dropdown, Empty, Icon, Input, Menu, Table } from 'antd';
import { checkDate } from 'helpers';
import 'types/TimeSlots_Types';
import 'types/AutoPilot_Types';
import './Availabilty.less';
import { assistantActions, databaseActions } from 'store/actions';
import { conversationActions } from '../../../../store/actions';

let momentFormat = 'DD/MM/YYYY';


class Availability extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            assistant: null,
            database: null,
            start: moment().startOf('isoWeek'),
            end: moment().endOf('isoWeek'),
            searches: {}
        };

        this.columns = [
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
                dataIndex: 'currentJobTitle',
                key: 'currentJobTitle'
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
            },
        ];
    }

    componentWillMount() {
        this.props.dispatch(assistantActions.fetchAssistants());
        this.props.dispatch(databaseActions.getDatabasesList());
    }

    handleMenuClick = (item) => {
        if (item.key)
            if (item.keyPath[1] === 'item_0') {
                this.setState({ assistant: null, database: item.key });
                this.props.dispatch(databaseActions.fetchAvailableCandidates(item.key)).then(() => {
                    this.populateRecords('DB');
                    this.setState({ sourceType: 'DB' });
                });
            } else {
                this.setState({ assistant: item.key, database: null });
                this.props.dispatch(conversationActions.fetchConversations(item.key)).then(() => {
                    this.populateRecords('ASSISTANT');
                    this.setState({ sourceType: 'ASSISTANT' });
                });
            }
    };

    populateRecords = (sourceType) => {
        let availableText = <Icon type="check" style={{ textAlign: 'center' }}/>;

        const { assistant, database } = this.state;
        const { conversations, availableCandidates } = this.props;

        let records = [];
        let availability;

        if (database && availableCandidates && availableCandidates.length)
            records = availableCandidates;

        if (assistant && conversations && conversations.length)
            records = conversations.map(conversation => {
                    if (conversation.Data.keywordsByDataType['Candidate Availability'])
                        return {
                            ...conversation,
                            CandidateAvailability: conversation.Data.keywordsByDataType['Candidate Availability'].join(',')
                        };
                }
            ).filter(x => x);

        if (records) {
            switch (sourceType) {
                case 'DB':
                    availability = this.filterThisWeek_DB(records).map(item => {
                        return {
                            name: item.data.name,
                            skills: item.data.skills,
                            location: item.data.location,
                            currentJobTitle: item.data.currentJobTitle,
                            consultant: item.data.consultant,
                            monday: item.dates.find(date => date.isoWeekday() === 1) !== undefined ? availableText : '',
                            tuesday: item.dates.find(date => date.isoWeekday() === 2) !== undefined ? availableText : '',
                            wednesday: item.dates.find(date => date.isoWeekday() === 3) !== undefined ? availableText : '',
                            thursday: item.dates.find(date => date.isoWeekday() === 4) !== undefined ? availableText : '',
                            friday: item.dates.find(date => date.isoWeekday() === 5) !== undefined ? availableText : '',
                            saturday: item.dates.find(date => date.isoWeekday() === 6) !== undefined ? availableText : '',
                            sunday: item.dates.find(date => date.isoWeekday() === 7) !== undefined ? availableText : ''
                        };
                    });
                    this.setState({ availability });
                    break;
                case 'ASSISTANT':
                    availability = this.filterThisWeek_Assistant(records).map((item, i) => {
                        return {
                            name: item.data.name,
                            skills: item.data.skills,
                            location: item.data.location,
                            currentJobTitle: item.data.currentJobTitle,
                            consultant: item.data.consultant,
                            monday: item.dates.find(date => date.isoWeekday() === 1) !== undefined ? availableText : '',
                            tuesday: item.dates.find(date => date.isoWeekday() === 2) !== undefined ? availableText : '',
                            wednesday: item.dates.find(date => date.isoWeekday() === 3) !== undefined ? availableText : '',
                            thursday: item.dates.find(date => date.isoWeekday() === 4) !== undefined ? availableText : '',
                            friday: item.dates.find(date => date.isoWeekday() === 5) !== undefined ? availableText : '',
                            saturday: item.dates.find(date => date.isoWeekday() === 6) !== undefined ? availableText : '',
                            sunday: item.dates.find(date => date.isoWeekday() === 7) !== undefined ? availableText : ''
                        };
                    });
                    this.setState({ availability });
                    break;
            }


        }
    };

    filterThisWeek_DB = (records) => {
        const searchArray = (convID) => {
            for (let idx in availability)
                if (availability[idx].ID === convID)
                    return idx;
            return null;
        };

        let availability = [];
        const { start, end } = this.state;

        records.filter(record => record.CandidateAvailability).filter(record => {
            let dates = record.CandidateAvailability.split(',');

            let data = {
                name: record.CandidateName,
                skills: record.CandidateSkills,
                location: record.CandidateCity,
                consultant: record.CandidateConsultantName,
                currentJobTitle: record.CandidateJobTitle
            };

            dates.forEach(date => {
                if (date[0] === ' ') {
                    date = date.substr(1, date.length - 1);
                }
                let realDate = checkDate(date, true, false);
                if (!realDate) return;
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

    filterThisWeek_Assistant = (records) => {
        const searchArray = (convID) => {
            for (let idx in availability)
                if (availability[idx].ID === convID)
                    return idx;
            return null;
        };

        let availability = [];
        const { start, end } = this.state;

        records.filter(record => record.CandidateAvailability).filter(record => {
            let data = {
                name: record.Name,
                location: '',
                skills: '',
                consultant: '',
                currentJobTitle: ''
            };

            if (record.Data.keywordsByDataType['Candidate Country'] &&
                record.Data.keywordsByDataType['Candidate Country'].join)
                data.location = record.Data.keywordsByDataType['Candidate Country'].join(' ');

            if (record.Data.keywordsByDataType['Candidate Skills'] &&
                record.Data.keywordsByDataType['Candidate Skills'].join)
                data.skills = record.Data.keywordsByDataType['Candidate Skills'].join(' ');

            if (record.Data.keywordsByDataType['Candidate Consultant Name'] &&
                record.Data.keywordsByDataType['Candidate Consultant Name'].join)
                data.consultant = record.Data.keywordsByDataType['Candidate Consultant Name'].join(' ');

            if (record.Data.keywordsByDataType['Current Job Title'] &&
                record.Data.keywordsByDataType['Current Job Title'].join)
                data.currentJobTitle = record.Data.keywordsByDataType['Current Job Title'].join(' ');


            let dates = record.CandidateAvailability.split(',');
            dates.forEach(date => {
                date = date.trim();
                let realDate = checkDate(date, true, false);
                if (!realDate) return;
                if (realDate.isBetween(start, end) || realDate.isSame(start, 'date') || realDate.isSame(end, 'date')) {
                    let key = searchArray(record.ID); // key exists?
                    console.log(key);
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

    filterSearches = () => {
        const { searches, availability } = this.state;
        const filtered = availability.filter(record => {
            let matches = Object.keys(searches).length;
            let catches = 0;
            Object.keys(searches).map(search => {
                if (record[search].indexOf(searches[search]) !== -1) {
                    catches++;
                }
            });
            return catches === matches;
        });
        this.setState({ availability: filtered });
    };

    moveWeek = change => {
        const { start, end, sourceType } = this.state;
        this.setState(
            { start: start.clone().add(change, 'weeks'), end: end.clone().add(change, 'weeks') },
            () => this.populateRecords(sourceType)
        );
    };

    getSearchAggregates = records => {
        const returnNewAggregate = (record, aggr) => {
            Object.keys(record).map(key => {
                if (key === 'skills') {
                    if(record[key]){
                        record[key].split(',').forEach(skill => {
                            if (!aggr[key].includes(skill)) {
                                aggr[key].push(skill);
                            }
                        });
                    }
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
        this.setState({ searches: searches }, () => this.filterSearches());
    };

    render() {
        const menu = () => {
            const dbItems = [...this.props.dbList];
            const assistantItems = [...this.props.assistants];
            return <Menu onClick={this.handleMenuClick}>
                {
                    dbItems.length &&
                    <Menu.SubMenu title="Databases">
                        {dbItems.map((database, i) => (
                            <Menu.Item key={database.ID}>
                                {database.Name}
                            </Menu.Item>
                        ))}
                    </Menu.SubMenu>
                }
                {
                    assistantItems.length &&
                    <Menu.SubMenu title="Assistants">
                        {assistantItems.map((assistant, i) => (
                            <Menu.Item key={assistant.ID}>
                                {assistant.Name}
                            </Menu.Item>
                        ))}
                    </Menu.SubMenu>
                }
                {
                    !dbItems.length && !assistantItems.length && <Empty description={false}/>
                }
            </Menu>;
        };


        let aggregates = this.state.availability ? this.getSearchAggregates(this.state.availability) : [];


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
                            placeholder="Location"
                            onChange={val => this.setSearch('location', val)}
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
                            dataSource={aggregates.currentJobTitle || []}
                            size="large"
                            style={{ width: '100%' }}
                            placeholder="Job Title"
                            optionLabelProp="value"
                            onChange={val => this.setSearch('preferredJobTitle', val)}
                        >
                            <Input suffix={<Icon type="search" className="certain-category-icon"/>}/>
                        </AutoComplete>
                    </div>
                </div>

                <Dropdown overlay={menu}>
                    <Button>
                        Select a database <Icon type="down"/>
                    </Button>
                </Dropdown>

                <Button onClick={() => this.moveWeek(-1)}>
                    Prev Week <Icon type="left"/>
                </Button>

                {this.state.start.format(momentFormat)}
                <Button onClick={() => this.moveWeek(1)} style={{ marginLeft: 6 }}>
                    Next Week <Icon type="right"/>
                </Button>

                <Table style={{ marginTop: '22px' }}
                       columns={this.columns}
                       dataSource={this.state.availability}
                       scroll={{ x: 'max-content' }}/>
            </div>);
    }
}


function mapStateToProps(state) {
    return {
        dbList: state.database.databasesList,
        conversations: state.conversation.conversations.conversationsList,
        assistants: state.assistant.assistantList,
        db: state.database.fetchedDatabase,
        isAvailableCandidatesLoading: state.database.isFetchedAvailableCandidatesLoading,
        availableCandidates: state.database.fetchedAvailableCandidates
    };
}

export default connect(mapStateToProps, null)(Availability);
