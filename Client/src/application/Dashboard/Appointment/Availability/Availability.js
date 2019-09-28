import React from 'react'
import styles from "../../AutoPilots/AutoPilot/AutoPilot.module.less";
import moment from "moment";
import momentTZ from 'moment-timezone'
import {connect} from 'react-redux'

import {Badge, Checkbox, Col, Form, List, Radio, Tag, Input,TimePicker, message, Button} from 'antd'
import 'types/TimeSlots_Types'
import 'types/AutoPilot_Types'

import {availabilityActions} from "store/actions";


class Availability extends React.Component {

    constructor(props){
        super(props)
        this.state = {
            saved: false,
            Name: props.name,
            ID: props.id,
            Info: props.info,
            nameError: null
        }
    }

    componentWillMount() {
      this.props.dispatch(availabilityActions.fetchAvailability)
    }

    componentDidMount() {
        console.log(this.props.tz)
        console.log(availabilityActions)
    }

    render() {
       return(<div>lol</div>)
    }
}


function mapStateToProps(state) {
    return {
        availability: state.availability.availability
    };
}

export default connect(mapStateToProps, null)(Availability);
