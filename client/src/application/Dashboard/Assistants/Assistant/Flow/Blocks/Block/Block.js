import React, {Component} from 'react';
import {Row, Col, Collapse, Divider, Button, Card, Tag} from "antd";

const Panel = Collapse.Panel;
const {Meta} = Card;

class Block extends Component {

    render() {
        const {block} = this.props;
        return (
            <Collapse bordered={true}>
                <Panel header={(
                    <>
                        {block.type} <Divider type="vertical"/>
                        {block.content.text} <Divider type="vertical"/>
                        <Button icon={'edit'} size={"small"}/> <Divider type="vertical"/>
                        <Button icon={'delete'} size={"small"} type={"danger"}/>
                    </>
                )}
                       key={this.props.key}>

                    {block.content.text ?
                        <Row>
                            <Col span={6}>Question:</Col>
                            <Col span={12}>{block.content.text}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.content.blockToGoID ?
                        <Row>
                            <Col span={6}>block To Go ID:</Col>
                            <Col span={12}>{block.content.blockToGoID}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.content.validation ?
                        <Row>
                            <Col span={6}>validation</Col>
                            <Col span={12}>{block.content.validation}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.content.action ?
                        <Row>
                            <Col span={6}>action</Col>
                            <Col span={12}>{block.content.action}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.content.afterMessage ?
                        <Row>
                            <Col span={6}>after Message</Col>
                            <Col span={12}>{block.content.afterMessage}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.content.showTop ?
                        <Row>
                            <Col span={6}>show Top</Col>
                            <Col span={12}>{block.content.showTop}</Col>
                            <Divider/>
                        </Row>
                        : null
                    }

                    {block.content.answers ?
                        <>
                            Answers:
                            {
                                block.content.answers.map((answer, i) =>
                                    <Card key={i}>
                                        <Meta
                                            title={answer.text}
                                            description={
                                                answer.keywords.map((keyword, i) =>
                                                    <Tag key={i}>{keyword}</Tag>)
                                            }
                                        />
                                    </Card>
                                )
                            }
                            <Divider/>
                        </>
                        : null
                    }

                </Panel>
            </Collapse>
        );
    }

}

export default Block;

