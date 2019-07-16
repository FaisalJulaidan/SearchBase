import React from "react";
import {Badge, Button as AntdButton, Card, Carousel, Tag} from "antd";
import 'antd/lib/card/style';
import 'antd/lib/carousel/style';
import 'antd/lib/tag/style';
import 'antd/lib/badge/style';
import styles from "./Solutions.module.css";
import './Solutions.css'


const Solutions = message => {
    let isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
    let isEdge = /Edge/.test(navigator.userAgent);

    const {solutions, skippable, skipText}= message.content;
    if (!solutions[0])
        return (<div>Sorry, I couldn't find anything for you 😕</div>);


    const card = (solution, i) => (
        <Card hoverable className={styles.Card}
              key={i}
              cover={<img alt="example" height="100px" style={{objectFit: 'cover'}}
                          src="https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/voice_control_ofo1.svg"/>}
        >
            <div className={styles.Card_Text}>
                <h3 className={styles.Title}>{solution.title} </h3>
                {solution.subTitles.map(title => <p className={styles.SubTitle}>{title}</p>)}
                <div className={styles.Paragraph}>{solution.description}</div>
            </div>

            <div className={styles.Card_Buttons}>
                <AntdButton block disabled={!message.isLastMsg}
                            onClick={() => message.selectSolution(solution)}>
                    {solution.selected ? <Tag color="#87d068">Selected</Tag> : solution.buttonText}
                </AntdButton>
            </div>
        </Card>
    );

    // Create the skip button if Skippable is set as true
    let button = skippable ?
        (<AntdButton block data-warning="true" type="danger" key={8}
                    disabled={!message.isLastMsg}
                    onClick={() => message.skipped(skipText)}>
            {skipText}
        </AntdButton>) : null;

    // If there is at least one selected solution convert the skip button so submit
    if (solutions.findIndex(s => s.selected) > -1) {
        const selected = solutions.filter(s => s.selected);
        button = (
            <Badge count={selected.length} style={{ backgroundColor: '#0589ff' }} dot={solutions.length === 1}>
                <AntdButton block  key={9}
                            disabled={!message.isLastMsg}
                            onClick={() => message.submitSolutions(selected)}>
                    Submit Application(s)
                </AntdButton>
            </Badge> );
    }


    return (
    <div className={styles.Solutions}>
        {solutions.length > 1 ? <div className={styles.Text}>*Multiple selection</div> : ""}
        {
            solutions.length === 1 ?
                card(solutions[0])
                :
                <Carousel draggable centerMode={!(isIE11 || isEdge)} arrows infinite={false}>
                    {solutions.map((solution, i) => card(solution, i))}
                </Carousel>
        }
        <br/>
        {button}
    </div>);
};

export default Solutions;