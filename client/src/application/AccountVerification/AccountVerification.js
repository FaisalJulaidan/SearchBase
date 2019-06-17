import React from 'react'
import styles from './AccountVerification.module.less'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {connect} from 'react-redux';
import {getLink} from "helpers";
import {Typography} from 'antd';


class AccountVerification extends React.Component {

    requestToken = 'dummyText';

    componentDidMount() {
        this.requestToken = this.props.location.pathname.split('/')[2];
        console.log(this.requestToken);
        // this.props.dispatch(appointmentsPickerActions.fetchAppointment(this.requestToken));
    }

    render() {
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

                    <div style={{textAlign: 'center'}}>
                        <img src={getLink('/static/images/undraw/success.svg')} alt="" height={300}/>
                        <Typography.Title>
                            Your account is verified
                        </Typography.Title>
                    </div>

                </div>

            </div>
        )
    }
}

function mapStateToProps(state) {
    return {};
}

export default connect(mapStateToProps)(AccountVerification);
