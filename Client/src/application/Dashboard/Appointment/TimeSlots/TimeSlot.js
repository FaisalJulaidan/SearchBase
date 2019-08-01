import React from 'react'
import styles from "../../AutoPilots/AutoPilot/AutoPilot.module.less";
import moment from "moment";
import {connect} from 'react-redux'
import {Badge, Checkbox, Col, Form, List, Radio, Tag, Input,TimePicker, Dropdown, Menu, Icon, message, Button, Tabs} from 'antd'
import 'types/TimeSlots_Types'
import 'types/AutoPilot_Types'
import {appointmentAllocationTimeActions} from "store/actions";
import UserInput from "../../Assistants/Assistant/Flow/Blocks/CardTypes/UserInput";


const FormItem = Form.Item;


class TimeSlot extends React.Component {

    constructor(props){
        super(props)
        this.state = {
            saved: false,
            Name: props.name,
            ID: props.id,
            Info: props.info
        }

    }

    infoKVChange = (day, key, value) => {
        let aat = this.state.Info.slice()
        if(day === null) {
            aat = aat.map(day => ({...day, [key]: value}))
        } else {
            aat.find(wd => wd.Day === day)[key] = value
        }
        this.setState({Info: aat}, () => console.log(this.state))
    }

    mainKVChange = (key, value) => {
        this.setState({[key]: value})
    }

    saveSettings = () => {
        let savedSettings = {
            name: this.state.Name,
            duration: this.state.Info[0].Duration,
            weekDays: this.state.Info.map(fullDay => ({...fullDay, day: fullDay.Day , from: fullDay.From, to: fullDay.To}))
        }
        this.props.save(savedSettings)
    }

    render() {
        const TimeRange = weekDay => {
            let to = moment(weekDay.To, "HH:mm:ss")
            let from = moment(weekDay.From, "HH:mm:ss")
            return (
                <>
                    <span className={styles.TimeRange}>
                        <TimePicker value={from} format={'HH:mm'} minuteStep={30}
                                    onChange={time => this.infoKVChange(weekDay.Day, 'From', time)}
                                    disabled={!weekDay.Active}/>
                    </span>
                    <span style={{marginRight: '5px', marginLeft: '5px'}}>-</span>
                    <span className={styles.TimeRange}>
                        <TimePicker value={to} format={'HH:mm'} minuteStep={30}
                                    disabledHours={() => Array.apply(null, {length: from.hours() + 1}).map(Number.call, Number)}
                                    onChange={time => this.infoKVChange( weekDay.Day, 'To', time)}
                                    disabled={!weekDay.Active || !weekDay.From}/>
                    </span>
                </>
            );
        };

        const TotalSlots = (From, To, duration) => {
            let from = moment(From, "HH:mm:ss")
            let to = moment(To, "HH:mm:ss")
            let minutes = to.diff(from, 'minutes')
            return Math.round(minutes / duration)
        };

        return (

            <Form>
                <FormItem
                    label="Appoitment Allocation Table Name"
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
                          style={{width: 700}}
                          renderItem={(weekDay, i) => (
                              <List.Item key={i}>
                                  <Col span={6}>
                                      <Checkbox className={styles.CheckBox}
                                                checked={weekDay.Active}
                                                onChange={event => this.infoKVChange(weekDay.Day, 'Active', event.target.checked)}/>
                                      <Tag style={{marginTop: 6}}
                                           color={weekDay.Active ? 'purple' : 'grey'}>
                                          {moment().isoWeekday(weekDay.Day + 1).format('dddd')}
                                      </Tag>
                                  </Col>

                                  <Col span={12}>
                                      {TimeRange(weekDay)}
                                  </Col>

                                  <Col span={6}>
                                      {weekDay.To && weekDay.From && weekDay.Active &&
                                      <div style={{display: 'flex'}}>
                                          <p style={{margin: 0}}>Total slots: </p>
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

        )
    }
}


export default TimeSlot
