import React from 'react';
import styles from '../../AutoPilots/Assistant/AutoPilot.module.less';
import moment from 'moment';
import momentTZ from 'moment-timezone';
import { convertTimezone, getTimezone } from 'helpers';


import { Badge, Checkbox, Col, Form, List, Radio, Tag, Input, TimePicker, message, Button } from 'antd';
import 'types/TimeSlots_Types';
import 'types/AutoPilot_Types';


const FormItem = Form.Item;


class TimeSlot extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            saved: false,
            Name: props.name,
            ID: props.id,
            Info: props.info,
            nameError: null
        };
    }

    componentDidMount() {
        this.setState({
            Info: this.state.Info.map(item => ({
                ...item,
                From: convertTimezone(item.From, 'HH:mm:ss'),
                To: convertTimezone(item.To, 'HH:mm:ss')
            }))
        });
    }

    infoKVChange = (day, key, value) => {
        console.log(value);
        let aat = this.state.Info.slice();
        if (day === null) {
            aat = aat.map(day => ({ ...day, [key]: value }));
        } else {
            aat.find(wd => wd.Day === day)[key] = value;
        }
        this.setState({ Info: aat }, () => console.log(this.state));
    };

    mainKVChange = (key, value) => {
        let nameError = null;
        if (key === 'Name') {
            if (!this.props.checkNameAllowed(value, this.props.name)) {
                nameError = 'Name is already taken! Please chose something else!';
            }
        }
        this.setState({ [key]: value, nameError });
    };

    saveSettings = () => {
        if (this.state.nameError) {
            message.error('Your inputs have errors, please check them and try again!');
            return;
        }

        // Convert it back to UTC for the server
        const setTimeToUTC = (time, day) => {
            return momentTZ.tz(`${time} ${day}`, 'HH:mm:ss d', getTimezone()).utc().format('HH:mm');
        };

        let savedSettings = {
            Name: this.state.Name,
            Duration: this.state.Info[0].Duration,
            Info: this.state.Info.map(fullDay => ({
                ...fullDay,
                Day: fullDay.Day,
                From: setTimeToUTC(fullDay.From, fullDay.Day),
                To: setTimeToUTC(fullDay.To, fullDay.Day)
            }))
        };
        this.props.save(savedSettings);
    };

    render() {
        const TimeRange = weekDay => {
            let to = moment(weekDay.To, 'HH:mm:ss');
            let from = moment(weekDay.From, 'HH:mm:ss');

            return (
                <>
                    <span className={styles.TimeRange}>
                        <TimePicker value={from} format={'HH:mm'} minuteStep={30}
                                    onChange={(time, str) => this.infoKVChange(weekDay.Day, 'From', str)}
                                    disabled={!weekDay.Active}/>
                    </span>
                    <span style={{ marginRight: '5px', marginLeft: '5px' }}>-</span>
                    <span className={styles.TimeRange}>
                        <TimePicker value={to} format={'HH:mm'} minuteStep={30}
                                    disabledHours={() => Array.apply(null, { length: from.hours() + 1 }).map(Number.call, Number)}
                                    onChange={(time, str) => this.infoKVChange(weekDay.Day, 'To', str)}
                                    disabled={!weekDay.Active || !weekDay.From}/>
                    </span>
                </>
            );
        };

        const TotalSlots = (From, To, duration) => {
            let from = moment(From, 'HH:mm:ss');
            let to = moment(To, 'HH:mm:ss');
            let minutes = to.diff(from, 'minutes');
            return Math.round(minutes / duration);
        };

        return (

            <Form>
                <FormItem
                    label="Appoitment Allocation Table Name"
                    validateStatus={this.state.nameError ? 'error' : ''}
                    help={this.state.nameError}
                    extra="Set a unique name for your timetable">
                    <Input value={this.state.Name} placeholder="Enter the name for your Appoitment Allocation Table"
                           onChange={e => this.mainKVChange('Name', e.target.value)}/>
                </FormItem>
                <FormItem
                    label="Appointment Duration"
                    extra="This is will change the number of appointment slots per day"
                >
                    <Radio.Group value={this.state.Info[0].Duration}
                                 onChange={e => this.infoKVChange(null, 'Duration', e.target.value)}>
                        <Radio.Button value={60}>1 Hour</Radio.Button>
                        <Radio.Button value={30}>30 Minutes</Radio.Button>
                    </Radio.Group>
                </FormItem>
                <FormItem
                    label="Timetable selection"
                    extra="Select the days, and times in those days in which you would like to have appointments">
                    <List bordered
                          dataSource={this.state.Info}
                          style={{ width: 700 }}
                          renderItem={(weekDay, i) => (
                              <List.Item key={i}>
                                  <Col span={6}>
                                      <Checkbox className={styles.CheckBox}
                                                checked={weekDay.Active}
                                                onChange={event => this.infoKVChange(weekDay.Day, 'Active', event.target.checked)}/>
                                      <Tag style={{ marginTop: 6 }}
                                           color={weekDay.Active ? 'purple' : 'grey'}>
                                          {moment().isoWeekday(weekDay.Day + 1).format('dddd')}
                                      </Tag>
                                  </Col>

                                  <Col span={12}>
                                      {TimeRange(weekDay)}
                                  </Col>

                                  <Col span={6}>
                                      {weekDay.To && weekDay.From && weekDay.Active &&
                                      <div style={{ display: 'flex' }}>
                                          <p style={{ margin: 0 }}>Total slots: </p>
                                          <Badge count={TotalSlots(weekDay.From, weekDay.To, weekDay.Duration)}
                                                 style={{
                                                     backgroundColor: '#fff',
                                                     color: 'black',
                                                     marginTop: 2,
                                                     width: 30
                                                 }}/>
                                      </div>}
                                  </Col>

                              </List.Item>
                          )}/>
                </FormItem>
                <Button onClick={() => this.saveSettings()}>Save Changes</Button>
            </Form>

        );
    }
}


export default TimeSlot;
