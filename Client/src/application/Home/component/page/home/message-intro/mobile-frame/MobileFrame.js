import React, {Component} from 'react';
import styles from './mobile-frame.module.css';
import {Image} from "react-bootstrap";
import {getLink} from "helpers";
import {faCloud} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

class MobileFrame extends Component {

    items={

    };

    render() {
        return (
            <div className={styles.content_frame}>
                <Image className={styles.frame} fluid
                       src={"/images/home/home/iphone-x.png"}/>
                <div className={styles.background}/>
                <Image className={styles.background2}
                       src={"/images/home/home/video-intro-bg.svg"}/>
                <div className={styles.content}>
                    {this.props.children}
                </div>
                <div className={styles.label_wrapper}>
                    <h1 className={styles.label}>
                        Chat by
                        <FontAwesomeIcon className={styles.icon} size="1x" icon={faCloud}/>
                        <span className={styles.name}>SearchBase</span>
                    </h1>
                </div>
            </div>
        );
    }
}

export default MobileFrame;
