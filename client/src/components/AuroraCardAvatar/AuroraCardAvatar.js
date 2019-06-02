import React from 'react';
import PropTypes from 'prop-types';
import styles from "./AuroraCardAvatar.module.less"
import {Typography, Avatar, Tooltip, Tag, Divider, Icon} from 'antd';

const {Title, Text} = Typography;

class AuroraCardAvatar extends React.Component {
    render() {
        const getTag = (status) => {
            switch (status) {
                case 'CONNECTED':
                    return <Tag color={'#87d068'}><Icon type="safety"/> Connected</Tag>;
                case 'NOT_CONNECTED':
                    return <Tag>Not Connected</Tag>;
                case 'FAILED':
                    return <Tag color={'#f50'}><Icon type="disconnect"/> Failed</Tag>;
                default:
                    return null
            }
        };
        return (
            <Tooltip title={`Disconnect from first`} visible={false}>
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
                            <Divider/>
                            {getTag(this.props.status)}
                        </div>
                    </div>
                </button>
            </Tooltip>
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
    onClick: PropTypes.func,
    status: PropTypes.oneOf(['CONNECTED', 'NOT_CONNECTED', 'FAILED'])
};
export default AuroraCardAvatar
