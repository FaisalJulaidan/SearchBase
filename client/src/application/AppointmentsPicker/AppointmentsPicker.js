import React from 'react'
import styles from './AppointmentsPicker.module.less'
import {Button, Skeleton, Typography} from 'antd'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import moment from 'moment';
import {appointmentsPickerActions} from "store/actions";
import {connect} from 'react-redux';

const {Title, Paragraph} = Typography;

class AppointmentsPicker extends React.Component {

    constructor(props) {
        super(props);
        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
    }

    state = {
        width: 0,
        height: 0,
        firstDate: moment(),
        stWeekDays: [],
        selectedTimeSlot: ''
    };

    firstDateAfter4weeks = moment().add(28, 'day');
    requestToken = 'dummyText';

    componentDidMount() {
        this.updateWindowDimensions();
        window.addEventListener('resize', this.updateWindowDimensions);

        this.requestToken = this.props.location.pathname.split('/')[2];
        this.props.dispatch(appointmentsPickerActions.fetchAppointment(this.requestToken));
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateWindowDimensions);
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevState.width !== this.state.width)
            this.createTimeTable();
    }

    componentWillReceiveProps(nextProps) {
        this.createTimeTable(nextProps)
    }

    updateWindowDimensions() {
        this.setState({width: window.innerWidth, height: window.innerHeight});
    }

    createTimeTable = (props = this.props, state = this.state) => {
        const getTimeSlots = (From, To, duration) => {
            const hours = moment.duration(To.diff(From)).hours(); // 3
            const minutes = moment.duration(To.diff(From)).minutes();// 30
            let totalHalfHours = (minutes / 30) + (hours * 2); // 1 + 6 = 7

            if (duration === 60)
                if (totalHalfHours < 2)
                    totalHalfHours = 0;
                else
                    totalHalfHours = Math.ceil(totalHalfHours / 2);

            return totalHalfHours
        };

        const range = state.width < 700 ? 3 : 7;

        const weekDaysKey = {
            0: 'Mon',
            1: 'Tue',
            2: 'Wed',
            3: 'Thu',
            4: 'Fri',
            5: 'Sat',
            6: 'Sun',
        };

        let weekDays = [];
        let sv_appointment = props.appointment;

        for (const i in sv_appointment.openTimes) {
            sv_appointment.openTimes[i].From = moment(sv_appointment.openTimes[i].From, 'HH:mm');
            sv_appointment.openTimes[i].To = moment(sv_appointment.openTimes[i].To, 'HH:mm')
        }

        if (sv_appointment.openTimes) {

            for (let i = 0; i < range; i++) {
                const date = state.firstDate.clone().add(i, 'days');

                const weekDay = {
                    day: date.date(),
                    dayText: date.format('ddd'), // Sun
                    month: date.month(),
                    monthText: date.format('MMM'), // Jun
                    year: date.year(),

                    slots: []
                };

                const svWeekDay = sv_appointment.openTimes.find(ot => weekDaysKey[ot.Day] === weekDay.dayText);

                const totalSlots = getTimeSlots(
                    svWeekDay.From,
                    svWeekDay.To,
                    svWeekDay.Duration
                );

                // generate slots
                if (totalSlots)
                    for (let j = 1; j <= totalSlots; j++) {
                        if (j === 1)
                            weekDay.slots.push({
                                selected: false,
                                active: svWeekDay.Active,
                                duration: svWeekDay.Duration,
                                time: svWeekDay.From.format('HH:mm'),
                                timeMoment: svWeekDay.From,
                                dateMoment: date
                            });
                        else
                            weekDay.slots.push({
                                selected: false,
                                active: svWeekDay.Active,
                                duration: svWeekDay.Duration,
                                time: svWeekDay.From.clone().add(svWeekDay.Duration * (j - 1), 'minutes').format('HH:mm'),
                                timeMoment: svWeekDay.From.clone().add(svWeekDay.Duration * (j - 1), 'minutes'),
                                dateMoment: date
                            });
                    }

                weekDays.push(weekDay)
            }


            /**
             * Refining the taken slots:
             *  1- find the day
             *  2- find the slot
             *  3- deactivate the slot
             */
            for (let i = 0; i < range; i++) {
                sv_appointment.takenTimeSlots.forEach((timeSlot) => {
                    const takenTimeSlot = moment(timeSlot.DateTime, 'ddd, DD MMM YYYY HH:mm:ss');
                    // finding the day
                    weekDays.find(weekDay => {
                        // founded the day
                        if (weekDay.day === takenTimeSlot.date() && weekDay.month === takenTimeSlot.month()) {
                            // finding the slot
                            weekDay.slots.find(slot => {
                                // founded the slot
                                if (slot.time === takenTimeSlot.format('HH:mm')) {
                                    // deactivate it
                                    slot.active = false;
                                }
                            })
                        }
                    })
                });
            }

            /**
             * Refining the current day slots:
             *  1- go for current day
             *  2- deactivate all passed slots
             */
            // find the current day
            weekDays.find(
                weekDay => {
                    // founded the current day
                    if (weekDay.day === moment().date() && weekDay.month === moment().month()) {

                        // 1- deactivate the passed slots
                        // 2- deactivate the next 6 hours
                        weekDay.slots.forEach(slot => {
                            // is slot passed the current time ? then deactivate it
                            if (moment(slot.time, 'HH:mm').isBefore())
                                slot.active = false;

                            if (moment(slot.time, 'HH:mm').isBefore(moment().add(6, 'hours')))
                                slot.active = false;
                        })
                    }
                }
            );

            this.setState({stWeekDays: weekDays})
        }
    };

    /**
     * It adds a {range} days for the first date
     * Not more than 4 weeks from the first date
     * @param range {{3 | 7}}  Range is the factor to add 3 is for mobile 7 for larger screens
     * */
    nextWeek = range => this.setState(state => {
        const nextWeek = state.firstDate.clone().add(range, 'days');
        if (!nextWeek.isAfter(this.firstDateAfter4weeks))
            return state.firstDate = nextWeek;
    }, () => this.createTimeTable());

    /**
     * It removes a {range} days for the first date
     * Not more less than the current date
     * @param range {{3 | 7}}  Range is the factor to add 3 is for mobile 7 for larger screens
     * */
    lastWeek = range => this.setState(state => {
        const lastWeek = state.firstDate.clone().add(-range, 'days');
        if (!lastWeek.isBefore(moment().subtract(1, "days")))
            return state.firstDate = lastWeek;
    }, () => this.createTimeTable());


    /**
     * It removes any selected time slot
     * then
     * It selects the new picked time slot
     * @param i {number} stWeekDays pointer for the selected day
     * @param j {number} slots pointer for the selected slot in the above day
     * */
    selectTimeSlot = (i, j) => this.setState(state => {
        // remove any prev selected button
        state.stWeekDays.forEach(weekDay => weekDay.slots.forEach(slot => slot.selected = false));
        const currentSlot = state.stWeekDays[i].slots[j];
        // select the new one
        currentSlot.selected = true;
        // store the selected day and slot
        state.selectTimeSlot = `${currentSlot.dateMoment.format('YYYY-MM-DD')} ${currentSlot.timeMoment.format('HH:mm')}`;
        // Server expect something like this: 2019-06-23 16:00
        return state
    });

    render() {

        const range = this.state.width < 700 ? 3 : 7;
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

                    <div className={styles.Title}>
                        {
                            this.props.appointment ?
                                <Typography>
                                    <Title>Hi {this.props.appointment.userName} </Title>
                                    <Paragraph>
                                        In the process of internal desktop applications development, many different
                                        design specs
                                        and
                                        implementations would be involved, which might cause designers and developers
                                        difficulties and
                                        duplication and reduce the efficiency of development.
                                    </Paragraph>
                                </Typography>
                                : <Skeleton active/>
                        }
                    </div>

                    <div className={styles.Container}>

                        {
                            this.props.appointment ?
                                <div className={styles.Table}>
                                    <div className={styles.TableContent}>
                                        <Button className={styles.NavigateButtons}
                                                onClick={() => this.lastWeek(range)}
                                                icon={'left'} size={'large'}></Button>

                                        <div className={styles.Columns}>
                                            {
                                                this.state.stWeekDays.map((weekDay, i) =>
                                                    <div key={i}>
                                                        <div className={styles.Header}>
                                                            <h3>{weekDay.dayText}</h3>
                                                            {weekDay.monthText} {weekDay.day}
                                                        </div>
                                                        {
                                                            <div className={styles.Body}>
                                                                {
                                                                    weekDay.slots.map(
                                                                        (slot, j) =>
                                                                            <Button key={j} block
                                                                                    onClick={() => this.selectTimeSlot(i, j)}
                                                                                    type={slot.selected ? 'primary' : ''}
                                                                                    disabled={!slot.active}>{slot.time}</Button>
                                                                    )
                                                                }
                                                            </div>
                                                        }

                                                    </div>
                                                )
                                            }
                                        </div>

                                        <Button className={styles.NavigateButtons}
                                                onClick={() => this.nextWeek(range)}
                                                icon={'right'} size={'large'}></Button>
                                    </div>
                                </div>
                                : <Skeleton active={true}/>
                        }

                        {
                            this.props.appointment ?
                                <div style={{width: '100%'}}>
                                    <Button type={'primary'}
                                            style={{marginTop: 10, float: 'right'}}
                                            size={'large'}>Submit</Button>
                                </div>
                                : <Skeleton active={true}/>
                        }

                    </div>
                </div>

            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        appointment: state.appointmentsPicker.appointment,
    };
}

export default connect(mapStateToProps)(AppointmentsPicker);
