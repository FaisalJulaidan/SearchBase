import React, {Component} from 'react';
import {Button, Card, Checkbox, Col, Collapse, Divider, Row, Tag} from "antd";

const Panel = Collapse.Panel;
const {Meta} = Card;

class Block extends Component {

    editBlock = (block) => this.props.editBlock(block);
    deleteBlock = (block) => this.props.deleteBlock(block);

    render() {
        const {block} = this.props;
        return (
            <Collapse bordered={true}>
                <Panel header={(
                    <>
                        {block.type} <Divider type="vertical"/>
                        {block.Content.text} <Divider type="vertical"/>

                        <Button icon={'edit'} size={"small"} onClick={() => this.editBlock(block)}/>
                        <Divider type="vertical"/>
                        <Button icon={'delete'} size={"small"} type={"danger"}
                                onClick={() => this.deleteBlock(block)}/>
                    </>
                )}
                       key={this.props.key}>

                    {block.Content.text ?
                        <Row>
                            <Col span={6}>Question:</Col>
                            <Col span={12}>{block.Content.text}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.blockToGoID ?
                        <Row>
                            <Col span={6}>block To Go ID:</Col>
                            <Col span={12}>{block.Content.blockToGoID}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.validation ?
                        <Row>
                            <Col span={6}>validation</Col>
                            <Col span={12}>{block.Content.validation}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.action ?
                        <Row>
                            <Col span={6}>action</Col>
                            <Col span={12}>{block.Content.action}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.afterMessage ?
                        <Row>
                            <Col span={6}>after Message</Col>
                            <Col span={12}>{block.Content.afterMessage}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.showTop ?
                        <Row>
                            <Col span={6}>show Top</Col>
                            <Col span={12}>{block.Content.showTop}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.storeInDB ?
                        <Row>
                            <Col span={6}>Stroe in DB:</Col>
                            <Col span={6}><Checkbox checked={block.Content.storeInDB}></Checkbox></Col>

                            <Col span={6}>Skippable:</Col>
                            <Col span={6}><Checkbox checked={block.content.isSkippable}></Checkbox></Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.Content.answers ?
                        <div>
                            Answers:
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

                </Panel>
            </Collapse>
        );
    }

}

export default Block;

