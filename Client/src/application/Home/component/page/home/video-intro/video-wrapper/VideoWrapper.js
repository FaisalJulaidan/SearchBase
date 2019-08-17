import React, {Component} from 'react';
import styles from './video-wrapper.module.css';
import {Image} from "react-bootstrap";

class VideoWrapper extends Component {
    render() {
        return (
            <div className={styles.video_frame}>
                    <Image className={styles.image} fluid src="assets/img/home/iphone-x.png"/>
                <div className={styles.background}/>
                <Image className={styles.background2} src="assets/img/home/video-intro-bg.svg"/>
                <div className={styles.video}>
                    {this.props.children}
                </div>
            </div>
        );
    }
}

export default VideoWrapper;