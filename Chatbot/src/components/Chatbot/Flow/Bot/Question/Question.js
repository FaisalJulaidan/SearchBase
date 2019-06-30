import React from "react";
import styles from "./Question.module.css";
import {Button as AntdButton} from "antd";


const Question = message => {
    const {answers, skippable, skipText} = message.content;
    const answersBtns = [];

    answers.map((answer, i) => {
        answersBtns.push(
        <AntdButton block key={i} disabled={!message.isLastMsg}
                    onClick={() => message.answerClicked(answer, answers)}>
          {answer.text}
        </AntdButton>);
    });

    // Add the skip button if the question is skippable
    if (skippable) {
        answersBtns.push(
            <AntdButton block data-danger="true" type="danger" key={99} disabled={!message.isLastMsg}
                        onClick={() => message.skipped(skipText)}>
                {skipText}
            </AntdButton>)
    }
    return (
        <div className={styles.Question}>
            {answersBtns}
        </div>
    );
};

export default Question;
