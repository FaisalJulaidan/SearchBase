import React from 'react'
import styles from "../../AutoPilots/AutoPilot/AutoPilot.module.less";
import moment from "moment";
import {connect} from 'react-redux'
import {Badge, Checkbox, Col, Form, List, Radio, Tag, TimePicker} from 'antd'
import 'types/TimeSlots_Types'
import 'types/AutoPilot_Types'
import {appointmentAllocationTimeActions} from "store/actions";

const FormItem = Form.Item;

class TimeSlots extends React.Component {

    componentDidMount() {
        const /**@type AutoPilot*/x = this.props.autoPilot;

        this.props.dispatch(appointmentAllocationTimeActions.fetchAAT());
        console.log(this.props)
        // this.setState(state => {
        //     state.duration = x.OpenTimes[0].Duration + 'min';
        //     state.weekDays.forEach((weekDay, i) => {
        //         weekDay.active = x.OpenTimes[i].Active;
        //         weekDay.from = moment(x.OpenTimes[i].From, "HHmmss");
        //         weekDay.to = moment(x.OpenTimes[i].To, "HHmmss");
        //     })
        // })

    }

    state = {
        duration: '60min',
        /** @type {WeekDay[]}*/
        weekDays: [
            {
                day: 'Monday',
                active: false,
                from: null,
                to: null,
            },
            {
                day: 'Tuesday',
                active: false,
                from: null,
                to: null,
            },
            {
                day: 'Wednesday',
                active: false,
                from: null,
                to: null,
            },
            {
                day: 'Thursday',
                active: false,
                from: null,
                to: null,
            },
            {
                day: 'Friday',
                active: false,
                from: null,
                to: null,
            },
            {
                day: 'Saturday',
                active: false,
                from: null,
                to: null,
            },
            {
                day: 'Sunday',
                active: false,
                from: null,
                to: null,
            },
        ]
    };

    handleActivateDay = (event, day) => this.setState(state => state.weekDays.find(wd => wd.day === day).active = event.target.checked);
    handleChangeTime = (time, day, origin) => this.setState(state => state.weekDays.find(wd => wd.day === day)[origin] = time);

    render() {
        const { getFieldDecorator } = this.props.form
        const TimeRange = /** @type {WeekDay}*/weekDay => {
            return (
                <>
                    <span className={styles.TimeRange}>
                        <TimePicker value={weekDay.from} format={'HH:mm'} minuteStep={30}
                                    onChange={time => this.handleChangeTime(time, weekDay.day, 'from')}
                                    disabled={!weekDay.active}/>
                    </span>

                    <span style={{marginRight: '5px', marginLeft: '5px'}}>-</span>

                    <span className={styles.TimeRange}>
                        <TimePicker value={weekDay.to} format={'HH:mm'} minuteStep={30}
                                    disabledHours={() => Array.apply(null, {length: weekDay.from.hours() + 1}).map(Number.call, Number)}
                                    onChange={time => this.handleChangeTime(time, weekDay.day, 'to')}
                                    disabled={!weekDay.active || !weekDay.from}/>
                    </span>
                </>
            );
        };
        const CheckBox = (day, active) => <Checkbox className={styles.CheckBox}
                                                    checked={active}
                                                    onChange={event => this.handleActivateDay(event, day)}/>;
        const TotalSlots = (From, To) => {
            if (From && To) {
                // 7:30 -> 11:00
                const hours = moment.duration(To.diff(From)).hours(); // 3
                const minutes = moment.duration(To.diff(From)).minutes();// 30
                const totalHalfHours = (minutes / 30) + (hours * 2); // 1 + 6 = 7

                if (this.state.duration === "60min")
                    if (totalHalfHours < 2) {
                        return 'Non';
                    }
                    else
                        return Math.ceil(totalHalfHours / 2);
                else
                    return totalHalfHours;
            }
        };

        return (
            <Form>
                <FormItem
                    label="Appointment Duration"
                    extra="This is will change the number of appointment slots per day"
                    {...this.props.layout}>
                    {getFieldDecorator('appointmentDuration', {
                        initialValue: this.state.duration,
                        onChange: (e) => this.setState({duration: e.target.value}),
                        rules: [{}],
                    })(
                        <Radio.Group>
                            <Radio.Button value="60min">1 Hour</Radio.Button>
                            <Radio.Button value="30min">30 Minutes</Radio.Button>
                        </Radio.Group>,
                    )}
                </FormItem>

                <div style={{ width: 850}}>
                    {
                        <List bordered
                              dataSource={this.state.weekDays}
                              renderItem={weekDay => (
                                  <List.Item>
                                      <Col span={6}>
                                          {CheckBox(weekDay.day, weekDay.active)}
                                          <Tag style={{marginTop: 6}}
                                               color={weekDay.active ? 'purple' : 'grey'}>
                                              {weekDay.day}
                                          </Tag>
                                      </Col>

                                      <Col span={12}>
                                          {TimeRange(weekDay)}
                                      </Col>

                                      <Col span={6}>
                                          {
                                              weekDay.to && weekDay.from && weekDay.active &&
                                              <div style={{display: 'flex'}}>
                                                  <p style={{margin: 0}}>Total slots: </p>
                                                  <Badge count={TotalSlots(weekDay.from, weekDay.to)}
                                                         style={{
                                                             backgroundColor: '#fff',
                                                             color: 'black',
                                                             marginTop: 2,
                                                             width: 30
                                                         }}/>
                                              </div>
                                          }
                                      </Col>

                                  </List.Item>
                              )}/>
                    }
                </div>

            </Form>
        )
    }
}

const mapStateToProps = (state) => ({
    appointmentAllocationTime: state.appointmentAllocationTime.allocationTimes
})

export default connect(mapStateToProps, null)(Form.create()(TimeSlots))
