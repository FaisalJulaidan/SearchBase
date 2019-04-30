import React from 'react';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import AuroraCard from 'components/AuroraCard/AuroraCard'
import {Typography} from 'antd';
import {LoremIpsum} from "lorem-ipsum";


import styles from './Integrations.module.less'
import {getLink} from "helpers";

const {Title} = Typography;
const lorem = new LoremIpsum({
    sentencesPerParagraph: {
        max: 8,
        min: 4
    },
    wordsPerSentence: {
        max: 16,
        min: 4
    }
});


class Integrations extends React.Component {

    state = {
        i: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    };

    render() {
        return (
            <NoHeaderPanel>
                <div className={styles.Title}>
                    <Title>All Integrations</Title>
                </div>

                <div className={styles.Body}>
                    {
                        this.state.i.map((_, i) =>
                            <div className={styles.CardFrame}>
                                <AuroraCard title={lorem.generateWords(1)}
                                            desc={lorem.generateWords(7)}
                                            image={getLink('/static/images/CRM/adapt.png')}/>
                            </div>
                        )
                    }
                </div>

            </NoHeaderPanel>
        );
    }
}

export default Integrations;
