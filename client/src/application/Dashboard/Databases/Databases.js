import React, {Component} from 'react';
import {Button, message, Skeleton} from 'antd';
import {connect} from 'react-redux';

import styles from "./Databases.module.less"

class Databases extends Component {
    state = {
        visible: false,
    };

    componentDidUpdate(prevProps) {

    }


    componentDidMount() {

    }


    showModal = () => this.setState({visible: true});
    hideModal = () => this.setState({visible: false});


    render() {
        return (
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>Databases List</h3>
                            <p>Here you can see all your sources of data</p>
                        </div>
                        <div>
                            <Button className={styles.Panel_Header_Button} type="primary" icon="plus"
                                    onClick={this.showModal}>
                                Add Database
                            </Button>
                        </div>
                    </div>


                    <div className={styles.Panel_Body}>
                        <div className={styles.DatabasesList}>
                            {/*{*/}
                                {/*this.props.assistantList[0] ?*/}
                                    {/*(*/}
                                        {/*this.props.assistantList.map((assistant, i) => <Assistant assistant={assistant}*/}
                                                                                                  {/*key={i}*/}
                                                                                                  {/*index={i}*/}
                                                                                                  {/*isLoading={this.props.isLoading}*/}
                                        {/*/>)*/}
                                    {/*)*/}
                                    {/*: <Skeleton active/>*/}
                            {/*}*/}
                        </div>
                    </div>

                </div>

                {/*<NewAssistantModal visible={this.state.visible}*/}
                                   {/*hideModal={this.hideModal}/>*/}

            </div>
        );
    }
}

function mapStateToProps(state) {
    return {

    };
}

export default connect(mapStateToProps)(Databases);
