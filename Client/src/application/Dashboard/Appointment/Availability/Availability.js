import React from 'react';
import { connect } from 'react-redux';

import moment from 'moment';
import { Button, Cascader, Icon, Input, Table } from 'antd';
import { checkDate } from 'helpers';
import Highlighter from 'react-highlight-words';
import 'types/TimeSlots_Types';
import 'types/AutoPilot_Types';
import './Availabilty.less';
import { assistantActions, databaseActions, conversationActions } from 'store/actions';

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
                key: 'name',
                ...this.getColumnSearchProps('name')
            },
            {
                title: 'Skills',
                dataIndex: 'skills',
                key: 'skills',
                ...this.getColumnSearchProps('skills')
            },
            {
                title: 'Location',
                dataIndex: 'location',
                key: 'location',
                ...this.getColumnSearchProps('location')
            },
            {
                title: 'Job Title',
                dataIndex: 'currentJobTitle',
                key: 'currentJobTitle',
                ...this.getColumnSearchProps('currentJobTitle')
            },
            {
                title: 'Consultant',
                dataIndex: 'consultant',
                key: 'consultant',
                ...this.getColumnSearchProps('consultant')
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
    }

    componentWillMount() {
        this.props.dispatch(assistantActions.fetchAssistants());
        this.props.dispatch(databaseActions.getDatabasesList());
    }

    // Copied from Antd
    getColumnSearchProps = dataIndex => ({
        filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
            <div style={{ padding: 8 }}>
                <Input
                    ref={node => {
                        this.searchInput = node;
                    }}
                    placeholder={`Search ${dataIndex}`}
                    value={selectedKeys[0]}
                    onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
                    onPressEnter={() => this.handleSearch(selectedKeys, confirm, dataIndex)}
                    style={{ width: 188, marginBottom: 8, display: 'block' }}
                />
                <Button
                    type="primary"
                    onClick={() => this.handleSearch(selectedKeys, confirm, dataIndex)}
                    icon="search"
                    size="small"
                    style={{ width: 90, marginRight: 8 }}
                >
                    Search
                </Button>
                <Button onClick={() => this.handleReset(clearFilters)} size="small" style={{ width: 90 }}>
                    Reset
                </Button>
            </div>
        ),
        filterIcon: filtered => (
            <Icon type="search" style={{ color: filtered ? '#9254de' : undefined }}/>
        ),
        onFilter: (value, record) =>
            record[dataIndex]
                .toString()
                .toLowerCase()
                .includes(value.toLowerCase()),
        onFilterDropdownVisibleChange: visible => {
            if (visible) {
                setTimeout(() => this.searchInput.select());
            }
        },
        render: text =>
            this.state.searchedColumn === dataIndex ? (
                <Highlighter
                    highlightStyle={{ backgroundColor: '#ffc069', padding: 0 }}
                    searchWords={[this.state.searchText]}
                    autoEscape
                    textToHighlight={text.toString()}
                />
            ) : (
                text
            )
    });

    handleSearch = (selectedKeys, confirm, dataIndex) => {
        confirm();
        this.setState({
            searchText: selectedKeys[0],
            searchedColumn: dataIndex
        });
    };

    handleReset = clearFilters => {
        clearFilters();
        this.setState({ searchText: '' });
    };

    handleMenuClick = (item) => {
        const source = item[0];
        const key = item[1];
        if (source === 'Assistants') {
            this.setState({ assistant: key, database: null });
            this.props.dispatch(conversationActions.fetchConversations(key)).then(() => {
                this.populateRecords('ASSISTANT');
                this.setState({ sourceType: 'ASSISTANT' });
            });
        } else if (source === 'Databases') {
            this.setState({ assistant: null, database: key });
            this.props.dispatch(databaseActions.fetchAvailableCandidates(key)).then(() => {
                this.populateRecords('DB');
                this.setState({ sourceType: 'DB' });
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
                    availability = this.filterThisWeek_Assistant(records).map((item) => {
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
        const { start, end, sourceType } = this.state;
        this.setState(
            { start: start.clone().add(change, 'weeks'), end: end.clone().add(change, 'weeks') },
            () => this.populateRecords(sourceType)
        );
    };

    render() {
        const { assistants, databases } = this.props;
        const options = [
            {
                value: 'Assistants',
                label: 'Assistants',
                disabled: !assistants.length,
                children: assistants.map((assistant, i) => ({ value: assistant.ID, label: assistant.Name }))
            },
            {
                value: 'Databases',
                label: 'Databases',
                disabled: !databases.length,
                children: databases.map((database, i) => ({ value: database.ID, label: database.Name }))
            }
        ];

        return (
            <div>
                <Cascader style={{ marginRight: '8px' }} options={options} onChange={this.handleMenuClick}
                          placeholder="Select source"/>

                <Button onClick={() => this.moveWeek(-1)}>
                    Prev Week <Icon type="left"/>
                </Button>

                <span style={{ fontWeight: 700 }}>
                    {`${this.state.start.format(momentFormat)} - ${this.state.end.format(momentFormat)}`}
                </span>

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
        databases: state.database.databasesList,
        conversations: state.conversation.conversations.conversationsList,
        assistants: state.assistant.assistantList,
        db: state.database.fetchedDatabase,
        isAvailableCandidatesLoading: state.database.isFetchedAvailableCandidatesLoading,
        availableCandidates: state.database.fetchedAvailableCandidates
    };
}

export default connect(mapStateToProps, null)(Availability);
