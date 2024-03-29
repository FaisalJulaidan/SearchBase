import React from 'react';

import styles from './PublicPage.module.less';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloud } from '@fortawesome/free-solid-svg-icons';
import { Spin } from 'antd';
import queryString from 'query-string';

import { history } from '../helpers';
import axios from 'axios';

export const PublicPage = (Component, param, redirectIfFail, authUrl) => {
    return class extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                isLoading: true,
                success: null,
                data: null,
                error: null,
                key: null
            };
        }

        componentDidMount() {
            let params = queryString.parse(this.props.location.search);
            if (!params[param]) {
                history.push(redirectIfFail);
            }
            let url = `api/${authUrl}/${params[param]}`;
            axios.get(url).then(data => {
                this.setState({
                    isLoading: false,
                    success: true,
                    data: data.data,
                    key: params[param]
                });
            }).catch((req) => {
                this.setState({
                    isLoading: false,
                    success: false,
                    error: req.response.data.msg,
                    key: params[param]
                });
            });

        }

        render() {
            const { isLoading } = this.state;
            return (
                <div style={{ height: '100%' }}>
                    <div className={styles.Navbar}>
                        <div>
                            <FontAwesomeIcon size="2x" icon={faCloud} style={{ color: '#9254de' }}/>
                            <div style={{
                                lineHeight: '40px',
                                marginLeft: 18,
                                color: '#9254de'
                            }}>TheSearchBase
                            </div>
                        </div>
                    </div>

                    <div className={styles.Wrapper}>
                        <div>
                            {!isLoading ?
                                <Component success={this.state.success} data={this.state.data} error={this.state.error}
                                           token={this.state.key}/>
                                : <Spin style={{ margin: 'auto', display: 'block' }}/>}
                        </div>
                    </div>

                </div>
            );
        }
    };
};

export default PublicPage;
