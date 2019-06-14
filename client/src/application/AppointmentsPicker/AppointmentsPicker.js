import React from 'react'
import styles from './AppointmentsPicker.module.less'
import {Button, Typography} from 'antd'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import moment from 'moment';

const {Title, Paragraph, Text} = Typography;

class AppointmentsPicker extends React.Component {

    constructor(props) {
        super(props);
        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
    }

    state = {
        width: 0,
        height: 0,
        firstDate: moment(),
    };

    firstDateAfter4weeks = moment().add(3, 'weeks');

    componentDidMount() {
        this.updateWindowDimensions();
        window.addEventListener('resize', this.updateWindowDimensions);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateWindowDimensions);
    }

    updateWindowDimensions() {
        this.setState({width: window.innerWidth, height: window.innerHeight});
    }

    getPadding = () => {
        const is_xl = this.state.width >= 1400;
        const is_lg = this.state.width >= 1100;
        const is_md = this.state.width >= 800;

        if (is_xl)
            return {padding: '0 250px'};
        else if (is_lg)
            return {padding: '0 200px'};
        else if (is_md)
            return {padding: '0 100px'};
        else if (this.state.width < 800)
            return {padding: 25};
    };

    getTimeSlots = (From, To, duration) => {
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

    nextWeek = () => this.setState(state => {
        const nextWeek = state.firstDate.clone().add(7, 'days');
        if (!nextWeek.isAfter(this.firstDateAfter4weeks))
            return state.firstDate = nextWeek;
    });

    lastWeek = () => this.setState(state => {
        const lastWeek = state.firstDate.clone().add(-7, 'days');
        if (!lastWeek.isBefore(moment().subtract(1, "days")))
            return state.firstDate = lastWeek;
    });

    render() {

        const weekDaysKey = {
            0: 'Sun',
            1: 'Mon',
            2: 'Tue',
            3: 'Wed',
            4: 'Thu',
            5: 'Fri',
            6: 'Sat',
        };

        const range = 7;

        let weekDays = [];

        const json_res = {
            companyLogoURL: null,
            openTimes: [
                {
                    ID: 1,
                    Day: 0,
                    From: '08:30:00',
                    To: '10:30:00',
                    Duration: 60,
                    Active: true,
                    AutoPilotID: 1
                },
                {
                    ID: 2,
                    Day: 1,
                    From: '08:30:00',
                    To: '10:30:00',
                    Duration: 60,
                    Active: false,
                    AutoPilotID: 1
                },
                {
                    ID: 3,
                    Day: 2,
                    From: '08:30:00',
                    To: '10:30:00',
                    Duration: 60,
                    Active: true,
                    AutoPilotID: 1
                },
                {
                    ID: 4,
                    Day: 3,
                    From: '08:30:00',
                    To: '10:30:00',
                    Duration: 60,
                    Active: true,
                    AutoPilotID: 1
                },
                {
                    ID: 5,
                    Day: 4,
                    From: '08:30:00',
                    To: '10:30:00',
                    Duration: 60,
                    Active: false,
                    AutoPilotID: 1
                },
                {
                    ID: 6,
                    Day: 5,
                    From: '08:30:00',
                    To: '10:30:00',
                    Duration: 60,
                    Active: false,
                    AutoPilotID: 1
                },
                {
                    ID: 7,
                    Day: 6,
                    From: '00:00:00',
                    To: '10:30:00',
                    Duration: 30,
                    Active: true,
                    AutoPilotID: 1
                }
            ],
            takenTimeSlots: [
                {
                    ID: 1,
                    DateTime: "Wed, 19 Jun 2019 9:30:39 GMT",
                    AssistantID: 1,
                    ConversationID: 1
                },
                {
                    ID: 1,
                    DateTime: "Sun, 16 Jun 2019 10:30:39 GMT",
                    AssistantID: 1,
                    ConversationID: 1
                },
                {
                    ID: 1,
                    DateTime: "Wed, 19 Jun 2019 8:30:39 GMT",
                    AssistantID: 1,
                    ConversationID: 1
                }
            ],
            userName: 'Faisal Julaidan'
        };


        for (let i = 0; i < range; i++) {
            const date = this.state.firstDate.clone().add(i, 'days');
            const weekDay = {
                day: date.date(),
                dayText: date.format('ddd'), // Sun
                month: date.month(),
                monthText: date.format('MMM'), // Jun
                year: date.year(),

                slots: []
            };

            const svWeekDay = json_res.openTimes.find(ot => weekDaysKey[ot.Day] === weekDay.dayText);

            svWeekDay.To = moment(svWeekDay.To, 'HH:mm');
            svWeekDay.From = moment(svWeekDay.From, 'HH:mm');

            const totalSlots = this.getTimeSlots(
                svWeekDay.From,
                svWeekDay.To,
                svWeekDay.Duration
            );

            // generate slots
            for (let j = 0; j <= totalSlots; j++) {
                if (j === 0)
                    weekDay.slots.push({
                        active: svWeekDay.Active,
                        duration: svWeekDay.Duration,
                        time: svWeekDay.From.format('HH:mm')
                    });
                else
                    weekDay.slots.push({
                        active: svWeekDay.Active,
                        duration: svWeekDay.Duration,
                        time: svWeekDay.From.add(svWeekDay.Duration, 'minutes').format('HH:mm')
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
            json_res.takenTimeSlots.forEach((timeSlot) => {
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

                <div className={styles.Wrapper} style={this.getPadding()}>

                    <div className={styles.Title}>
                        <Typography>
                            <Title>Introduction</Title>
                            <Paragraph>
                                In the process of internal desktop applications development, many different design specs
                                and
                                implementations would be involved, which might cause designers and developers
                                difficulties and
                                duplication and reduce the efficiency of development.
                            </Paragraph>
                            <Paragraph>
                                After massive project practice and summaries, Ant Design, a design language for
                                background
                                applications, is refined by Ant UED Team, which aims to{' '}
                                <Text strong>
                                    uniform the user interface specs for internal background projects, lower the
                                    unnecessary
                                    cost of design differences and implementation and liberate the resources of design
                                    and
                                    front-end development
                                </Text>
                            </Paragraph>
                        </Typography>
                    </div>

                    <div className={styles.Container}>

                        <div className={styles.Table}>
                            <div className={styles.TableContent}>
                                <Button className={styles.NavigateButtons}
                                        onClick={() => this.lastWeek()}
                                        icon={'left'} size={'large'}></Button>

                                <div className={styles.Columns}>
                                    {
                                        weekDays.map((weekDay, i) =>
                                            <div key={i}>
                                                <div className={styles.Header}>
                                                    <h3>{weekDay.dayText}</h3>
                                                    {weekDay.monthText} {weekDay.day}
                                                </div>
                                                {
                                                    <div className={styles.Body}>
                                                        {
                                                            weekDay.slots.map(
                                                                (slot, i) =>
                                                                    <Button key={i} block
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
                                        onClick={() => this.nextWeek()}
                                        icon={'right'} size={'large'}></Button>
                            </div>
                        </div>

                        <div style={{width: '100%'}}>
                            <Button type={'primary'} style={{marginTop: 10, float: 'right'}}
                                    size={'large'}>Submit</Button>
                        </div>
                    </div>
                </div>

            </div>
        )
    }
}

export default AppointmentsPicker
