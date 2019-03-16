import React, {Component} from 'react';
import {Collapse, Icon} from 'antd';
import ReactJson from 'react-json-view'

const Panel = Collapse.Panel;

const customPanelStyle = {
    background: '#f7f7f7',
    borderRadius: 4,
    marginBottom: 24,
    border: 0,
    overflow: 'hidden',
};

class SelectedSolutions extends Component {

    removeNulls = (obj) => Object.keys(obj).filter(e => obj[e] !== null && e !== 'ID' && e !== 'DatabaseID')
        .reduce((o, e) => {
            o[e] = obj[e];
            return o;
        }, {});


    render() {

        return (
            <Collapse
                bordered={false}
                defaultActiveKey={['1']}
                expandIcon={({isActive}) => <Icon type="caret-right" rotate={isActive ? 90 : 0}/>}>
                {
                    this.props.solutions.map((solution, i) =>
                        <Panel header={`${solution.type.substring(0, solution.type.length - 1)} ${i + 1} ✅`}
                               key={i}
                               style={customPanelStyle}>
                            <ReactJson src={this.removeNulls(solution.data)}
                                       name={false}
                                       displayDataTypes={false}/>
                        </Panel>
                    )
                }
            </Collapse>
        );
    }
}

export default SelectedSolutions;