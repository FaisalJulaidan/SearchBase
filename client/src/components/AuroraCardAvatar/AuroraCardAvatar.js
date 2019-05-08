import React from 'react';
import PropTypes from 'prop-types';
import styles from "./AuroraCardAvatar.module.less"
import {Typography, Avatar} from 'antd';

const {Title, Text} = Typography;

class AuroraCardAvatar extends React.Component {
    render() {
        return (
            <button
                className={[styles.SelectButton, styles.Unbuttonized, this.props.selected ? styles.Selected : ''].join(' ')}
                onClick={this.props.onClick}>
                <div className={styles.Main}>
                    <Avatar shape="square" style={{width: 100, height: 80}} src={this.props.image}/>
                    <div className={styles.Desc}>
                        <Typography>
                            <Title level={4}>{this.props.title}</Title>
                            <Text type="secondary">
                                {this.props.desc}
                            </Text>
                        </Typography>
                    </div>
                </div>
            </button>
        );
    }
}

AuroraCardAvatar.propTypes = {
    title: PropTypes.string,
    image: PropTypes.string,
    desc: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.element
    ]),
    onClick: PropTypes.func
};
export default AuroraCardAvatar
