import React from 'react'
import styles from './AppointmentsPicker.module.less'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {appointmentsPickerActions} from "store/actions";
import {connect} from 'react-redux';
import AppointmentsTimetable from './AppointmentsTimetable/AppointmentsTimetable'
import {getLink} from "helpers";
import {Typography} from 'antd';


class AppointmentsPicker extends React.Component {

    requestToken = 'dummyText';

    componentDidMount() {
        this.requestToken = this.props.location.pathname.split('/')[2];
        this.props.dispatch(appointmentsPickerActions.fetchAppointment(this.requestToken));
    }

    onSubmit = selectedTimeSlot => this.props.dispatch(
        appointmentsPickerActions.selectAppointmentTime(this.requestToken, selectedTimeSlot)
    );


    render() {

        const timeTable = (
            this.props.appointment &&
            !this.props.isSelected &&
            <AppointmentsTimetable appointment={this.props.appointment} onSubmit={this.onSubmit}/>
        );

        const selected = (
            this.props.isSuccess &&
            this.props.isSelected &&
            <div style={{textAlign: 'center'}}>
                <img src={getLink('/static/images/undraw/success.svg')} alt="" height={300}/>
                <Typography.Title>
                    Thanks for your selection
                </Typography.Title>
                <h3>
                    Your appointment will be confirmed when the recruiter confrims the appointment
                    You will be notified by email
                </h3>
            </div>
        );

        return (
            <div style={{height: '100%'}}>
                <div className={styles.Navbar}>
                    <div>
                        <FontAwesomeIcon size="2x" icon={faCloud} style={{color: '#9254de'}}/>
                        <div style={{
                            lineHeight: '40px',
                            marginLeft: 18,
                            color: "#9254de"
                        }}>TheSearchBase
                        </div>
                    </div>
                </div>

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
