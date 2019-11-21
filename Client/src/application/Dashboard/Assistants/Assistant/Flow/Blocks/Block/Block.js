import React, { Component } from 'react';
import { Button, Checkbox, Col, Collapse, Divider, Row, Tag, Tooltip, Typography } from 'antd';

const Panel = Collapse.Panel;
const {Paragraph} = Typography;


class Block extends Component {

    editBlock = (block) => this.props.editBlock(block);
    deleteBlock = (block) => this.props.deleteBlock(block);

    getBlockToGO = (ID) => {
        const {allGroups} = this.props;
        if (!ID)
            return 'None';
        let allBlocks = allGroups.map(group => group.blocks.flat(1)).flat(1);
        let blockToGo = allBlocks.find(block => block.ID === ID);
        return blockToGo?.Content?.text || `Data Scan and Return Block Type`
    };

    switchBlockTypes = (type) => {
        switch (type) {
            case 'User Input':
                return <Tag color="geekblue">Open Answers</Tag>;
            case 'Question':
                return <Tag color="purple">Pre-Selected Answers</Tag>;
            case 'Solutions':
                return <Tag color="blue">Data Scan and Return</Tag>;
            case 'File Upload':
                return <Tag color="cyan">{type}</Tag>;
            case 'Raw Text':
                return <Tag color="magenta">{type}</Tag>;
            case 'Salary Picker':
                return <Tag color="magenta">{type}</Tag>;
            case 'Job Type':
                return <Tag color="red">{type}</Tag>;
            case 'User Type':
                return <Tag color="orange">{type}</Tag>;
            case 'Date Picker':
                return <Tag color="green">{type}</Tag>;
            default:
                return <Tag>{type}</Tag>;
        }
    };

    render() {
        const {block, options} = this.props;
        const databases = options ? options.databases : null;
        return (
            <Collapse bordered={true}>
                <Panel header={(
                    <>

                        <Tooltip title={'Block Type'} placement={'left'}>
                            {this.switchBlockTypes(block.Type)}
                        </Tooltip>

                        <Divider type="vertical"/>

                        {block.Content.text?.substring(0, 90)}
                        {block.Content.text?.length > 90 ? '...' : null}

                        <div style={{float: 'right', marginRight: 10}}>
                            <Tag>{block.DataType.name}</Tag>
                            <Divider type="vertical"/>
                            <Button icon={'edit'} size={"small"} onClick={(event) => {
                                this.editBlock(block);
                                event.stopPropagation();
                            }}/>
                            <Divider type="vertical"/>
                            <Button icon={'delete'} size={"small"} type={"danger"}
                                    onClick={(event) => {
                                        this.deleteBlock(block);
                                        event.stopPropagation();
                                    }}/>
                        </div>
                    </>
                )}
                       key={this.props.key}>

                    {block.Content.text ?
                        <Row>
                            <Col span={6}><b>Question::</b></Col>
                            <Col span={12}>
                                <Paragraph ellipsis={{rows: 1, expandable: true}}>
                                    {block.Content.text}
                                </Paragraph>
                            </Col>
                            <Divider/>
                        </Row>
                        : null
                    }


                    {block.Content.validation ?
                        <Row>
                            <Col span={6}><b>Validation:</b></Col>
                            <Col span={12}>{block.Content.validation}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }


                    {block.Content.showTop ?
                        <Row>
                            <Col span={6}><b>Show Top:</b></Col>
                            <Col span={12}>{block.Content.showTop}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.databaseID ?
                        <Row>
                            <Col span={6}><b>Database:</b></Col>
                            <Col
                                span={12}>{databases.databaseTypes?databases.databaseTypes
                                .find(databaseType => databaseType === block.Content.databaseType):null}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.storeInDB ?
                        <Row>
                            <Col span={6}><b>Store in DB:</b></Col>
                            <Col span={6}><Checkbox checked={block.Content.storeInDB}></Checkbox></Col>

                            <Col span={6}><b>Skippable:</b></Col>
                            <Col span={6}><Checkbox checked={block.content.isSkippable}></Checkbox></Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.answers ?
                        <div>
                            <b>Answers:</b>
                            <div style={{width: '70%', margin: '0 auto 15px'}}>
                                <Collapse accordion>
                                    {
                                        block.Content.answers.map((answer, i) => (
                                            <Collapse.Panel header={answer.text} key={i}>
                                                <Row>
                                                    <Col span={8}>Answer:</Col>
                                                    <Col span={16}>
                                                        {answer.text}
                                                    </Col>
                                                </Row>

                                                <Row>
                                                    <Divider/>
                                                    <Col span={8}>Action:</Col>
                                                    <Col span={16}>{answer.action}</Col>
                                                </Row>

                                                <Row>
                                                    <Divider/>
                                                    <Col span={8}>Question To Go Text:</Col>
                                                    <Col span={16}>
                                                        {this.getBlockToGO(answer.blockToGoID || null)}
                                                    </Col>
                                                </Row>


                                                <Row>
                                                    <Divider/>
                                                    <Col span={8}>Keywords:</Col>
                                                    <Col span={16}>
                                                        {
                                                            answer.keywords[0] ?
                                                                answer.keywords.map((keyword, i) =>
                                                                    <Tag key={i}>{keyword}</Tag>)
                                                                : 'No Keywords'
                                                        }
                                                    </Col>
                                                </Row>

                                                {
                                                    answer.afterMessage &&
                                                    <Row>
                                                        <Divider/>
                                                        <Col span={8}>After Message:</Col>
                                                        <Col span={16}>{answer.afterMessage}</Col>
                                                    </Row>
                                                }

                                            </Collapse.Panel>
                                        ))
                                    }
                                </Collapse>
                            </div>
                        </div>
                        : null
                    }

                    {block.Content.action ?
                        <Row>
                            <Col span={6}><b>Action:</b></Col>
                            <Col span={12}>{block.Content.action}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {
                        block.Type !== 'Question' &&
                        <Row>
                            <Col span={6}><b>Question To Go Text:</b></Col>
                            <Col span={12}>
                                {
                                    this.getBlockToGO(block.Content.blockToGoID || null)
                                }
                            </Col>
                            <Divider/>
                        </Row>
                    }

                    {block.Content.afterMessage ?
                        <Row>
                            <Col span={6}><b>After Message:</b></Col>
                            <Col span={12}>{block.Content.afterMessage}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }


                    {block.Skippable && block.SkipAction ?
                        <>
                            <Divider dashed={true} style={{fontWeight: 'normal', fontSize: '14px'}}>
                                {block.Type === 'Solutions' ? 'Not Found' : 'Skip'} Button
                            </Divider>
                            <Row>

                                <Col span={6}><b>Action:</b></Col>
                                <Col span={12}>{block.SkipAction}</Col>
                                <Divider/>
                            </Row>

                            <Row>
                                <Col span={6}>
                                    <b>
                                        Question To Go Text When {block.Type === 'Solutions' ? 'Not Found' : 'Skip'}:
                                    </b>
                                </Col>
                                <Col span={12}>
                                    {this.getBlockToGO(block.SkipBlockToGoID || null)}
                                </Col>
                                <Divider/>
                            </Row>

                        </>
                        : null
                    }


                </Panel>
            </Collapse>
        );
    }

}

export default Block;

