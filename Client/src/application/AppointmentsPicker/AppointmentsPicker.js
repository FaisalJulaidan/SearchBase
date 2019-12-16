import React from 'react';
import styles from './AppointmentsPicker.module.less';
import { appointmentsPickerActions } from 'store/actions';
import { connect } from 'react-redux';
import AppointmentsTimetable from './AppointmentsTimetable/AppointmentsTimetable';
import PublicNavbar from "components/PublicNavbar/PublicNavbar";
import { getLink } from 'helpers';
import { Typography } from 'antd';
import moment from 'moment';


class AppointmentsPicker extends React.Component {

    requestToken = 'dummyText';

    componentDidMount() {
        this.requestToken = this.props.location.pathname.split('/')[2];
        this.props.dispatch(appointmentsPickerActions.fetchAppointment(this.requestToken));
    }

    onSubmit = ({ selectedTimeSlot, userTimeZone }) => {
        const convertedTimeBackToUTC = moment(selectedTimeSlot, 'YYYY-MM-DD hh:mm').utc().format('YYYY-MM-DD hh:mm');
        this.props.dispatch(
            appointmentsPickerActions.selectAppointmentTime(this.requestToken, convertedTimeBackToUTC, userTimeZone)
        );
    };


    render() {
        const {logoPath, companyName} = this.props.appointment;
        const timeTable = (
            this.props.appointment &&
            !this.props.isSelected &&
            <AppointmentsTimetable appointment={this.props.appointment} onSubmit={this.onSubmit}/>
        );

        const selected = (
            this.props.isSuccess &&
            this.props.isSelected &&
            <div style={{textAlign: 'center'}}>
                <img src={"/images/undraw/success.svg"} alt="" height={300}/>
                <Typography.Title>
                    Thanks for your selection
                </Typography.Title>
                <h3>
                    Your appointment will be confirmed when the recruiter confirms the appointment.
                    You will be notified by email
                </h3>
            </div>
        );

        return (
            <div style={{height: '100%'}}>
                <PublicNavbar logoPath={logoPath} companyName={companyName}
                              hideOnMobile={true}/>

                <div className={styles.Wrapper}>

                    {timeTable}

                    {selected}

                </div>

            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        appointment: state.appointmentsPicker.appointment,
        isSuccess: state.appointmentsPicker.isSuccess,
        isSelected: state.appointmentsPicker.isSelected,
    };
}

export default connect(mapStateToProps)(AppointmentsPicker);
