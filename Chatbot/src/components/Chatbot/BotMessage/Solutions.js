import React, { useState } from 'react';
import { Badge, Button, Card, Carousel, Tag } from 'antd';
// Constants
import * as solutionAttributes from '../../../constants/SolutionAttributes';
// Styles
import './styles/Solutions.css';
import * as messageTypes from '../../../constants/MessageType';

const Solutions = ({responded, submitSolution, skipResponse, solutions, skippable, skipText}) => {
    const isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
    const isEdge = /Edge/.test(navigator.userAgent);
    let [selectedSolutions, setSelectedSolutions] = useState([]);

    const toggleSelect = (key) => {
        setSelectedSolutions(solutions => {
            let s = [...solutions];
            if (solutions.includes(key))
                return s.filter(s => s !== key);
            else {
                s.push(key);
                return s;
            }
        });
    };

    const handleSubmit = () => {
        const selected = selectedSolutions.map(key => solutions[key]);
        console.log(selected)
        submitSolution(
            '✅',
            messageTypes.TEXT,
            {skipped: false, selectedSolutions: selected});
    };

    // Create the skip button if Skippable is set as true
    let button = skippable ?
        (<Button block data-warning="true" type="danger" key={8}
                 disabled={responded}
                 className={['Button', 'Danger', 'SkipButton'].join(' ')}
                 onClick={skipResponse}>
            {skipText}
        </Button>) : null;

    if (selectedSolutions.length > 0) {
        button = (
            <Badge count={selectedSolutions.length} style={{backgroundColor: '#0589ff'}} dot={solutions.length === 1}>
                <Button block key={9}
                        disabled={responded}
                        onClick={() => handleSubmit()}>
                    Submit Application(s)
                </Button>
            </Badge>);
    }

    const props = {
        responded: responded,
        toggleSelect: toggleSelect
    };

    if (solutions) {
        if (!solutions.length) {
            return null;
        }
    } else {
        return null
    }

    return (
        <div className={'Solutions'}>
            {
                solutions.length === 1 ?
                    <SingleSolution {...props}
                                    solution={solutions[0]}
                                    selected={!!selectedSolutions.length}
                                    index={0}/>
                    :
                    <>
                        <div className={'Solutions_Text'}>*Multiple selection</div>
                        <Carousel variableWidth={false} draggable centerMode={!(isIE11 || isEdge)} arrows
                                  infinite={false}>
                            {solutions.map((solution, i) => {
                                return (
                                    <Solution {...props}
                                              key={i} index={i}
                                              solution={solution}
                                              selected={selectedSolutions.filter(k => k === i).length}/>
                                );
                            })}
                        </Carousel>
                    </>

            }
            {button}
        </div>
    );
};


const Solution = ({solution, index, selected, responded, toggleSelect}) => {

    let subtitles = solution[solutionAttributes.SUB_TITLES].constructor === Array ? solution[solutionAttributes.SUB_TITLES] : [solution[solutionAttributes.SUB_TITLES]]

    return (
        <Card hoverable className={'Card'}
              cover={<img alt="example" height="100px" style={{ objectFit: 'cover', height: 100 }}
                          src="https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/voice_control_ofo1.svg"/>}
        >
            <div className={'Card_Text'}>
                <h3 className={'Title'}>{solution.title} </h3>
                {subtitles.map((subtitle, i) => <p key={i}
                                                   className={'SubTitle'}>{subtitle}</p>)}
                <div className={'Paragraph'}>{solution[solutionAttributes.DESCRIPTION]}</div>
            </div>

            <div className={'Card_Buttons'}>
                <Button block disabled={responded} onClick={() => toggleSelect(index)}>
                    {selected ? <Tag color="#87d068">Selected</Tag> : solution[solutionAttributes.BUTTON_TEXT]}
                </Button>
            </div>
        </Card>
    );
};

const SingleSolution = ({solution, index, selected, responded, toggleSelect}) => {

    let subtitles = solution[solutionAttributes.SUB_TITLES].constructor === Array ? solution[solutionAttributes.SUB_TITLES] : [solution[solutionAttributes.SUB_TITLES]]

    return (
        <div className={'Single_Solution'}>
            <Card hoverable className={'Card'}
                  cover={<img alt="example" height="100px" style={{ objectFit: 'cover', height: 100 }}
                              src="https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/voice_control_ofo1.svg"/>}
            >
                <div className={'Card_Text'}>
                    <h3 className={'Title'}>{solution.title} </h3>
                    {subtitles.map((subtitle, i) => <p key={i}
                                                       className={'SubTitle'}>{subtitle}</p>)}
                    <div className={'Paragraph'}>{solution[solutionAttributes.DESCRIPTION]}</div>
                </div>

                <div className={'Card_Buttons'}>
                    <Button block disabled={responded} onClick={() => toggleSelect(index)}>
                        {selected ? <Tag color="#87d068">Selected</Tag> : solution[solutionAttributes.BUTTON_TEXT]}
                    </Button>
                </div>
            </Card>
        </div>
    );
};

export default Solutions;
