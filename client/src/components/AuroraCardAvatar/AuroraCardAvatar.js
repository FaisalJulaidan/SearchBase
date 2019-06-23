import React from 'react';
import PropTypes from 'prop-types';
import styles from "./AuroraCardAvatar.module.less"
import {Icon, Tag, Tooltip, Typography} from 'antd';

const {Title, Paragraph} = Typography;

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
                case 'Comming Soon':
                    return <Tag color={'purple'}> Comming Soon</Tag>;
                default:
                    return null
            }
        };
        return (
            <Tooltip title={`Disconnect from first`} visible={false}>
                <button
                    style={{
                        pointerEvents: this.props.disabled ? 'none' : 'auto'
                    }}
                    className={[styles.SelectButton, styles.Unbuttonized, this.props.selected ? styles.Selected : ''].join(' ')}
                    onClick={this.props.onClick}>
                    <div className={styles.Main}>
                        <img src={this.props.image} width={100} style={{
                            float: 'left',
                            marginLeft: 20
                        }}/>
                        <div className={styles.Desc}>
                            <Typography>
                                <Title level={4}>{this.props.title}</Title>
                                <Paragraph type="secondary" ellipsis={{rows: 3}}>
                                    {this.props.desc}
                                </Paragraph>
                            </Typography>
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
    disabled: PropTypes.bool,
    status: PropTypes.oneOf(['CONNECTED', 'NOT_CONNECTED', 'FAILED', 'Comming Soon'])
};
export default AuroraCardAvatar
