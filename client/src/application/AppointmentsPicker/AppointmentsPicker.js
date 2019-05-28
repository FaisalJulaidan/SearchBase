import React from 'react'
import styles from './AppointmentsPicker.module.less'
import {Button, Row, Typography} from 'antd'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'

const {Title, Paragraph, Text} = Typography;

class AppointmentsPicker extends React.Component {

    render() {

        const weekDays = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday',
        ];
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
                        <Row type="flex" justify="center">

                            <div className={styles.Table}>
                                <div className={styles.TableContent}>
                                    <Button className={styles.NavigateButtons} icon={'left'} size={'large'}></Button>

                                    {
                                        weekDays.map((day) =>
                                            <div>
                                                <div className={styles.Header}>
                                                    <h3>{day}</h3>
                                                    Aug 7
                                                </div>
                                                {
                                                    day !== 'Saturday' &&
                                                    day !== 'Sunday' &&
                                                    <div className={styles.Body}>
                                                        <Button block>9:00</Button>
                                                        <Button block>9:30</Button>
                                                        <Button block disabled>10:00</Button>
                                                        <Button block>10:30</Button>
                                                        <Button block>11:00</Button>
                                                    </div>
                                                }

                                            </div>
                                        )
                                    }
                                    <Button className={styles.NavigateButtons} icon={'right'} size={'large'}></Button>
                                </div>
                            </div>
                            <div style={{width: '100%'}}>
                                <Button type={'primary'}
                                        style={{marginTop: 10, float: 'right', marginRight: 86}}
                                        size={'large'}>Submit</Button>
                            </div>
                        </Row>


                    </div>
                </div>

            </div>
        )
    }
}

export default AppointmentsPicker
