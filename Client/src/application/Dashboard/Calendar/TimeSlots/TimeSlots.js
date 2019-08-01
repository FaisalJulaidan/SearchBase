import React from 'react'
import styles from "../../AutoPilots/AutoPilot/AutoPilot.module.less";
import moment from "moment";
import {connect} from 'react-redux'
import {Badge, Checkbox, Col, Form, List, Radio, Tag, Input,TimePicker, Dropdown, Menu, Icon, message, Button} from 'antd'
import 'types/TimeSlots_Types'
import 'types/AutoPilot_Types'
import {appointmentAllocationTimeActions} from "store/actions";
import UserInput from "../../Assistants/Assistant/Flow/Blocks/CardTypes/UserInput";

const FormItem = Form.Item;

const dupeData = (day) => ({
    Day: day,
    Duration: 30,
    Active: false,
    From: "08:30:00",
    To: "12:00:00",
})


const emptyAAT = (id) =>  ({
    Name: "",
    ID: id,
    Info: new Array(7).fill(0).map((index, i) => dupeData(i))
});


class TimeSlots extends React.Component {

    state = {
        creating: false,
        saved: false,
        Name: "",
        ID: null,
        Info: emptyAAT().Info
    }

    getCurrent = () => this.state.creating ? ({Info: this.state.Info, ID: this.state.ID, Name: this.state.Name}) : this.props.active


    componentDidMount() {
        this.props.dispatch(appointmentAllocationTimeActions.fetchAAT());
    }

    componentWillReceiveProps() {
        if(!this.state.activeID && this.props.appointmentAllocationTime.length !== 0){
            this.setState({activeID:  this.props.appointmentAllocationTime[0].ID })
        }
        this.setState({saved: true, creating: false})
    }

    infoKVChange = (activeID, day, key, value) => {
        let aat = this.getCurrent()
        if(day === null) {
            aat.Info = aat.Info.map(day => ({...day, [key]: value}))
        } else {
            aat.Info.find(wd => wd.Day === day)[key] = value
        }
        this.setState({Info: aat.Info}, () => console.log(this.state))
    }

    mainKVChange = (activeID, key, value) => {
        let currentAAT = this.getCurrent()
        currentAAT[key] = value
        this.setState({[key]: value})
    }

    saveSettings = () => {
        let active = this.getCurrent()
        let savedSettings = {
            name: active.Name,
            duration: active.Info[0].Duration,
            weekDays: active.Info.map(fullDay => ({...fullDay, day: fullDay.Day , from: fullDay.From, to: fullDay.To}))
        }
        if(this.state.creating){
            this.props.dispatch(appointmentAllocationTimeActions.createAAT(savedSettings))
        } else {
            this.props.dispatch(appointmentAllocationTimeActions.saveAAT({...savedSettings, id: active.ID}))
        }
    }

    handleActiveDayChange = event => {
        this.props.dispatch(appointmentAllocationTimeActions.switchActiveAAT(event.key))
        this.setState({
            saved: false,
        })
    }

    createNewAAT = () => {
        this.setState({...emptyAAT(Math.random().toString(36).slice(2)), creating: true})
    }

    render() {
        const active = this.getCurrent()
        const menu = (<Menu onClick={this.handleActiveDayChange}>
            {this.props.appointmentAllocationTime.map(time => {
                return (
                    <Menu.Item key={time.ID}>
                        {time.Name}
                    </Menu.Item>
                )
            })}
        </Menu>)

        const TimeRange = weekDay => {
            let to = moment(weekDay.To, "HH:mm:ss")
            let from = moment(weekDay.From, "HH:mm:ss")
            return (
                <>
                    <span className={styles.TimeRange}>
                        <TimePicker value={from} format={'HH:mm'} minuteStep={30}
                                    onChange={time => this.infoKVChange(active.ID, weekDay.Day,'From', time)}
                                    disabled={!weekDay.Active}/>
                    </span>
                    <span style={{marginRight: '5px', marginLeft: '5px'}}>-</span>
                    <span className={styles.TimeRange}>
                        <TimePicker value={to} format={'HH:mm'} minuteStep={30}
                                    disabledHours={() => Array.apply(null, {length: from.hours() + 1}).map(Number.call, Number)}
                                    onChange={time => this.infoKVChange(active.ID, weekDay.Day,'To', time)}
                                    disabled={!weekDay.Active || !weekDay.From}/>
                    </span>
                </>
            );
        };

        const TotalSlots = (From, To, duration) => {
            let from = moment(From, "HH:mm:ss")
            let to = moment(To, "HH:mm:ss")
            let minutes = to.diff(from, 'minutes')
            return Math.round(minutes/duration)
        };

        return (
            <>
                {active ?
                    <>

                <Form>
                    <FormItem
                        label="Select the timetable you would like to change"
                        extra="Pick the timetable you would like to modify, or create a new one">
                        <Dropdown overlay={menu}>
                            <Button>
                                {active.Name}
                            </Button>
                        </Dropdown>
                        <Button icon="plus" onClick={this.createNewAAT}>
                            Create new
                        </Button>
                    </FormItem>
                    <FormItem
                        label="Appoitment Allocation Table Name"
                        extra="Set a unique name for your timetable">
                        <Input value={active.Name} onChange={e => this.mainKVChange(this.state.activeID, 'Name', e.target.value)} />
                    </FormItem>
                    <FormItem
                        label="Appointment Duration"
                        extra="This is will change the number of appointment slots per day"
                        >
                        <Radio.Group value={active.Info[0].Duration} onChange={e => this.infoKVChange(active.ID, null, 'Duration', e.target.value)}>
                            <Radio.Button value={60}>1 Hour</Radio.Button>
                            <Radio.Button value={30}>30 Minutes</Radio.Button>
                        </Radio.Group>
                    </FormItem>
                    <FormItem
                        label="Timetable selection"
                        extra="Select the days, and times in those days in which you would like to have appointments">
                            <List bordered
                                  dataSource={active.Info}
                                  style={{width: 700}}
                                  renderItem={(weekDay, i) => (
                                      <List.Item key={i}>
                                          <Col span={6}>
                                              <Checkbox className={styles.CheckBox}
                                                        checked={weekDay.Active}
                                                        onChange={event => this.infoKVChange(this.state.activeID, weekDay.Day, 'Active', event.target.checked)}/>
                                              <Tag style={{marginTop: 6}}
                                                   color={weekDay.Active ? 'purple' : 'grey'}>
                                                  {console.log(weekDay.Day)}
                                                  {moment().isoWeekday(weekDay.Day+1).format('dddd')}
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
                </Form>
                <br />
                <Button onClick={() => this.saveSettings(active.ID)}>Save Changes</Button>
            </> : null }
            </>
        )
    }
}

const mapStateToProps = (state) => ({
    appointmentAllocationTime: state.appointmentAllocationTime.allocationTimes,
    active: state.appointmentAllocationTime.aat
})

export default connect(mapStateToProps, null)(TimeSlots)
