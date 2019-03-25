import React, {Component} from 'react';
import {Button, Card, Checkbox, Col, Collapse, Divider, Row, Tag, Typography} from "antd";

const Panel = Collapse.Panel;
const {Meta} = Card;
const {Paragraph} = Typography;


class Block extends Component {

    editBlock = (block) => this.props.editBlock(block);
    deleteBlock = (block) => this.props.deleteBlock(block);

    render() {
        const {block, options} = this.props;
        const databases = options ? options.databases : null;

        return (
            <Collapse bordered={true}>
                <Panel header={(
                    <>
                        {block.Type} <Divider type="vertical"/>
                        {block.Content.text?.substring(0, 90)}
                        {block.Content.text?.length > 90 ? '...' : null}

                        <div style={{float: 'right', marginRight: 10}}>
                            <Divider type="vertical"/>
                            <Button icon={'edit'} size={"small"} onClick={() => this.editBlock(block)}/>
                            <Divider type="vertical"/>
                            <Button icon={'delete'} size={"small"} type={"danger"}
                                    onClick={() => this.deleteBlock(block)}/>
                        </div>
                    </>
                )}
                       key={this.props.key}>

                    {block.Content.text ?
                        <Row>
                            <Col span={6}><b>Question::</b></Col>
                            <Col span={12}>
                                <Paragraph ellipsis={{rows: 1, expandable: false}}>
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

                    {block.Content.action ?
                        <Row>
                            <Col span={6}><b>Action:</b></Col>
                            <Col span={12}>{block.Content.action}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.afterMessage ?
                        <Row>
                            <Col span={6}><b>After Message:</b></Col>
                            <Col span={12}>{block.Content.afterMessage}</Col>
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
                            {
                                block.Content.answers.map((answer, i) =>
                                    <Card key={i} style={{margin: 5, width: 300}}>
                                        <Meta
                                            title={answer.text}
                                            description={
                                                (<>Keywords: {answer.keywords.map((keyword, i) =>
                                                    <Tag key={i}>{keyword}</Tag>)}</>)
                                            }
                                        />
                                        <Row>
                                            <Divider/>
                                            <Col span={6}>Action:</Col>
                                            <Col span={12}>{answer.action}</Col>
                                        </Row>

                                        <Row>
                                            <Divider/>
                                            <Col span={6}>After Message</Col>
                                            <Col span={12}>{answer.afterMessage}</Col>
                                        </Row>

                                    </Card>
                                )
                            }
                        </div>
                        : null
                    }

                    <Row>
                        <Col span={6}><b>Block To Go ID:</b></Col>
                        <Col span={12}>{block.Content.blockToGoID || `None`}</Col>
                        <Divider/>
                    </Row>

                </Panel>
            </Collapse>
        );
    }

}

export default Block;

