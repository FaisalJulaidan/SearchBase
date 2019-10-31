import React from 'react'
import styles from './AccountVerification.module.less'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {connect} from 'react-redux';
import {getLink, history} from "helpers";
import {authActions} from "store/actions";
import {Typography} from "antd";

const {Title, Paragraph} = Typography;

class AccountVerification extends React.Component {

    requestToken = 'dummyText';

    state = {
        isSent: false,
        isVerified: false
    };

    componentDidMount() {
        this.setState({isSent: false, isVerified: false});

        this.requestToken = this.props.location.pathname.split('/')[2];

        this.props.dispatch(authActions.verifyAccount(this.requestToken))
            .then(() => {
                this.setState({isSent: true, isVerified: true});
                setTimeout(() => history.push(`/login`), 5000)
            })
            .catch(() => {
                this.setState({isSent: true, isVerified: false});
                setTimeout(() => window.location.href = 'http://thesearchbase.com', 5000)
            })
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

                    {
                        this.state.isSent &&
                        this.state.isVerified &&
                        <div style={{textAlign: 'center'}}>
                            <img src={"/images/undraw/success.svg"} alt="" height={300}/>
                            <Typography.Title>
                                Your account is verified
                            </Typography.Title>
                            <Paragraph type="secondary">
                                You will be redirected to login page in seconds
                            </Paragraph>
                        </div>
                    }

                    {
                        this.state.isSent &&
                        !this.state.isVerified &&
                        <div style={{textAlign: 'center'}}>
                            <img src={"/images/undraw/failed.svg"} alt="" height={300}/>
                            <Title>
                                Account verification is failed
                            </Title>
                            <Paragraph type="secondary">
                                This might be the link is old, please contact us.
                            </Paragraph>
                            <Paragraph type="secondary">
                                You will be redirected to home page in seconds
                            </Paragraph>
                        </div>
                    }


                </div>

            </div>
        )
    }
}

function mapStateToProps(state) {
    return {};
}

export default connect(mapStateToProps)(AccountVerification);
