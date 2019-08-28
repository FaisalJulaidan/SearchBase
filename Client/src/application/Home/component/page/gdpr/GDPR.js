import React from 'react';
import {WEBSITE_TITLE} from '../../../../../constants/config';
import DescriptiveLayout from "../../../hoc/descriptive-layout/DescriptiveLayout";
import gdprJson from "./gdpr.json"

const GDPR = () => {

    document.title = "GDPR | " + WEBSITE_TITLE;

    return (
        <DescriptiveLayout title="EU General Data Protection Regulation" items={gdprJson}/>
    );
};

export default GDPR;
