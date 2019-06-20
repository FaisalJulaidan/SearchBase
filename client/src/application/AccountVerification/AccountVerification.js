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

    isSent = false;
    isVerified = false;

    componentDidMount() {
        this.requestToken = this.props.location.pathname.split('/')[2];
        this.props.dispatch(authActions.validateAccount(this.requestToken))
            .then(() => {
                this.isSent = true;
                this.isVerified = true;
                setTimeout(() => history.push(`/login`), 5000)
            })
            .catch(() => {
                this.isSent = true;
                this.isVerified = false;
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

                    {/*<div style={{textAlign: 'center'}}>*/}
                    {/*<img src={getLink('/static/images/undraw/success.svg')} alt="" height={300}/>*/}
                    {/*<Typography.Title>*/}
                    {/*Your account is verified*/}
                    {/*</Typography.Title>*/}
                    {/*</div>*/}


                    <div style={{textAlign: 'center'}}>
                        <img src={getLink('/static/images/undraw/failed.svg')} alt="" height={300}/>
                        <Title>
                            Account verification is failed
                        </Title>
                        <Paragraph type="secondary">
                            This might be the link is old, please contact us.
                        </Paragraph>
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
