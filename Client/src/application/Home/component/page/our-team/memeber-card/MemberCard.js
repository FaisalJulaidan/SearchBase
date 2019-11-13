import React from 'react';
import PropTypes from "prop-types";
import {Card} from "react-bootstrap";
import styles from "./member-card.module.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faFacebook, faGithub, faLinkedin} from "@fortawesome/free-brands-svg-icons";
import {faTwitter} from "@fortawesome/free-brands-svg-icons/faTwitter";
import {getLink} from "helpers";

const MemberCard = (props) => {
    return (
        <Card className={styles.card}>
            <div className={styles.img_container}>
                <Card.Img className={styles.img} variant="top" src={getLink(props.img)}/>
            </div>
            <Card.Body>
                <h4 className={styles.name}>{props.name}</h4>
                <h1 className={styles.title}>{props.title}</h1>
                <p className={styles.description}>{props.desc}</p>
                <div className={styles.icon_wrapper}
                     style={{
                         display: (typeof props.linkedin != "undefined") && (typeof props.facebook != "undefined")
                         && (typeof props.twitter != "undefined") && (typeof props.github != "undefined") ? 'block' : 'none'
                     }}>
                    <a style={{display: (typeof props.linkedin != "undefined") ? 'block' : 'none'}}
                       target="_blank"
                       rel="noopener noreferrer"
                       href={"https://www.linkedin.com/in/" + props.linkedin}>
                        <FontAwesomeIcon className={styles.icon} color="#0177B5" icon={faLinkedin}/>
                    </a>
                    <a style={{display: (typeof props.facebook != "undefined") ? 'block' : 'none'}} target="_blank"
                       rel="noopener noreferrer" href={"https://www.facecbook.com/" + props.facebook}>
                        <FontAwesomeIcon className={styles.icon} color="#3A5CA0" icon={faFacebook}/>
                    </a>
                    <a style={{display: (typeof props.twitter != "undefined") ? 'block' : 'none'}} target="_blank"
                       rel="noopener noreferrer" href={"https://twitter.com/" + props.twitter}>
                        <FontAwesomeIcon className={styles.icon} color="#1DA1F2" icon={faTwitter}/>
                    </a>
                    <a style={{display: (typeof props.github != "undefined") ? 'block' : 'none'}} target="_blank"
                       rel="noopener noreferrer" href={"https://github.com/" + props.github}>
                        <FontAwesomeIcon className={styles.icon} color="#24292E" icon={faGithub}/>
                    </a>
                </div>
            </Card.Body>
        </Card>
    );
};

MemberCard.propTypes = {
    name: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    img: PropTypes.string.isRequired,
    desc: PropTypes.string,
    linkedin: PropTypes.string,
    twitter: PropTypes.string,
    facebook: PropTypes.string,
    github: PropTypes.string,
};

export default MemberCard;
