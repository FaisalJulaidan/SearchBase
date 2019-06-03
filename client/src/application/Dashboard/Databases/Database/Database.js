import React from 'react'
import {connect} from 'react-redux';
import styles from "./Database.module.less";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {databaseActions} from "store/actions";
import {Button, Col, Form, Input, InputNumber, Table, Typography, Pagination} from 'antd';
import {history} from "helpers";
import {store} from "../../../../store/store";
import {authActions} from "../../../../store/actions";

const FormItem = Form.Item;

const {Title, Paragraph} = Typography;


/* Note: Find the columns for Candidates and Jobs tables at the end */
class Database extends React.Component {

    state = {
        data: [],
        pagination: {current:1, pageSize: 10},
        currentPage: 1,
        records: []
    };

    componentWillMount() {
        this.fetchDatabase(1)
    }

    fetchDatabase = (currentPage) => {
        store.dispatch(databaseActions.fetchDatabase(this.props.match.params.id, currentPage)).then(()=> {
            this.setState({
                currentPage:this.props.database?.databaseContent?.currentPage || 1,
                records: this.props.database?.databaseContent?.records || [],
            })
        })
    };


    updateDatabase = (updatedDatabase, databaseID) => {
        this.props.dispatch(databaseActions.updateDatabase(updatedDatabase, databaseID));
    };


    getColumnsByType = (type) => {
        if (type === 'Candidates')
            return CandidateColumns;
        if (type === 'Jobs')
            return JobColumns;
        return null
    };

    render() {
        const {databaseContent, databaseInfo} = this.props.database;
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Title}>
                        <div className={styles.Details}>
                            <Title>{databaseInfo?.Name} ({databaseInfo?.Type.name})</Title>
                            <Paragraph type="secondary">
                                View Your database content
                            </Paragraph>
                        </div>
                    </div>

                    <div className={styles.Body}>
                        <Table columns={this.getColumnsByType(databaseInfo?.Type.name)}
                               rowKey={record => record.ID}
                               dataSource={databaseContent?.records}
                               size='middle'
                               loading={this.props.isLoadingDatabase}
                               pagination={{
                                   pageSize: databaseContent?.totalPerPage,
                                   current: this.state.currentPage,
                                   total:databaseContent?.totalItems,
                                   position:"both",
                               }}
                               onChange={(p)=> this.fetchDatabase(p.current)}
                        />
                    </div>
                </NoHeaderPanel>
            </>
        )
    }
}

function mapStateToProps(state) {
    return {
        databasesList: state.database.databasesList,
        database: state.database.fetchedDatabase,
        isLoadingDatabase: state.database.isLoading,
        options: state.options.options,
    };
}

// export default Form.create()(DatabaseConfigs);
export default connect(mapStateToProps)(Form.create()(Database));

// Candidate Columns
const CandidateColumns = [{
    title: '#',
    key: '#',
    dataIndex: '#',
    render: (text, record, index) => (<p>{index + 1}</p>),
},{
    title: 'Name',
    key: 'CandidateName',
    dataIndex: 'CandidateName',
    render: (text, record, index) => (<p>{record.CandidateName || "--"}</p>),
}, {
    title: 'Email',
    key: 'CandidateEmail',
    dataIndex: 'CandidateEmail',
    render: (text, record, index) => (<p>{record.CandidateEmail || "--"}</p>),
}, {
    title: 'Mobile',
    key: 'CandidateMobile',
    dataIndex: 'CandidateMobile',
    render: (text, record, index) => (<p>{record.CandidateMobile || "--"}</p>),
} , {
    title: 'Location',
    key: 'Location',
    dataIndex: 'Location',
    render: (text, record, index) => (<p>{record.CandidateLocation || "--"}</p>),
} , {
    title: 'Skills',
    key: 'CandidateSkills',
    dataIndex: 'CandidateSkills',
    render: (text, record, index) => (<p>{record.CandidateSkills || "--"}</p>),
} , {
    title: 'Linkdin URL',
    key: 'CandidateLinkdinURL',
    dataIndex: 'CandidateLinkdinURL',
    render: (text, record, index) => (<p>{record.CandidateLinkdinURL || "--"}</p>),
}, {
    title: 'Availability',
    key: 'CandidateAvailability',
    dataIndex: 'CandidateAvailability',
    render: (text, record, index) => (<p>{record.CandidateAvailability || "--"}</p>),
}, {
    title: 'Job Title',
    key: 'CandidateJobTitle',
    dataIndex: 'CandidateJobTitle',
    render: (text, record, index) => (<p>{record.CandidateJobTitle || "--"}</p>),
}, {
    title: 'Education',
    key: 'CandidateEducation',
    dataIndex: 'CandidateEducation',
    render: (text, record, index) => (<p>{record.CandidateEducation || "--"}</p>),
}, {
    title: 'Years Of Experience',
    key: 'CandidateYearsExperience',
    dataIndex: 'CandidateYearsExperience',
    render: (text, record, index) => (<p>{record.CandidateYearsExperience || "--"}</p>),
}, {
    title: 'Desired Salary',
    key: 'CandidateDesiredSalary',
    dataIndex: 'CandidateDesiredSalary',
    render: (text, record, index) => (<p>{record.CandidateDesiredSalary || "--"}</p>),
}, {
    title: 'Currency',
    key: 'Currency',
    dataIndex: 'Currency',
    render: (text, record, index) => (<p>{record.Currency || "--"}</p>),
}];


const JobColumns = [{
    title: '#',
    key: '#',
    render: (text, record, index) => (<p>{index + 1}</p>),
},{
    title: 'Job Title',
    key: 'JobTitle',
    render: (text, record, index) => (<p>{record.JobTitle || "--"}</p>),
}, {
    title: 'Description',
    key: 'JobDescription',
    render: (text, record, index) => (<p>{record.JobDescription || "--"}</p>),
}, {
    title: 'Location',
    key: 'JobLocation',
    render: (text, record, index) => (<p>{record.JobLocation || "--"}</p>),
} , {
    title: 'Type',
    key: 'JobType',
    render: (text, record, index) => (<p>{record.JobType || "--"}</p>),
} , {
    title: 'Salary',
    key: 'JobSalary',
    render: (text, record, index) => (<p>{record.JobSalary || "--"}</p>),
} , {
    title: 'Currency',
    key: 'Currency',
    render: (text, record, index) => (<p>{record.Currency || "--"}</p>),
}, {
    title: 'Essential Skills',
    key: 'JobEssentialSkills',
    render: (text, record, index) => (<p>{record.JobEssentialSkills || "--"}</p>),
}, {
    title: 'Desired Skills',
    key: 'JobDesiredSkills',
    render: (text, record, index) => (<p>{record.JobDesiredSkills || "--"}</p>),
}, {
    title: 'Education',
    key: 'CandidateEducation',
    render: (text, record, index) => (<p>{record.CandidateEducation || "--"}</p>),
}, {
    title: 'Years Required',
    key: 'JobYearsRequired',
    render: (text, record, index) => (<p>{record.JobYearsRequired || "--"}</p>),
}, {
    title: 'Start Date',
    key: 'JobStartDate',
    render: (text, record, index) => (<p>{record.JobStartDate || "--"}</p>),
}, {
    title: 'End Date',
    key: 'JobEndDate',
    render: (text, record, index) => (<p>{record.JobEndDate || "--"}</p>),
}, {
    title: 'Job URL',
    key: 'JobLinkURL',
    render: (text, record, index) => (<p>{record.JobLinkURL || "--"}</p>),
}];