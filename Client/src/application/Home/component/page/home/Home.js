import React from 'react';
import styles from './home.module.css'
import Intro from "./intro/Intro";
import DividerButton from "./divider-button/DividerButton";
import MessageIntro from "./message-intro/MessageIntro";
import CaptureCandidates from "./capture-candidates/CaptureCandidates";
import OurFocus from "./our-focus/OurFocus";
import WhyWait from "./why-wait/WhyWait";
import {WEBSITE_TITLE} from '../../../../../constants/config';
import Layout from "../../../hoc/layout/Layout";
import Integrations from "./integrations/Integrations";
import KeyFeatures from "./key-features/KeyFeatures";
import Conversations from "./conversations/Conversations";
import Statistics from "./statistics/Statistics";
import Partners from "./partners/Partners";

const Home = () => {

    document.title = WEBSITE_TITLE;

    return (
        <Layout background={"#FFFFFF"}>
            <div>
                <section className={styles.section}>
                    <Intro/>
                </section>
                <section className={styles.section}>
                    <Partners/>
                </section>
                <section className={styles.section}>
                    <MessageIntro id="intro2"/>
                </section>
                <DividerButton scrollTo="ourFocus"/>
                <section className={styles.section}>
                    <OurFocus id="ourFocus"/>
                </section>
                <section className={styles.section}>
                    <Integrations id="integrations"/>
                </section>
                <section className={styles.section}>
                    <KeyFeatures id="keyFeatures"/>
                </section>
                <section className={styles.section}>
                    <CaptureCandidates id="captureCandidates"/>
                </section>
                <section className={styles.section}>
                    <Conversations id="conversations"/>
                </section>
                <section className={styles.section}>
                    <Statistics id="statistics"/>
                </section>
                <section className={styles.section}>
                    <WhyWait/>
                </section>
            </div>
        </Layout>
    );
};

export default Home;
