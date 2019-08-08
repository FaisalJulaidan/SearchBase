import React from 'react'

import styles from './Phone.module.less'

import phone from './phone.png'

export default class Phone extends React.Component {

    render() {
        return(
            <div style={{backgroundImage: `url(${phone})`}} className={styles.image}>
                <div className={styles.messages}>
                    {this.props.messages.map(message => {
                        return (<div className={styles.message}>{message}</div>)
                    })}
                </div>
            </div>
        )
    }
}