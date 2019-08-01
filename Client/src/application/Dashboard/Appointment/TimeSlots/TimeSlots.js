import React from 'react'
import {connect} from 'react-redux'
import { Modal, Button, message, Tabs} from 'antd'
import 'types/TimeSlots_Types'
import 'types/AutoPilot_Types'
import {appointmentAllocationTimeActions} from "store/actions";
import TimeSlot from "./TimeSlot";

const { TabPane } = Tabs

const dupeData = (day) => ({
    Day: day,
    Duration: 30,
    Active: false,
    From: "08:30:00",
    To: "12:00:00",
})


const emptyAAT = (id) =>  ({
    ID: 'new',
    Name: "New Timetable",
    Info: new Array(7).fill(0).map((index, i) => dupeData(i))
});


class TimeSlots extends React.Component {

    state = {
        creating: false,
        activeKey: null
    }

    componentDidMount() {
        this.props.dispatch(appointmentAllocationTimeActions.fetchAAT());
    }

    saveTimeSlot = (id, newSettings) => {
        if(id === "new"){
            this.props.dispatch(appointmentAllocationTimeActions.createAAT(newSettings))

        } else {
            this.props.dispatch(appointmentAllocationTimeActions.saveAAT({...newSettings, id: id}))
        }
    }

    componentDidUpdate(){
        if(this.props.active && this.state.activeKey !== this.props.active?.ID){
            this.setState({activeKey: this.props.active.ID, creating: false})
        }
        if(this.props.appointmentAllocationTime.length !== 0 && !this.state.activeKey){
            this.setState({activeKey: this.props.appointmentAllocationTime[0].ID})
        }
        if(!this.props.isLoading && this.props.appointmentAllocationTime.length === 0 && !this.state.creating){
            this.setState({creating: true, activeKey: "new"})
        }
    }


    onChange = (key, action) => {
        this.setState({activeKey: key})
    }

    add = () => {
        if(!this.state.creating) {
            this.setState({creating: true, activeKey: `new`})
        } else {
            message.warn("Please finish working on your new timetable before you create a new one!")
        }
    }

    remove = (key) => {
        return Modal.confirm({
            title: 'Are you sure you want to delete this timetable?',
            content: 'You will lose this timetable foreve if it is deleted',
            okText: 'Yes',
            cancelText: 'No',
            onOk: (e) => {
                console.log(e)
                this.props.dispatch(appointmentAllocationTimeActions.deleteAATRequest(key))
                e()
            },
            maskClosable: true
        });
    }

    onEdit = (key, action) => {
        this[action](key)
    }


    render() {
        let tabList = this.props.appointmentAllocationTime.concat(this.state.creating ? [emptyAAT()] : [])
         return (
            <Tabs onChange={this.onChange}
                  type="editable-card"
                  activeKey={`${this.state.activeKey}`}
                  onEdit={this.onEdit}>
            {tabList.map((timeSlot, i) => {
                return (<TabPane tab={timeSlot.Name} key={`${timeSlot.ID}`} closable={timeSlot.ID === "new" ? false :true}>
                    <TimeSlot
                        info={timeSlot.Info}
                        id={timeSlot.ID}
                        name={timeSlot.Name}
                        save={newSettings => this.saveTimeSlot(timeSlot.ID, newSettings)}/>
                </TabPane>)
            })}
            </Tabs>
        )

    }
}

const mapStateToProps = (state) => ({
    appointmentAllocationTime: state.appointmentAllocationTime.allocationTimes,
    isLoading: state.appointmentAllocationTime.isLoading,
    active: state.appointmentAllocationTime.aat
})

export default connect(mapStateToProps, null)(TimeSlots)
