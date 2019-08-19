import React, {Component} from 'react';
import styles from './mobile-frame.module.css';
import {Image} from "react-bootstrap";
import {getLink} from "helpers";

class MobileFrame extends Component {
    render() {
        return (
            <div className={styles.video_frame}>
                <Image className={styles.image} fluid
                       src={getLink("/static/images/home/home/iphone-x.png")}/>
                <div className={styles.background}/>
                <Image className={styles.background2}
                       src={getLink("/static/images/home/home/video-intro-bg.svg")}/>
                <div className={styles.video}>
                    {this.props.children}
                </div>
            </div>
        );
    }
}

export default MobileFrame;