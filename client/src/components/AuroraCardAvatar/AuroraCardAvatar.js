import React from 'react';
import PropTypes from 'prop-types';
import styles from "./AuroraCardAvatar.module.less"
import {Tooltip, Typography} from 'antd';
import {getLink} from "helpers";

const {Title, Paragraph} = Typography;

class AuroraCardAvatar extends React.Component {
    render() {
        return (
            <Tooltip title={`Disconnect from first`} visible={false}>
                <button
                    style={{
                        pointerEvents: this.props.disabled ? 'none' : 'auto'
                    }}
                    className={[styles.SelectButton, styles.Unbuttonized, this.props.selected ? styles.Selected : ''].join(' ')}
                    onClick={this.props.onClick}>
                    <div className={styles.Main}>
                        <img src={getLink(this.props.image)} width={100} style={{
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
